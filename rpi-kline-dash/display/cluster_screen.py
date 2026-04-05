"""Main gauge cluster screen layout and rendering.

Matches the original LVGL-based design:
  - Tachometer (left, orange arc, 0-8000 RPM, red zone 6000+)
  - Speedometer (right, blue arc, 0-260 km/h, gear indicator)
  - Coolant temperature (bottom-left, teal arc, 40-130C)
  - Fuel level (bottom-right, gold arc, 0-100%)
  - Telltale row (top center: ENG, OIL, BAT, ABS, ESP)
  - Vertical divider, trip info at bottom
"""

import pygame

from config import (
    SCREEN_W, SCREEN_H,
    LARGE_ARC_D, SMALL_ARC_D,
    CLR_BG, CLR_DIVIDER,
    CLR_RPM_ARC, CLR_SPD_ARC, CLR_TEMP_ARC, CLR_FUEL_ARC,
    CLR_RED_ZONE, CLR_WARN_YELLOW, CLR_WARN_RED,
    CLR_TEXT_MAIN, CLR_TEXT_DIM, CLR_GEAR_GREEN,
    RPM_MIN, RPM_MAX, RPM_REDZONE,
    SPD_MIN, SPD_MAX,
    TEMP_MIN, TEMP_MAX, TEMP_WARN,
    FUEL_MIN, FUEL_MAX, FUEL_WARN,
)
from .gauges import draw_gauge_arc, draw_redzone, draw_telltale


class ClusterScreen:
    """Renders the full gauge cluster layout."""

    def __init__(self):
        # Fonts (DejaVu is available on Raspberry Pi OS)
        self.font_huge  = pygame.font.SysFont("DejaVu Sans", 52, bold=True)
        self.font_large = pygame.font.SysFont("DejaVu Sans", 36, bold=True)
        self.font_med   = pygame.font.SysFont("DejaVu Sans", 18)
        self.font_small = pygame.font.SysFont("DejaVu Sans", 14)
        self.font_gear  = pygame.font.SysFont("DejaVu Sans", 34, bold=True)
        self.font_temp  = pygame.font.SysFont("DejaVu Sans", 18, bold=True)

        # Pre-compute gauge centers
        self.rpm_center  = (SCREEN_W // 4, SCREEN_H // 2 - 20)
        self.spd_center  = (3 * SCREEN_W // 4, SCREEN_H // 2 - 20)
        self.temp_center = (40 + SMALL_ARC_D // 2,
                           SCREEN_H - SMALL_ARC_D // 2 - 50)
        self.fuel_center = (SCREEN_W - 40 - SMALL_ARC_D // 2,
                           SCREEN_H - SMALL_ARC_D // 2 - 50)

    def draw(self, surface, data: dict):
        """Render the full cluster given a data snapshot dict."""
        surface.fill(CLR_BG)

        # Vertical center divider
        pygame.draw.line(surface, CLR_DIVIDER,
                        (SCREEN_W // 2, 60), (SCREEN_W // 2, 520), 1)

        self._draw_tachometer(surface, data)
        self._draw_speedometer(surface, data)
        self._draw_coolant(surface, data)
        self._draw_fuel(surface, data)
        self._draw_telltales(surface, data)
        self._draw_status_bar(surface, data)

    # ---- Tachometer ----

    def _draw_tachometer(self, surface, data):
        rpm = data["rpm"]

        # Dynamic arc color
        if rpm >= 6000:
            arc_color = CLR_RED_ZONE
        elif rpm >= 5000:
            arc_color = (255, 140, 0)
        else:
            arc_color = CLR_RPM_ARC

        draw_gauge_arc(surface, self.rpm_center, LARGE_ARC_D // 2,
                       rpm, RPM_MIN, RPM_MAX, arc_color)
        draw_redzone(surface, self.rpm_center, LARGE_ARC_D // 2,
                    RPM_REDZONE, RPM_MAX, CLR_RED_ZONE)

        # Value (displayed as hundreds)
        self._center_text(surface, str(rpm // 100), self.font_huge,
                         CLR_TEXT_MAIN,
                         (self.rpm_center[0], self.rpm_center[1] - 4))
        self._center_text(surface, "RPM x100", self.font_small,
                         CLR_TEXT_DIM,
                         (self.rpm_center[0], self.rpm_center[1] + 32))

    # ---- Speedometer ----

    def _draw_speedometer(self, surface, data):
        speed = data["speed"]

        draw_gauge_arc(surface, self.spd_center, LARGE_ARC_D // 2,
                       speed, SPD_MIN, SPD_MAX, CLR_SPD_ARC)

        self._center_text(surface, str(speed), self.font_huge,
                         CLR_TEXT_MAIN,
                         (self.spd_center[0], self.spd_center[1] - 4))
        self._center_text(surface, "km/h", self.font_small,
                         CLR_TEXT_DIM,
                         (self.spd_center[0], self.spd_center[1] + 32))

        # Gear indicator
        gear = data["gear"]
        gear_str = "N" if gear == 0 else ("R" if gear == 7 else str(gear))
        self._center_text(surface, gear_str, self.font_gear,
                         CLR_GEAR_GREEN,
                         (self.spd_center[0], self.spd_center[1] + 66))

    # ---- Coolant Temperature ----

    def _draw_coolant(self, surface, data):
        coolant = data["coolant"]
        color = CLR_RED_ZONE if coolant >= TEMP_WARN else CLR_TEMP_ARC

        draw_gauge_arc(surface, self.temp_center, SMALL_ARC_D // 2,
                       coolant, TEMP_MIN, TEMP_MAX, color)

        # Title
        title = self.font_small.render("COOLANT", True, CLR_TEXT_DIM)
        surface.blit(title, (self.temp_center[0] - 28,
                             self.temp_center[1] - SMALL_ARC_D // 2 - 22))

        # Value
        self._center_text(surface, f"{int(coolant)}\u00b0C", self.font_temp,
                         CLR_TEXT_MAIN, self.temp_center)

    # ---- Fuel Gauge ----

    def _draw_fuel(self, surface, data):
        fuel = data["fuel_pct"]
        color = CLR_WARN_RED if fuel <= FUEL_WARN else CLR_FUEL_ARC

        draw_gauge_arc(surface, self.fuel_center, SMALL_ARC_D // 2,
                       fuel, FUEL_MIN, FUEL_MAX, color)

        title = self.font_small.render("FUEL", True, CLR_TEXT_DIM)
        surface.blit(title, (self.fuel_center[0] - 14,
                             self.fuel_center[1] - SMALL_ARC_D // 2 - 22))

        self._center_text(surface, f"{fuel}%", self.font_temp,
                         CLR_TEXT_MAIN, self.fuel_center)

    # ---- Telltales ----

    def _draw_telltales(self, surface, data):
        tell_y = 14
        tell_gap = 66
        tell_start = SCREEN_W // 2 - (5 * tell_gap) // 2

        tells = [
            ("ENG", data["check_engine"], CLR_WARN_YELLOW),
            ("OIL", data["oil_pressure"], CLR_WARN_RED),
            ("BAT", data["battery_warn"], CLR_WARN_RED),
            ("ABS", data["abs_warn"],     CLR_WARN_YELLOW),
            ("ESP", data["esp_warn"],     CLR_WARN_YELLOW),
        ]
        for i, (label, active, color) in enumerate(tells):
            draw_telltale(surface, tell_start + i * tell_gap, tell_y,
                         label, active, color, self.font_small)

    # ---- Status Bar ----

    def _draw_status_bar(self, surface, data):
        if data.get("connected"):
            text = "TRIP  ---.- km"
        else:
            text = "DEMO MODE \u2014 No ECU"

        self._center_text(surface, text, self.font_small,
                         CLR_TEXT_DIM, (SCREEN_W // 2, SCREEN_H - 20))

    # ---- Helper ----

    def _center_text(self, surface, text, font, color, center):
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=center)
        surface.blit(rendered, rect)
