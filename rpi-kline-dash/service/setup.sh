#!/bin/bash
# ============================================================
# Setup script for BMW MS41 Gauge Cluster
# Raspberry Pi Zero 2 W — single-board K-Line + display
#
# Run as:  sudo bash setup.sh
# ============================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "========================================"
echo " BMW MS41 Gauge Cluster — Pi Setup"
echo "========================================"
echo " Project dir: ${SCRIPT_DIR}"
echo ""

# ---- 1. System packages ----
echo "[1/6] Updating system and installing packages..."
apt-get update -qq
apt-get install -y \
    python3 python3-pip python3-venv \
    python3-pygame python3-serial python3-rpi.gpio \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    fonts-dejavu-core

# ---- 2. Python packages (in case system packages are old) ----
echo "[2/6] Installing Python packages..."
pip3 install --break-system-packages pyserial RPi.GPIO 2>/dev/null \
    || pip3 install pyserial RPi.GPIO

# ---- 3. Disable serial console (free up UART for K-Line) ----
echo "[3/6] Configuring UART for K-Line..."

# Remove console=serial0 from kernel cmdline
if grep -q "console=serial0" /boot/cmdline.txt 2>/dev/null; then
    sed -i 's/console=serial0,[0-9]* //g' /boot/cmdline.txt
    echo "  Removed serial console from cmdline.txt"
fi
if grep -q "console=ttyAMA0" /boot/cmdline.txt 2>/dev/null; then
    sed -i 's/console=ttyAMA0,[0-9]* //g' /boot/cmdline.txt
    echo "  Removed ttyAMA0 console from cmdline.txt"
fi

# Enable hardware UART
if ! grep -q "^enable_uart=1" /boot/config.txt; then
    echo "enable_uart=1" >> /boot/config.txt
    echo "  Enabled UART in config.txt"
fi

# On Pi Zero 2 W, swap miniUART and PL011 so ttyAMA0 is the full UART
# (Bluetooth gets miniUART instead)
if ! grep -q "^dtoverlay=miniuart-bt" /boot/config.txt; then
    echo "dtoverlay=miniuart-bt" >> /boot/config.txt
    echo "  Swapped Bluetooth to miniUART (PL011 -> ttyAMA0 for K-Line)"
fi

# Disable serial login services
systemctl disable serial-getty@ttyAMA0.service 2>/dev/null || true
systemctl disable serial-getty@ttyS0.service 2>/dev/null || true
systemctl stop serial-getty@ttyAMA0.service 2>/dev/null || true
systemctl stop serial-getty@ttyS0.service 2>/dev/null || true
echo "  Disabled serial console services"

# ---- 4. Configure HDMI for Waveshare 7" 1024x600 ----
echo "[4/6] Configuring HDMI display..."

# Only add if not already present
if ! grep -q "# BMW Gauge Cluster Display" /boot/config.txt; then
    cat >> /boot/config.txt << 'HDMIEOF'

# BMW Gauge Cluster Display — Waveshare 7" 1024x600
hdmi_group=2
hdmi_mode=87
hdmi_cvt=1024 600 60 3 0 0 0
hdmi_drive=2
hdmi_force_hotplug=1
disable_overscan=1
HDMIEOF
    echo "  Added HDMI config for 1024x600@60Hz"
else
    echo "  HDMI config already present"
fi

# ---- 5. Install systemd service ----
echo "[5/6] Installing systemd auto-start service..."

cat > /etc/systemd/system/gauge-cluster.service << SVCEOF
[Unit]
Description=BMW MS41 Gauge Cluster (K-Line + Display)
After=multi-user.target
Wants=multi-user.target

[Service]
Type=simple
User=root
Environment=SDL_VIDEODRIVER=kmsdrm
WorkingDirectory=${SCRIPT_DIR}
ExecStart=/usr/bin/python3 ${SCRIPT_DIR}/main.py
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SVCEOF

systemctl daemon-reload
systemctl enable gauge-cluster.service
echo "  Installed and enabled gauge-cluster.service"

# ---- 6. Add user to required groups ----
echo "[6/6] Setting permissions..."
usermod -a -G dialout,video,gpio pi 2>/dev/null || true
chmod +x "${SCRIPT_DIR}/main.py"

echo ""
echo "========================================"
echo " Setup Complete!"
echo "========================================"
echo ""
echo " Architecture:"
echo "   Pi GPIO14 (TX) -> L9637D TX -> K-Line -> BMW MS41 ECU"
echo "   Pi GPIO15 (RX) <- L9637D RX <- K-Line"
echo "   Pi HDMI        -> Waveshare 7\" 1024x600"
echo ""
echo " UART port:  /dev/ttyAMA0 (9600 baud, 8E1)"
echo " Display:    1024x600 via HDMI (kmsdrm backend)"
echo " Service:    gauge-cluster.service (auto-start at boot)"
echo ""
echo " Commands:"
echo "   Test now:    sudo python3 ${SCRIPT_DIR}/main.py"
echo "   Start:       sudo systemctl start gauge-cluster"
echo "   Stop:        sudo systemctl stop gauge-cluster"
echo "   Logs:        journalctl -u gauge-cluster -f"
echo ""
echo " *** REBOOT REQUIRED for UART and display changes! ***"
echo " Run:  sudo reboot"
