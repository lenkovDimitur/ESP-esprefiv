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

# ════════════════════════════════════════════════════════════
# BMW E36 Authentic Design — Hybrid Cairo + Pygame
# ════════════════════════════════════════════════════════════

# ---- E36 Color Palette ----
E36_FACE_BG      = (0, 0, 0)          # Pure black dial face
E36_TICK_MAJOR   = (255, 255, 255)    # White major ticks
E36_TICK_MINOR   = (180, 180, 180)    # Slightly dim minor ticks
E36_NUMBER       = (255, 255, 255)    # White dial numbers
E36_NEEDLE       = (255, 100, 20)     # BMW orange-red needle
E36_NEEDLE_TAIL  = (204, 80, 16)      # Darker counter-weight
E36_REDZONE_FILL = (200, 0, 0)        # Red zone sector fill
E36_REDZONE_TICK = (255, 0, 0)        # Red zone tick color
E36_COLD_ZONE    = (60, 120, 200)     # Coolant cold (blue)
E36_HOT_ZONE     = (200, 0, 0)        # Coolant hot (red)
E36_RESERVE      = (255, 140, 0)      # Fuel reserve (amber)
E36_CENTER_CAP   = (40, 40, 40)       # Needle pivot cap
E36_CAP_RIM      = (60, 60, 60)       # Cap rim highlight
E36_LCD_TEXT     = (140, 180, 140)    # Green-tinted LCD (odometer)
E36_RING         = (51, 51, 51)       # Outer ring of dial

# ---- E36 Gauge Layout (pixel positions on 1024x600) ----
E36_TACH_CENTER  = (270, 290)
E36_TACH_RADIUS  = 195
E36_SPD_CENTER   = (754, 290)
E36_SPD_RADIUS   = 195
E36_COOL_CENTER  = (115, 490)
E36_COOL_RADIUS  = 80
E36_FUEL_CENTER  = (909, 490)
E36_FUEL_RADIUS  = 80
E36_ODO_CENTER   = (512, 375)         # LCD odometer between dials

# ---- E36 Gauge Ranges ----
E36_RPM_MIN, E36_RPM_MAX = 0, 7000
E36_RPM_REDZONE  = 6500
E36_SPD_MIN, E36_SPD_MAX = 0, 240
E36_COOL_MIN, E36_COOL_MAX = 0, 100   # Abstract (ECU temp mapped to 0-100)
E36_COOL_COLD    = 25                  # Below 25% = cold zone
E36_COOL_HOT     = 75                  # Above 75% = hot zone
E36_FUEL_MIN, E36_FUEL_MAX = 0, 100
E36_FUEL_RESERVE = 15                  # Below 15% = reserve

# ---- E36 Sweep Angles (math convention: CCW from east) ----
E36_SWEEP_START  = 225                 # 7 o'clock
E36_SWEEP_DEG    = 270                 # Total sweep

# ---- E36 Needle Geometry ----
# Large (tach/speed): length from pivot to tip, tail counter-weight, widths
E36_NEEDLE_LG_LEN   = 160
E36_NEEDLE_LG_TAIL  = 28
E36_NEEDLE_LG_BASE  = 8
E36_NEEDLE_LG_TIP   = 2.5
# Small (coolant/fuel)
E36_NEEDLE_SM_LEN   = 55
E36_NEEDLE_SM_TAIL  = 14
E36_NEEDLE_SM_BASE  = 5
E36_NEEDLE_SM_TIP   = 2

# ---- E36 Tick Geometry ----
E36_LG_MAJOR_LEN    = 20              # Large gauge major tick length
E36_LG_MINOR_LEN    = 12
E36_LG_MAJOR_WIDTH  = 3.0
E36_LG_MINOR_WIDTH  = 1.5
E36_LG_NUMBER_INSET = 38              # How far inside the rim numbers sit
E36_SM_MAJOR_LEN    = 14              # Small gauge major tick length
E36_SM_MINOR_LEN    = 8
E36_SM_MAJOR_WIDTH  = 2.5
E36_SM_MINOR_WIDTH  = 1.0
E36_SM_NUMBER_INSET = 24

# ---- E36 Center Cap Sizes ----
E36_LG_CAP_RADIUS   = 12
E36_SM_CAP_RADIUS   = 7
