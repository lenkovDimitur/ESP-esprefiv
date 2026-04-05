# BMW MS41 K-Line Gauge Cluster — Raspberry Pi Zero 2 W

Automotive gauge cluster for BMW E36/E39 vehicles with Siemens MS41 ECU.
Reads live engine data via K-Line (DS2 protocol) and renders a real-time
dashboard on a 7" Waveshare 1024x600 HDMI display.

## Architecture

Single-board design — Raspberry Pi Zero 2 W handles both K-Line
communication and display rendering:

```
  Pi Zero 2 W GPIO14 (TX) ──> L9637D TX ──> K-Line ──> BMW MS41 ECU
  Pi Zero 2 W GPIO15 (RX) <── L9637D RX <── K-Line
  Pi Zero 2 W HDMI         ──> Waveshare 7" 1024x600 display
```

**Protocol:** BMW DS2 over ISO 9141 K-Line, 9600 baud 8E1
**Polling rate:** 10 Hz (100ms per request/response cycle)
**Display:** 1024x600 @ 30 FPS via pygame (kmsdrm backend, no X11)

## Wiring

### OBD-II Connector

```
Pin 4/5  (GND)    ──> Common ground (Pi + L9637D)
Pin 7    (K-Line) ──> L9637D K pin
Pin 16   (+12V)   ──> 12V-to-5V buck converter ──> Pi 5V + L9637D VCC
```

### L9637D K-Line Transceiver

```
┌───────────┐
│  L9637D   │
│           │
│ VCC ← 5V │  (from buck converter)
│ GND ← GND│  (common ground)
│ EN  ← 5V │  (always enabled)
│ TX  ← Pi GPIO14 (UART TX)
│ RX  → Pi GPIO15 (UART RX)
│ K   ↔ OBD Pin 7 (K-Line)
└───────────┘

Bypass cap: 100nF ceramic on VCC to GND
```

### Full System

```
┌─────────────────────────────────────────────────────────┐
│                   OBD-II Connector                       │
│                                                         │
│  Pin 16 (+12V) ─────┬──> 12V→5V Buck (LM2596)         │
│                      │        │                         │
│                     [10kΩ]    ├──> L9637D VCC (5V)      │
│                      │        └──> Pi 5V (via microUSB) │
│  Pin 7 (K-Line) ────┴──> L9637D K pin                  │
│                                                         │
│  Pin 4/5 (GND) ─────────> Common GND                   │
└─────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌───────────┐
│ Pi Zero 2 W      │         │  L9637D   │
│                  │         │           │
│ GPIO14 (TX) ─────┼────────>│ TX        │
│ GPIO15 (RX) <────┼─────────│ RX        │
│ GND ─────────────┼────────>│ GND       │
│                  │         │ VCC ← 5V  │
│ HDMI ────────────┼──┐      │ K ↔ K-Line│
└──────────────────┘  │      └───────────┘
                      │
              ┌───────┴────────┐
              │ Waveshare 7"   │
              │ 1024x600 HDMI  │
              └────────────────┘
```

## Project Structure

```
rpi-kline-dash/
├── main.py                    # Entry point: K-Line polling + display loop
├── config.py                  # All configuration (UART, display, colors, etc.)
├── requirements.txt           # Python dependencies
│
├── kline/                     # K-Line / DS2 protocol stack
│   ├── ds2_protocol.py        # DS2 frame building, checksum, validation
│   ├── kline_uart.py          # UART transport via L9637D (fast/slow init)
│   └── ms41.py                # MS41 ECU commands, parsers, DTC table
│
├── display/                   # Gauge cluster UI (pygame)
│   ├── gauges.py              # Arc drawing, telltale primitives
│   └── cluster_screen.py      # Full cluster layout and rendering
│
└── service/                   # Deployment
    ├── setup.sh               # Pi configuration script (UART, HDMI, deps)
    └── gauge-cluster.service  # systemd service for auto-start
```

## Live Data Parameters (30 PIDs from Analog Block 3)

| Parameter | Unit | Range |
|-----------|------|-------|
| Engine Speed (RPM) | RPM | 0-8000 |
| Coolant Temperature | C | -48 to 143 |
| Intake Air Temperature | C | -48 to 143 |
| Throttle Position | % | 0-100 |
| Battery Voltage | V | 0-25.5 |
| Engine Load | mg/str | 0-1350 |
| Lambda Integrator B1/B2 | % | -100 to 100 |
| Short-Term Fuel Trim B1/B2 | % | -100 to 100 |
| Oil Temperature | C | -48 to 155 |
| Vehicle Speed | km/h | 0-255 |
| Ignition Timing | deg BTDC | -22.5 to 73 |
| VANOS Position | deg | 0-95 |
| O2 Sensor Voltages (4x) | V | 0-5.0 |
| Idle Valve Position | % | 0-100 |
| Long-Term Fuel Trim B1/B2 | % | -100 to 100 |
| Catalyst Temps B1/B2 | C | 0-1200 |
| MAP Sensor | bar | 0-2.5 |
| Injection Time | ms | 0-65 |
| Knock Retard Cyl 1-3/4-6 | deg | 0-95 |

## Setup

### Prerequisites

- Raspberry Pi Zero 2 W with Raspberry Pi OS (Lite recommended)
- Waveshare 7" 1024x600 HDMI display
- L9637D K-Line transceiver board
- 12V to 5V buck converter (LM2596 or similar)
- OBD-II connector/cable

### Installation

```bash
# Clone to Pi
git clone <this-repo> ~/rpi-kline-dash
cd ~/rpi-kline-dash

# Run setup (configures UART, HDMI, installs deps, enables service)
sudo bash service/setup.sh

# Reboot for UART/HDMI changes
sudo reboot
```

### K-Line UART Setup (what setup.sh does)

1. Disables serial console on `/dev/ttyAMA0`
2. Enables hardware UART (`enable_uart=1` in config.txt)
3. Swaps Bluetooth to miniUART (`dtoverlay=miniuart-bt`) so the full
   PL011 UART is available on GPIO14/15 for K-Line
4. Configures HDMI for 1024x600@60Hz

### Running

```bash
# Manual test (with display connected)
sudo python3 main.py

# Via systemd (auto-starts on boot after setup)
sudo systemctl start gauge-cluster
sudo systemctl status gauge-cluster
journalctl -u gauge-cluster -f
```

The cluster starts in **demo mode** (animated gauges) if no ECU is
detected. It automatically switches to live data when the K-Line
connection is established.

## K-Line Communication

### Initialization

The MS41 ECU requires a wake-up sequence before communication:

- **Fast Init** (default): Pull TX LOW 25ms, HIGH 25ms, then UART at 9600 8E1
- **Slow Init** (fallback): Send address 0x12 at 5 baud, wait for sync/key bytes

The application tries fast init first, falls back to slow init automatically.

### DS2 Protocol

Request frame: `[Address=0x12] [Length] [Command...] [XOR Checksum]`
Response frame: `[Address=0x12] [Length] [ACK=0xA0] [Data...] [XOR Checksum]`

K-Line is half-duplex — every TX byte echoes on RX and must be discarded.

## Applicable Vehicles

| ECU | Engine | Vehicles |
|-----|--------|----------|
| MS41.0 | M52B20/B25/B28 | E36 320i/323i/328i |
| MS41.1 | M52B28/S52B32 | E36 328i, Z3 2.8, M3 |
| MS41.2 | M52B25/B28 | E39 523i/528i |
| MS41.3 | M52B28 | E36/E39 late models |
