"""BMW MS41 ECU interface — command builders and response parsers.

Supports:
  - ECU identification
  - Live data (analog block 3): 30 parameters
  - DTC read / clear
  - Adaptation values

All communication goes through KLineUART -> L9637D -> K-Line -> MS41 ECU.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .ds2_protocol import build_frame, validate_response, is_positive_ack
from .kline_uart import KLineUART
from config import DS2_ECU_ADDR

# ---- DS2 Command Payloads ----
CMD_ECU_IDENT      = bytes([0x00])
CMD_ANALOG_BLOCK_3 = bytes([0x0B, 0x03])
CMD_ANALOG_BLOCK_1 = bytes([0x0B, 0x01])
CMD_ANALOG_BLOCK_2 = bytes([0x0B, 0x02])
CMD_STATUS_READ    = bytes([0x0B, 0x04])
CMD_READ_DTC       = bytes([0x06])
CMD_CLEAR_DTC      = bytes([0x05])
CMD_READ_ADAPT     = bytes([0x0B, 0x10])
CMD_RESET_ADAPT    = bytes([0x09, 0x10])


@dataclass
class MS41LiveData:
    """Parsed live sensor data from MS41 analog block 3."""
    rpm: int = 0                    # Engine speed [RPM]
    coolant_temp: float = 0.0       # Coolant temperature [C]
    intake_air_temp: float = 0.0    # Intake air temperature [C]
    throttle_pos: float = 0.0       # Throttle position [%]
    battery_voltage: float = 0.0    # Battery voltage [V]
    engine_load: float = 0.0        # Engine load [mg/stroke]
    lambda_int_b1: float = 0.0      # Lambda integrator bank 1 [%]
    lambda_int_b2: float = 0.0      # Lambda integrator bank 2 [%]
    stft_b1: float = 0.0            # Short-term fuel trim B1 [%]
    stft_b2: float = 0.0            # Short-term fuel trim B2 [%]
    oil_temp: float = 0.0           # Oil temperature [C]
    vehicle_speed: int = 0          # Vehicle speed [km/h]
    ignition_timing: float = 0.0    # Ignition timing [deg BTDC]
    idle_target: int = 0            # Idle target RPM
    idle_actual: int = 0            # Idle actual RPM
    vanos_position: float = 0.0     # VANOS intake [deg]
    lambda_v_b1_pre: float = 0.0    # O2 sensor B1 pre-cat [V]
    lambda_v_b2_pre: float = 0.0    # O2 sensor B2 pre-cat [V]
    lambda_v_b1_post: float = 0.0   # O2 sensor B1 post-cat [V]
    lambda_v_b2_post: float = 0.0   # O2 sensor B2 post-cat [V]
    idle_valve_pos: float = 0.0     # Idle valve position [%]
    ltft_b1: float = 0.0            # Long-term fuel trim B1 [%]
    ltft_b2: float = 0.0            # Long-term fuel trim B2 [%]
    cat_temp_b1: float = 0.0        # Catalyst temp B1 [C]
    cat_temp_b2: float = 0.0        # Catalyst temp B2 [C]
    map_pressure: float = 0.0       # MAP sensor [bar]
    injection_time: float = 0.0     # Injection time [ms]
    knock_retard_13: float = 0.0    # Knock retard cyl 1-3 [deg]
    knock_retard_46: float = 0.0    # Knock retard cyl 4-6 [deg]


@dataclass
class MS41DTC:
    """A single diagnostic trouble code."""
    code: int = 0
    status: int = 0

    @property
    def hex_str(self) -> str:
        return f"0x{self.code:04X}"


# ---- Common DTC descriptions ----
DTC_DESCRIPTIONS = {
    0x0001: "DME control module internal fault",
    0x000A: "Intake air temp sensor: open/short",
    0x000B: "Coolant temp sensor: open/short",
    0x0014: "Throttle position sensor: out of range",
    0x001E: "Idle speed controller: open/short",
    0x0028: "O2 sensor B1S1: heating circuit",
    0x0029: "O2 sensor B1S2: heating circuit",
    0x002A: "O2 sensor B2S1: heating circuit",
    0x002B: "O2 sensor B2S2: heating circuit",
    0x0032: "Knock sensor 1: signal",
    0x0033: "Knock sensor 2: signal",
    0x003C: "VANOS intake: control deviation",
    0x0046: "Fuel injector cyl 1: open/short",
    0x0047: "Fuel injector cyl 2: open/short",
    0x0048: "Fuel injector cyl 3: open/short",
    0x0049: "Fuel injector cyl 4: open/short",
    0x004A: "Fuel injector cyl 5: open/short",
    0x004B: "Fuel injector cyl 6: open/short",
    0x0050: "Ignition coil cyl 1",
    0x0051: "Ignition coil cyl 2",
    0x0052: "Ignition coil cyl 3",
    0x0053: "Ignition coil cyl 4",
    0x0054: "Ignition coil cyl 5",
    0x0055: "Ignition coil cyl 6",
    0x005A: "Crankshaft position sensor",
    0x005B: "Camshaft position sensor",
    0x0064: "Fuel pump relay: open/short",
    0x0065: "AC compressor relay",
    0x006E: "EWS (immobilizer) tampering",
    0x006F: "EWS communication error",
    0x0078: "Catalyst efficiency B1 below threshold",
    0x0079: "Catalyst efficiency B2 below threshold",
    0x0082: "Misfire detected (multiple cylinders)",
    0x008C: "Fuel system too lean B1",
    0x008D: "Fuel system too rich B1",
    0x008E: "Fuel system too lean B2",
    0x008F: "Fuel system too rich B2",
    0x0096: "Vehicle speed signal",
    0x00A0: "Secondary air system",
    0x00AA: "EVAP system leak detected",
    0x00B4: "Tank vent valve",
}


class MS41:
    """High-level interface to the BMW MS41 ECU over K-Line."""

    def __init__(self, kline: KLineUART):
        self._kline = kline
        self.connected = False

    def connect(self, use_slow_init: bool = False) -> bool:
        """Initialize K-Line and verify ECU responds.

        Args:
            use_slow_init: If True, use 5-baud slow init instead of fast init.
        """
        if use_slow_init:
            ok = self._kline.slow_init(DS2_ECU_ADDR)
        else:
            ok = self._kline.fast_init()

        if not ok:
            self.connected = False
            return False

        # Verify with ECU ident
        frame = build_frame(DS2_ECU_ADDR, CMD_ECU_IDENT)
        resp = self._kline.transaction(frame)

        if resp and validate_response(resp) and is_positive_ack(resp):
            self.connected = True
            return True

        self.connected = False
        return False

    def read_live_data(self) -> Optional[MS41LiveData]:
        """Request and parse analog block 3 (all 30 live parameters)."""
        frame = build_frame(DS2_ECU_ADDR, CMD_ANALOG_BLOCK_3)
        resp = self._kline.transaction(frame)

        if not resp or not validate_response(resp) or not is_positive_ack(resp):
            return None

        return self._parse_analog_block3(resp)

    def read_dtc(self) -> Optional[List[MS41DTC]]:
        """Read stored diagnostic trouble codes."""
        frame = build_frame(DS2_ECU_ADDR, CMD_READ_DTC)
        resp = self._kline.transaction(frame)

        if not resp or not validate_response(resp) or not is_positive_ack(resp):
            return None

        # Each DTC = 3 bytes after the ACK: code_hi, code_lo, status
        data_start = 3
        data_end = len(resp) - 1  # exclude checksum
        data = resp[data_start:data_end]

        dtcs = []
        for i in range(0, len(data) - 2, 3):
            code = (data[i] << 8) | data[i + 1]
            status = data[i + 2]
            dtcs.append(MS41DTC(code=code, status=status))

        return dtcs

    def clear_dtc(self) -> bool:
        """Clear all stored fault codes."""
        frame = build_frame(DS2_ECU_ADDR, CMD_CLEAR_DTC)
        resp = self._kline.transaction(frame)
        return bool(resp and validate_response(resp) and is_positive_ack(resp))

    def read_ecu_ident(self) -> Optional[bytes]:
        """Read ECU identification (hardware/software version, part number)."""
        frame = build_frame(DS2_ECU_ADDR, CMD_ECU_IDENT)
        resp = self._kline.transaction(frame)
        if resp and validate_response(resp) and is_positive_ack(resp):
            return resp[3:-1]  # data between ACK and checksum
        return None

    @staticmethod
    def dtc_description(code: int) -> str:
        return DTC_DESCRIPTIONS.get(code, f"Unknown DTC 0x{code:04X}")

    # ---- Parsing ----

    @staticmethod
    def _parse_analog_block3(resp: bytes) -> Optional[MS41LiveData]:
        """Parse analog block 3 response into MS41LiveData."""
        if len(resp) < 33:
            return None

        d = resp[3:]  # skip addr, len, ACK
        data = MS41LiveData()

        data.rpm              = (d[0] << 8) | d[1]
        data.coolant_temp     = d[2] * 0.75 - 48.0
        data.intake_air_temp  = d[3] * 0.75 - 48.0
        data.throttle_pos     = d[4] * 100.0 / 255.0
        data.battery_voltage  = d[5] * 0.1
        data.engine_load      = ((d[6] << 8) | d[7]) * 0.021
        data.lambda_int_b1    = d[8] * 0.78125 - 100.0
        data.lambda_int_b2    = d[9] * 0.78125 - 100.0
        data.stft_b1          = (d[10] - 128) * 100.0 / 128.0
        data.stft_b2          = (d[11] - 128) * 100.0 / 128.0
        data.oil_temp         = d[12] * 0.796098 - 48.0137
        data.vehicle_speed    = (d[13] << 8) | d[14]
        data.ignition_timing  = d[15] * 0.375 - 22.5
        data.idle_target      = (d[16] << 8) | d[17]
        data.idle_actual      = (d[18] << 8) | d[19]
        data.vanos_position   = d[20] * 0.375
        data.lambda_v_b1_pre  = d[21] * 0.0196
        data.lambda_v_b2_pre  = d[22] * 0.0196
        data.lambda_v_b1_post = d[23] * 0.0196
        data.lambda_v_b2_post = d[24] * 0.0196
        data.idle_valve_pos   = d[25] * 100.0 / 255.0
        data.ltft_b1          = (d[26] - 128) * 100.0 / 128.0
        data.ltft_b2          = (d[27] - 128) * 100.0 / 128.0

        # Extended fields (only if response is long enough)
        if len(d) >= 38:
            data.cat_temp_b1      = ((d[28] << 8) | d[29]) * 0.1
            data.cat_temp_b2      = ((d[30] << 8) | d[31]) * 0.1
            data.map_pressure     = ((d[32] << 8) | d[33]) * 0.01
            data.injection_time   = ((d[34] << 8) | d[35]) * 0.004
            data.knock_retard_13  = d[36] * 0.375
            data.knock_retard_46  = d[37] * 0.375

        return data
