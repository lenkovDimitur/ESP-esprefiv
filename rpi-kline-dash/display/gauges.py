"""Gauge rendering primitives for pygame — arcs, telltales, labels."""

import math
import pygame

from config import (
    CLR_ARC_BG, CLR_TEXT_DIM, CLR_TELL_BG, CLR_TELL_BORDER,
    ARC_WIDTH, ARC_START_DEG, ARC_SWEEP_DEG,
)


def draw_arc(surface, center, radius, width, start_deg, end_deg,
             color, segments=60):
    """Draw a thick arc from start_deg to end_deg (CW, 0=3 o'clock).

    Uses polygon rendering for smooth thick arcs (pygame has no native
    thick-arc support).
    """
    if abs(start_deg - end_deg) < 0.1:
        return

    # Convert LVGL-style CW angles to pygame CCW radians
    start_rad = math.radians(-end_deg)
    end_rad = math.radians(-start_deg)
    if end_rad < start_rad:
        end_rad += 2 * math.pi

    step = (end_rad - start_rad) / segments
    r_out = radius
    r_in = radius - width

    points_outer = []
    points_inner = []
    for i in range(segments + 1):
        angle = start_rad + i * step
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        points_outer.append((center[0] + r_out * cos_a,
                             center[1] - r_out * sin_a))
        points_inner.append((center[0] + r_in * cos_a,
                             center[1] - r_in * sin_a))

    points = points_outer + list(reversed(points_inner))
    if len(points) >= 3:
        pygame.draw.polygon(surface, color, points)


def value_to_angle(value, val_min, val_max):
    """Map a value within [val_min, val_max] to an arc angle."""
    frac = max(0.0, min(1.0, (value - val_min) / (val_max - val_min)))
    return ARC_START_DEG + frac * ARC_SWEEP_DEG


def draw_gauge_arc(surface, center, radius, value, val_min, val_max,
                   arc_color, width=ARC_WIDTH):
    """Draw a complete gauge: background arc + colored indicator."""
    # Background arc (full sweep)
    bg_end = ARC_START_DEG + ARC_SWEEP_DEG
    draw_arc(surface, center, radius, width, ARC_START_DEG, bg_end, CLR_ARC_BG)

    # Indicator arc (proportional to value)
    end_angle = value_to_angle(value, val_min, val_max)
    if end_angle > ARC_START_DEG + 0.5:
        draw_arc(surface, center, radius, width,
                 ARC_START_DEG, end_angle, arc_color)


def draw_redzone(surface, center, radius, zone_start, val_max,
                 color, width=ARC_WIDTH, alpha=128):
    """Draw a semi-transparent red zone overlay on a gauge arc."""
    start_angle = value_to_angle(zone_start, 0, val_max)
    end_angle = ARC_START_DEG + ARC_SWEEP_DEG

    # Temp surface for alpha blending
    size = radius * 2 + 4
    tmp = pygame.Surface((size, size), pygame.SRCALPHA)
    tmp_center = (radius + 2, radius + 2)
    draw_arc(tmp, tmp_center, radius, width,
             start_angle, end_angle, (*color, alpha))
    surface.blit(tmp, (center[0] - radius - 2, center[1] - radius - 2))


def draw_telltale(surface, x, y, label, active, active_color, font):
    """Draw a telltale indicator box (ENG, OIL, BAT, ABS, ESP)."""
    w, h = 56, 36
    rect = pygame.Rect(x, y, w, h)

    if active:
        bg = tuple(min(255, c1 // 4 + c2) for c1, c2 in
                   zip(active_color, CLR_TELL_BG))
        pygame.draw.rect(surface, bg, rect, border_radius=6)
        pygame.draw.rect(surface, active_color, rect, 1, border_radius=6)
        text_color = active_color
    else:
        pygame.draw.rect(surface, CLR_TELL_BG, rect, border_radius=6)
        pygame.draw.rect(surface, CLR_TELL_BORDER, rect, 1, border_radius=6)
        text_color = CLR_TEXT_DIM

    text_surf = font.render(label, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)
