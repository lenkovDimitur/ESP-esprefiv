"""Configuration for BMW MS41 Gauge Cluster — Raspberry Pi Zero 2 W.

Single-board architecture:
  Pi Zero 2 W  ──UART──  L9637D  ──K-Line──  BMW MS41 ECU
  Pi Zero 2 W  ──HDMI──  Waveshare 7" 1024x600
"""

# ---- Display ----
SCREEN_W = 1024
SCREEN_H = 600
FPS = 30
FULLSCREEN = True  # Set False for windowed dev/debug mode

# ---- K-Line UART (Pi GPIO14 TX / GPIO15 RX via L9637D) ----
KLINE_PORT = "/dev/ttyAMA0"   # Pi hardware UART (GPIO 14/15)
KLINE_BAUD = 9600
KLINE_PARITY = "E"            # Even parity
KLINE_STOPBITS = 1
KLINE_BYTESIZE = 8
KLINE_TIMEOUT = 0.25          # 250ms response timeout
KLINE_ECHO_TIMEOUT = 0.05     # 50ms to read back echo

# ---- DS2 Protocol ----
DS2_ECU_ADDR = 0x12            # DME / Motronic (MS41)
DS2_ACK_OK = 0xA0
DS2_ACK_FAIL = 0xB0

# ---- K-Line Init Pins (for fast init bit-bang) ----
# TX pin must be toggled as GPIO for the 25ms LOW/HIGH init sequence
# GPIO14 = UART TX (directly drives L9637D TX input)
KLINE_TX_GPIO = 14

# ---- Timing ----
POLL_INTERVAL_S = 0.100        # 10 Hz polling
INIT_DELAY_S = 2.0             # Wait after power-on before init
RECONNECT_INTERVAL_S = 5.0    # Retry if ECU not responding

# ---- Colors (matching original gauge design) ----
CLR_BG          = (13, 13, 13)
CLR_PANEL       = (22, 22, 22)
CLR_RPM_ARC     = (255, 69, 0)       # Red-orange tachometer
CLR_SPD_ARC     = (0, 191, 255)      # Deep sky blue speedometer
CLR_TEMP_ARC    = (0, 229, 204)      # Teal coolant
CLR_FUEL_ARC    = (255, 215, 0)      # Gold fuel
CLR_ARC_BG      = (42, 42, 42)       # Dim arc background
CLR_TEXT_MAIN   = (232, 232, 232)
CLR_TEXT_DIM    = (96, 96, 96)
CLR_RED_ZONE    = (255, 16, 16)
CLR_WARN_YELLOW = (255, 170, 0)
CLR_WARN_RED    = (255, 32, 32)
CLR_GEAR_GREEN  = (0, 255, 127)
CLR_DIVIDER     = (40, 40, 40)
CLR_TELL_BG     = (30, 30, 30)
CLR_TELL_BORDER = (48, 48, 48)

# ---- Gauge geometry ----
LARGE_ARC_D   = 290
SMALL_ARC_D   = 140
ARC_WIDTH      = 18
ARC_START_DEG  = 135   # 7 o'clock
ARC_SWEEP_DEG  = 270   # Full sweep

# ---- Gauge ranges ----
RPM_MIN, RPM_MAX = 0, 8000
RPM_REDZONE      = 6000
SPD_MIN, SPD_MAX = 0, 260
TEMP_MIN, TEMP_MAX = 40, 130
TEMP_WARN        = 110
FUEL_MIN, FUEL_MAX = 0, 100
FUEL_WARN        = 10
