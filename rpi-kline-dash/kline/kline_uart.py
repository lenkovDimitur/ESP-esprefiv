"""K-Line transport layer — direct UART via L9637D on Raspberry Pi GPIO.

Wiring:
  Pi GPIO14 (TX) ──> L9637D TX pin
  Pi GPIO15 (RX) <── L9637D RX pin
  L9637D K pin   <──> OBD-II Pin 7 (K-Line to BMW MS41)
  L9637D VCC     <── 5V (from OBD Pin 16 via buck converter)
  L9637D EN      <── 5V (always enabled)
  Common GND

The L9637D handles 3.3V <-> 12V level shifting.
K-Line is half-duplex: every TX byte echoes back on RX and must be discarded.

Initialization:
  Fast Init: pull TX LOW 25ms, HIGH 25ms, then start UART at 9600 8E1.
  Slow Init (5-baud): send address byte 0x12 at 5 baud (200ms/bit),
                       wait for sync 0x55, key bytes 0x08 0x08, reply 0xF7.
"""

import time
import serial

# Attempt to import RPi.GPIO for fast-init bit-banging
try:
    import RPi.GPIO as GPIO
    HAS_GPIO = True
except ImportError:
    HAS_GPIO = False

from config import (
    KLINE_PORT, KLINE_BAUD, KLINE_PARITY, KLINE_STOPBITS,
    KLINE_BYTESIZE, KLINE_TIMEOUT, KLINE_ECHO_TIMEOUT, KLINE_TX_GPIO,
)


class KLineUART:
    """K-Line serial transport using Pi UART through L9637D transceiver."""

    def __init__(self):
        self._ser = None

    def open(self):
        """Open the UART port at 9600 8E1."""
        self._ser = serial.Serial(
            port=KLINE_PORT,
            baudrate=KLINE_BAUD,
            bytesize=KLINE_BYTESIZE,
            parity=KLINE_PARITY,
            stopbits=KLINE_STOPBITS,
            timeout=KLINE_TIMEOUT,
        )
        self._ser.reset_input_buffer()
        self._ser.reset_output_buffer()

    def close(self):
        if self._ser and self._ser.is_open:
            self._ser.close()
            self._ser = None

    # ---- Fast Initialization (25ms LOW / 25ms HIGH) ----

    def fast_init(self) -> bool:
        """Perform K-Line fast initialization.

        Closes UART, bit-bangs the TX pin LOW/HIGH for the init pulse,
        then re-opens UART. This wakes up the MS41 ECU.
        """
        # Close UART so we can control the TX pin as GPIO
        self.close()

        if HAS_GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(KLINE_TX_GPIO, GPIO.OUT)

            # Pull LOW for 25ms
            GPIO.output(KLINE_TX_GPIO, GPIO.LOW)
            time.sleep(0.025)

            # Pull HIGH for 25ms
            GPIO.output(KLINE_TX_GPIO, GPIO.HIGH)
            time.sleep(0.025)

            # Release GPIO back to UART alt function
            GPIO.cleanup(KLINE_TX_GPIO)
        else:
            # No GPIO available (dev mode) — just wait
            print("[KLINE] WARNING: No RPi.GPIO, skipping fast init pulse")
            time.sleep(0.050)

        # Re-open UART
        self.open()
        time.sleep(0.050)

        # Flush any garbage
        self._ser.reset_input_buffer()
        return True

    # ---- Slow Initialization (5-baud / ISO 9141-2) ----

    def slow_init(self, address: int = 0x12) -> bool:
        """Perform 5-baud slow initialization per ISO 9141-2.

        Sends address byte at 5 baud (200ms per bit), waits for:
          - Sync byte 0x55
          - Key byte 1: 0x08
          - Key byte 2: 0x08
        Then replies with inverted key byte 2 (0xF7).
        """
        self.close()

        if not HAS_GPIO:
            print("[KLINE] WARNING: No RPi.GPIO, cannot do slow init")
            self.open()
            return False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(KLINE_TX_GPIO, GPIO.OUT)

        BIT_DURATION = 0.200  # 200ms per bit at 5 baud

        # Start bit (LOW)
        GPIO.output(KLINE_TX_GPIO, GPIO.LOW)
        time.sleep(BIT_DURATION)

        # 8 data bits, LSB first
        for i in range(8):
            bit = (address >> i) & 0x01
            GPIO.output(KLINE_TX_GPIO, GPIO.HIGH if bit else GPIO.LOW)
            time.sleep(BIT_DURATION)

        # Stop bit (HIGH)
        GPIO.output(KLINE_TX_GPIO, GPIO.HIGH)
        time.sleep(BIT_DURATION)

        # Release GPIO, re-open UART
        GPIO.cleanup(KLINE_TX_GPIO)
        self.open()

        # Wait for sync byte 0x55 (ECU wakes up within ~300ms)
        sync = self._ser.read(1)
        if not sync or sync[0] != 0x55:
            print(f"[KLINE] Slow init: no sync (got {sync.hex() if sync else 'timeout'})")
            return False

        # Read key bytes
        key_bytes = self._ser.read(2)
        if len(key_bytes) < 2:
            print("[KLINE] Slow init: missing key bytes")
            return False

        print(f"[KLINE] Slow init: sync=0x55, keys=0x{key_bytes[0]:02X} 0x{key_bytes[1]:02X}")

        # Reply with inverted key byte 2
        inverted = (~key_bytes[1]) & 0xFF
        self._ser.write(bytes([inverted]))
        self._ser.flush()

        # Discard echo of our reply
        self._read_echo(1)

        # Wait for inverted address from ECU
        inv_addr = self._ser.read(1)
        if not inv_addr:
            print("[KLINE] Slow init: no inverted address response")
            return False

        expected = (~address) & 0xFF
        if inv_addr[0] != expected:
            print(f"[KLINE] Slow init: bad inv addr 0x{inv_addr[0]:02X} (expected 0x{expected:02X})")
            return False

        print("[KLINE] Slow init successful")
        return True

    # ---- Send / Receive ----

    def send(self, frame: bytes) -> bool:
        """Send a DS2 frame and discard the K-Line echo."""
        if not self._ser or not self._ser.is_open:
            return False

        self._ser.write(frame)
        self._ser.flush()
        return self._read_echo(len(frame))

    def receive(self) -> bytes:
        """Receive a DS2 response frame.

        Reads the address + length header, then reads remaining bytes.
        Returns the complete frame or empty bytes on timeout.
        """
        if not self._ser or not self._ser.is_open:
            return b""

        # Read first 2 bytes (address + length)
        header = self._ser.read(2)
        if len(header) < 2:
            return b""

        expected_len = header[1]
        if expected_len < 3 or expected_len > 128:
            return b""

        # Read remaining bytes
        remaining = expected_len - 2
        rest = self._ser.read(remaining)
        if len(rest) < remaining:
            return b""

        return header + rest

    def transaction(self, frame: bytes) -> bytes:
        """Send a request and receive the response (full DS2 transaction)."""
        if not self.send(frame):
            return b""
        return self.receive()

    # ---- Internal ----

    def _read_echo(self, count: int) -> bool:
        """Read and discard `count` echo bytes from K-Line half-duplex."""
        if not self._ser:
            return False
        old_timeout = self._ser.timeout
        self._ser.timeout = KLINE_ECHO_TIMEOUT
        echo = self._ser.read(count)
        self._ser.timeout = old_timeout
        return len(echo) == count
