"""BMW E36 authentic gauge cluster screen — hybrid Cairo + pygame.

Cairo pre-renders dial faces and needle sprites once at startup.
The per-frame loop is pure pygame blit + rotozoom: ~4.7ms per frame.

Drop-in replacement for ClusterScreen — same draw(surface, data) interface.
"""

import math
import pygame

from config import (
    SCREEN_W, SCREEN_H,
    CLR_BG, CLR_TEXT_DIM, CLR_WARN_YELLOW, CLR_WARN_RED,
    E36_TACH_CENTER, E36_TACH_RADIUS,
    E36_SPD_CENTER, E36_SPD_RADIUS,
    E36_COOL_CENTER, E36_COOL_RADIUS,
    E36_FUEL_CENTER, E36_FUEL_RADIUS,
    E36_ODO_CENTER,
    E36_RPM_MIN, E36_RPM_MAX,
    E36_SPD_MIN, E36_SPD_MAX,
    E36_COOL_MIN, E36_COOL_MAX,
    E36_FUEL_MIN, E36_FUEL_MAX,
    E36_SWEEP_START, E36_SWEEP_DEG,
    E36_CENTER_CAP, E36_CAP_RIM,
    E36_LG_CAP_RADIUS, E36_SM_CAP_RADIUS,
    E36_LCD_TEXT, E36_NEEDLE,
    CLR_TELL_BG, CLR_TELL_BORDER,
)

from .cairo_renderer import (
    render_tach_face, render_speed_face,
    render_coolant_face, render_fuel_face,
    render_large_needle, render_small_needle,
)
from .needle_cache import NeedleCache

PAD = 10  # Must match cairo_renderer.PAD


def _value_to_angle(value, val_min, val_max):
    """Map gauge value to rotation angle (degrees, for rotozoom)."""
    frac = max(0.0, min(1.0, (value - val_min) / (val_max - val_min)))
    return E36_SWEEP_START - frac * E36_SWEEP_DEG


def _clamp(val, lo, hi):
    return max(lo, min(hi, val))


class E36ClusterScreen:
    """BMW E36 authentic gauge cluster with needle gauges.

    Pre-renders all static elements at init time using Cairo.
    Per-frame: blit cached surfaces + rotozoom needles.
    """

    def __init__(self):
        # ── Pre-render dial faces (Cairo → pygame Surface) ──
        self._tach_face = render_tach_face()
        self._speed_face = render_speed_face()
        self._cool_face = render_coolant_face()
        self._fuel_face = render_fuel_face()

        # ── Pre-render needle master sprites ──
        needle_lg = render_large_needle()
        needle_sm = render_small_needle()

        # ── Needle caches (one per gauge) ──
        self._needle_tach = NeedleCache(needle_lg)
        self._needle_spd = NeedleCache(needle_lg)
        self._needle_cool = NeedleCache(needle_sm)
        self._needle_fuel = NeedleCache(needle_sm)

        # ── Blit positions for dial faces ──
        self._tach_pos = (E36_TACH_CENTER[0] - E36_TACH_RADIUS - PAD,
                          E36_TACH_CENTER[1] - E36_TACH_RADIUS - PAD)
        self._speed_pos = (E36_SPD_CENTER[0] - E36_SPD_RADIUS - PAD,
                           E36_SPD_CENTER[1] - E36_SPD_RADIUS - PAD)
        self._cool_pos = (E36_COOL_CENTER[0] - E36_COOL_RADIUS - PAD,
                          E36_COOL_CENTER[1] - E36_COOL_RADIUS - PAD)
        self._fuel_pos = (E36_FUEL_CENTER[0] - E36_FUEL_RADIUS - PAD,
                          E36_FUEL_CENTER[1] - E36_FUEL_RADIUS - PAD)

        # ── Pre-render center cap surfaces ──
        self._cap_lg = self._make_center_cap(E36_LG_CAP_RADIUS)
        self._cap_sm = self._make_center_cap(E36_SM_CAP_RADIUS)

        # ── Fonts ──
        self._font_digital = pygame.font.SysFont("DejaVu Sans", 28, bold=True)
        self._font_label = pygame.font.SysFont("DejaVu Sans", 11)
        self._font_gear = pygame.font.SysFont("DejaVu Sans", 22, bold=True)
        self._font_value = pygame.font.SysFont("DejaVu Sans", 14, bold=True)
        self._font_tell = pygame.font.SysFont("DejaVu Sans", 12, bold=True)
        self._font_odo = pygame.font.SysFont("Courier New", 16)
        self._font_status = pygame.font.SysFont("DejaVu Sans", 13)
        self._font_title = pygame.font.SysFont("DejaVu Sans", 12, bold=True)

    @staticmethod
    def _make_center_cap(radius):
        """Pre-render a needle pivot center cap as a small Surface."""
        size = (radius + 3) * 2
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)

        # Rim
        pygame.draw.circle(surf, E36_CAP_RIM, center, radius + 2)
        # Cap
        pygame.draw.circle(surf, E36_CENTER_CAP, center, radius)
        # Subtle highlight
        hl_pos = (center[0] - radius // 4, center[1] - radius // 4)
        pygame.draw.circle(surf, (255, 255, 255, 20), hl_pos, radius // 3)

        return surf

    def draw(self, surface, data):
        """Render the complete E36 gauge cluster.

        Args:
            surface: pygame display surface (1024x600)
            data: dict with keys: rpm, speed, coolant, fuel_pct, gear,
                  check_engine, oil_pressure, battery_warn, abs_warn,
                  esp_warn, connected
        """
        # 1. Background
        surface.fill(CLR_BG)

        # 2. Blit pre-rendered dial faces
        surface.blit(self._tach_face, self._tach_pos)
        surface.blit(self._speed_face, self._speed_pos)
        surface.blit(self._cool_face, self._cool_pos)
        surface.blit(self._fuel_face, self._fuel_pos)

        # 3. Rotate and blit needles
        self._draw_needle(surface, data, "tach")
        self._draw_needle(surface, data, "speed")
        self._draw_needle(surface, data, "coolant")
        self._draw_needle(surface, data, "fuel")

        # 4. Center caps
        self._blit_cap(surface, E36_TACH_CENTER, self._cap_lg)
        self._blit_cap(surface, E36_SPD_CENTER, self._cap_lg)
        self._blit_cap(surface, E36_COOL_CENTER, self._cap_sm)
        self._blit_cap(surface, E36_FUEL_CENTER, self._cap_sm)

        # 5. Digital readouts
        self._draw_tach_readout(surface, data)
        self._draw_speed_readout(surface, data)
        self._draw_small_readouts(surface, data)

        # 6. Odometer LCD
        self._draw_odometer(surface, data)

        # 7. Telltales
        self._draw_telltales(surface, data)

        # 8. Status bar
        self._draw_status_bar(surface, data)

    # ── Needle drawing ───────────────────────────────────────

    def _draw_needle(self, surface, data, gauge_type):
        if gauge_type == "tach":
            rpm = _clamp(data["rpm"], E36_RPM_MIN, E36_RPM_MAX)
            angle = _value_to_angle(rpm, E36_RPM_MIN, E36_RPM_MAX)
            surf, rect = self._needle_tach.get_rotated(angle, E36_TACH_CENTER)
        elif gauge_type == "speed":
            spd = _clamp(data["speed"], E36_SPD_MIN, E36_SPD_MAX)
            angle = _value_to_angle(spd, E36_SPD_MIN, E36_SPD_MAX)
            surf, rect = self._needle_spd.get_rotated(angle, E36_SPD_CENTER)
        elif gauge_type == "coolant":
            # Map ECU temp (40-130C) to abstract 0-100 range
            raw = _clamp(data["coolant"], 40.0, 130.0)
            norm = (raw - 40.0) / 90.0 * 100.0
            angle = _value_to_angle(norm, E36_COOL_MIN, E36_COOL_MAX)
            surf, rect = self._needle_cool.get_rotated(angle, E36_COOL_CENTER)
        elif gauge_type == "fuel":
            fuel = _clamp(data["fuel_pct"], E36_FUEL_MIN, E36_FUEL_MAX)
            angle = _value_to_angle(fuel, E36_FUEL_MIN, E36_FUEL_MAX)
            surf, rect = self._needle_fuel.get_rotated(angle, E36_FUEL_CENTER)

        surface.blit(surf, rect)

    def _blit_cap(self, surface, center, cap_surf):
        rect = cap_surf.get_rect(center=center)
        surface.blit(cap_surf, rect)

    # ── Digital readouts ─────────────────────────────────────

    def _draw_tach_readout(self, surface, data):
        cx, cy = E36_TACH_CENTER
        # RPM number
        rpm_text = self._font_digital.render(str(data["rpm"]), True, E36_LCD_TEXT)
        rect = rpm_text.get_rect(center=(cx, cy + 75))
        surface.blit(rpm_text, rect)
        # "RPM" label
        lbl = self._font_label.render("RPM", True, CLR_TEXT_DIM)
        rect = lbl.get_rect(center=(cx, cy + 95))
        surface.blit(lbl, rect)

    def _draw_speed_readout(self, surface, data):
        cx, cy = E36_SPD_CENTER
        # Speed number
        spd_text = self._font_digital.render(str(data["speed"]), True, E36_LCD_TEXT)
        rect = spd_text.get_rect(center=(cx, cy + 65))
        surface.blit(spd_text, rect)
        # Gear indicator
        gear = data["gear"]
        gear_str = "N" if gear == 0 else ("R" if gear == 7 else str(gear))
        gear_text = self._font_gear.render(gear_str, True,
                                           (0, 255, 127))  # CLR_GEAR_GREEN
        rect = gear_text.get_rect(center=(cx, cy + 92))
        surface.blit(gear_text, rect)

    def _draw_small_readouts(self, surface, data):
        # Coolant value
        cx, cy = E36_COOL_CENTER
        title = self._font_title.render("COOLANT", True, CLR_TEXT_DIM)
        surface.blit(title, title.get_rect(center=(cx, cy - E36_COOL_RADIUS - 12)))
        val = self._font_value.render(f"{int(data['coolant'])}\u00b0C", True,
                                      (232, 232, 232))
        surface.blit(val, val.get_rect(center=(cx, cy + 42)))

        # Fuel value
        cx, cy = E36_FUEL_CENTER
        title = self._font_title.render("FUEL", True, CLR_TEXT_DIM)
        surface.blit(title, title.get_rect(center=(cx, cy - E36_FUEL_RADIUS - 12)))
        val = self._font_value.render(f"{data['fuel_pct']}%", True,
                                      (232, 232, 232))
        surface.blit(val, val.get_rect(center=(cx, cy + 42)))

    # ── Odometer LCD ─────────────────────────────────────────

    def _draw_odometer(self, surface, data):
        cx, cy = E36_ODO_CENTER
        odo_w, odo_h = 144, 28

        # LCD background
        lcd_rect = pygame.Rect(cx - odo_w // 2, cy - odo_h // 2, odo_w, odo_h)
        pygame.draw.rect(surface, (10, 10, 10), lcd_rect, border_radius=4)
        pygame.draw.rect(surface, (42, 42, 42), lcd_rect, 1, border_radius=4)

        # LCD text
        odo_text = self._font_odo.render("123456 km", True, E36_LCD_TEXT)
        rect = odo_text.get_rect(center=(cx, cy))
        surface.blit(odo_text, rect)

    # ── Telltales ────────────────────────────────────────────

    def _draw_telltales(self, surface, data):
        tell_y = 18
        tell_gap = 60
        tell_start = SCREEN_W // 2 - (5 * tell_gap) // 2

        tells = [
            ("ENG", data["check_engine"], CLR_WARN_YELLOW),
            ("OIL", data["oil_pressure"], CLR_WARN_RED),
            ("BAT", data["battery_warn"], CLR_WARN_RED),
            ("ABS", data["abs_warn"],     CLR_WARN_YELLOW),
            ("ESP", data["esp_warn"],     CLR_WARN_YELLOW),
        ]

        for i, (label, active, color) in enumerate(tells):
            x = tell_start + i * tell_gap
            self._draw_single_telltale(surface, x, tell_y, label, active, color)

    def _draw_single_telltale(self, surface, x, y, label, active, active_color):
        w, h = 52, 30
        rect = pygame.Rect(x, y, w, h)

        if active:
            bg = tuple(min(255, c1 // 4 + c2)
                       for c1, c2 in zip(active_color, CLR_TELL_BG))
            pygame.draw.rect(surface, bg, rect, border_radius=6)
            pygame.draw.rect(surface, active_color, rect, 1, border_radius=6)
            text_color = active_color
        else:
            pygame.draw.rect(surface, CLR_TELL_BG, rect, border_radius=6)
            pygame.draw.rect(surface, CLR_TELL_BORDER, rect, 1, border_radius=6)
            text_color = CLR_TEXT_DIM

        text = self._font_tell.render(label, True, text_color)
        surface.blit(text, text.get_rect(center=rect.center))

    # ── Status Bar ───────────────────────────────────────────

    def _draw_status_bar(self, surface, data):
        if data.get("connected"):
            rpm = data["rpm"]
            spd = data["speed"]
            cool = int(data["coolant"])
            batt = data.get("battery", 0)
            text = f"BMW MS41 \u2014 {rpm} RPM  {spd} km/h  {cool}\u00b0C  {batt:.1f}V"
        else:
            text = "DEMO MODE \u2014 No ECU"

        rendered = self._font_status.render(text, True, CLR_TEXT_DIM)
        rect = rendered.get_rect(center=(SCREEN_W // 2, SCREEN_H - 16))
        surface.blit(rendered, rect)
