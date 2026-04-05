#!/usr/bin/env python3
"""BMW MS41 Gauge Cluster — Raspberry Pi Zero 2 W.

Single-board architecture:
  Pi Zero 2 W UART (GPIO14/15) -> L9637D -> K-Line -> BMW MS41 ECU
  Pi Zero 2 W HDMI -> Waveshare 7" 1024x600 display

Reads all 30 live parameters from the MS41 ECU via DS2 protocol at 10 Hz,
renders an automotive gauge cluster via pygame.
"""

import os
import sys
import time
import threading

# Use KMS/DRM backend on Pi (no X11 needed)
if "DISPLAY" not in os.environ:
    os.environ.setdefault("SDL_VIDEODRIVER", "kmsdrm")

import pygame

from config import SCREEN_W, SCREEN_H, FPS, FULLSCREEN, POLL_INTERVAL_S
from config import INIT_DELAY_S, RECONNECT_INTERVAL_S
from kline.kline_uart import KLineUART
from kline.ms41 import MS41, MS41LiveData
from display.e36_cluster_screen import E36ClusterScreen


class App:
    """Main application: K-Line polling thread + pygame render loop."""

    def __init__(self):
        self._lock = threading.Lock()
        self._live = MS41LiveData()
        self._connected = False
        self._running = True
        self._poll_count = 0
        self._error_count = 0

        # Display state for gauges (snapshot for render thread)
        self._display_data = self._default_data()

    @staticmethod
    def _default_data():
        return {
            "rpm": 0, "speed": 0, "coolant": 20.0, "throttle": 0.0,
            "battery": 12.0, "oil_temp": 20.0, "fuel_pct": 75,
            "gear": 0,
            "check_engine": False, "oil_pressure": False,
            "battery_warn": False, "abs_warn": False, "esp_warn": False,
            "connected": False,
        }

    def _snapshot(self) -> dict:
        """Build display data dict from current live data (thread-safe)."""
        with self._lock:
            d = self._live
            speed = d.vehicle_speed
            rpm = d.rpm

            # Estimate gear from speed/RPM (M52 with 5-speed Getrag)
            gear = 0
            if rpm > 500 and speed > 5:
                ratio = speed / (rpm / 1000.0)
                if ratio < 8:
                    gear = 1
                elif ratio < 13:
                    gear = 2
                elif ratio < 18:
                    gear = 3
                elif ratio < 24:
                    gear = 4
                else:
                    gear = 5

            return {
                "rpm": rpm,
                "speed": speed,
                "coolant": d.coolant_temp,
                "throttle": d.throttle_pos,
                "battery": d.battery_voltage,
                "oil_temp": d.oil_temp,
                "fuel_pct": 75,  # MS41 has no fuel level; placeholder
                "gear": gear,
                "check_engine": False,
                "oil_pressure": False,
                "battery_warn": d.battery_voltage < 11.5 and d.battery_voltage > 0,
                "abs_warn": False,
                "esp_warn": False,
                "connected": self._connected,
            }

    # ---- K-Line Polling Thread ----

    def _kline_thread(self):
        """Background thread: connect to ECU and poll live data at 10 Hz."""
        kline = KLineUART()
        ecu = MS41(kline)

        print("[KLINE] Waiting before init...")
        time.sleep(INIT_DELAY_S)

        while self._running:
            # Connect / reconnect
            if not ecu.connected:
                print("[KLINE] Attempting ECU connection (fast init)...")
                kline.open()
                if ecu.connect(use_slow_init=False):
                    print("[KLINE] MS41 connected!")
                    with self._lock:
                        self._connected = True
                        self._error_count = 0
                else:
                    # Try slow init as fallback
                    print("[KLINE] Fast init failed, trying slow init...")
                    if ecu.connect(use_slow_init=True):
                        print("[KLINE] MS41 connected (slow init)!")
                        with self._lock:
                            self._connected = True
                            self._error_count = 0
                    else:
                        print(f"[KLINE] ECU not responding. Retry in {RECONNECT_INTERVAL_S}s")
                        with self._lock:
                            self._connected = False
                        kline.close()
                        time.sleep(RECONNECT_INTERVAL_S)
                        continue

            # Poll live data
            data = ecu.read_live_data()
            if data:
                with self._lock:
                    self._live = data
                    self._poll_count += 1
                    self._error_count = 0
            else:
                with self._lock:
                    self._error_count += 1
                    if self._error_count > 10:
                        print("[KLINE] Lost ECU connection")
                        self._connected = False
                        ecu.connected = False
                        self._error_count = 0

            time.sleep(POLL_INTERVAL_S)

        kline.close()

    # ---- Demo Mode ----

    def _demo_update(self):
        """Animate gauges when no ECU is connected (for testing)."""
        if not hasattr(self, "_demo_rpm"):
            self._demo_rpm = 800
            self._demo_dir = 1
            self._demo_coolant = 20.0
            self._demo_warm = False

        self._demo_rpm += self._demo_dir * 120
        if self._demo_rpm >= 7200:
            self._demo_dir = -1
        if self._demo_rpm <= 700:
            self._demo_dir = 1

        speed = max(0, min(260, int((self._demo_rpm - 700) / 26)))

        if not self._demo_warm and self._demo_coolant < 90:
            self._demo_coolant += 0.5
        else:
            self._demo_warm = True
            self._demo_coolant = 88 + self._demo_rpm / 2000.0

        gear = 0
        if speed >= 170:
            gear = 6
        elif speed >= 130:
            gear = 5
        elif speed >= 90:
            gear = 4
        elif speed >= 60:
            gear = 3
        elif speed >= 30:
            gear = 2
        elif speed >= 10:
            gear = 1

        fuel = max(0, 75 - int(time.time() % 200) // 3)

        self._display_data = {
            "rpm": self._demo_rpm, "speed": speed,
            "coolant": self._demo_coolant, "throttle": self._demo_rpm / 80.0,
            "battery": 13.8, "oil_temp": self._demo_coolant - 5,
            "fuel_pct": fuel, "gear": gear,
            "check_engine": False, "oil_pressure": False,
            "battery_warn": fuel < 15,
            "abs_warn": False, "esp_warn": False,
            "connected": False,
        }

    # ---- Main Loop ----

    def run(self):
        pygame.init()

        flags = pygame.FULLSCREEN if FULLSCREEN else 0
        screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags)
        pygame.display.set_caption("BMW MS41 Gauge Cluster")
        if FULLSCREEN:
            pygame.mouse.set_visible(False)

        clock = pygame.time.Clock()
        cluster = E36ClusterScreen()

        # Start K-Line polling in background thread
        kline_t = threading.Thread(target=self._kline_thread, daemon=True)
        kline_t.start()

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        self._running = False

            # Use real data if connected, otherwise demo
            with self._lock:
                connected = self._connected

            if connected:
                self._display_data = self._snapshot()
            else:
                self._demo_update()

            cluster.draw(screen, self._display_data)
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    app = App()
    app.run()
