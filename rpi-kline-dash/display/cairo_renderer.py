"""Cairo-based one-time renderer for BMW E36 gauge dial faces and needle sprites.

All rendering happens once at startup. The output is pygame Surfaces that get
blitted every frame in the main render loop — zero per-frame vector math.

Cairo provides anti-aliased tick marks, numbers, arc sectors, and needle shapes
that look identical to the HTML Canvas preview.
"""

import math
import cairo
import numpy as np
import pygame

from config import (
    E36_FACE_BG, E36_TICK_MAJOR, E36_TICK_MINOR, E36_NUMBER,
    E36_NEEDLE, E36_NEEDLE_TAIL,
    E36_REDZONE_FILL, E36_REDZONE_TICK,
    E36_COLD_ZONE, E36_HOT_ZONE, E36_RESERVE,
    E36_RING,
    E36_SWEEP_START, E36_SWEEP_DEG,
    E36_RPM_MIN, E36_RPM_MAX, E36_RPM_REDZONE,
    E36_SPD_MIN, E36_SPD_MAX,
    E36_COOL_MIN, E36_COOL_MAX, E36_COOL_COLD, E36_COOL_HOT,
    E36_FUEL_MIN, E36_FUEL_MAX, E36_FUEL_RESERVE,
    E36_TACH_RADIUS, E36_SPD_RADIUS, E36_COOL_RADIUS, E36_FUEL_RADIUS,
    E36_LG_MAJOR_LEN, E36_LG_MINOR_LEN,
    E36_LG_MAJOR_WIDTH, E36_LG_MINOR_WIDTH, E36_LG_NUMBER_INSET,
    E36_SM_MAJOR_LEN, E36_SM_MINOR_LEN,
    E36_SM_MAJOR_WIDTH, E36_SM_MINOR_WIDTH, E36_SM_NUMBER_INSET,
    E36_NEEDLE_LG_LEN, E36_NEEDLE_LG_TAIL,
    E36_NEEDLE_LG_BASE, E36_NEEDLE_LG_TIP,
    E36_NEEDLE_SM_LEN, E36_NEEDLE_SM_TAIL,
    E36_NEEDLE_SM_BASE, E36_NEEDLE_SM_TIP,
    CLR_TEXT_DIM,
)

PAD = 10  # Padding around dial face surfaces


# ── Helpers ──────────────────────────────────────────────────

def _rgb(color):
    """Convert (R, G, B) 0-255 tuple to Cairo (r, g, b) 0-1."""
    return (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)


def _rgba(color, alpha):
    """Convert (R, G, B) 0-255 tuple + alpha to Cairo (r, g, b, a) 0-1."""
    return (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, alpha)


def _value_to_angle_rad(value, val_min, val_max):
    """Map a gauge value to an angle in radians (math convention: CCW from east)."""
    frac = max(0.0, min(1.0, (value - val_min) / (val_max - val_min)))
    deg = E36_SWEEP_START - frac * E36_SWEEP_DEG
    return math.radians(deg)


def _cairo_to_pygame(surface):
    """Convert a Cairo ImageSurface (ARGB32) to a pygame Surface with alpha.

    Cairo ARGB32 on little-endian stores pixels as BGRA in memory.
    We use numpy to swizzle BGRA -> RGBA for pygame.
    """
    surface.flush()
    w = surface.get_width()
    h = surface.get_height()
    stride = surface.get_stride()

    buf = surface.get_data()
    # Create numpy array from buffer (BGRA byte order on little-endian)
    arr = np.frombuffer(buf, dtype=np.uint8).reshape((h, stride // 4, 4)).copy()
    arr = arr[:, :w, :]  # Trim stride padding

    # Swizzle BGRA -> RGBA
    arr[:, :, [0, 2]] = arr[:, :, [2, 0]]

    pg_surf = pygame.image.frombuffer(arr.tobytes(), (w, h), "RGBA")
    return pg_surf.convert_alpha()


# ── Arc Sector Drawing ───────────────────────────────────────

def _draw_arc_sector(ctx, cx, cy, r_outer, r_inner,
                     val_start, val_end, val_min, val_max, color_rgba):
    """Draw a filled annular sector between two gauge values."""
    a_start = _value_to_angle_rad(val_start, val_min, val_max)
    a_end = _value_to_angle_rad(val_end, val_min, val_max)

    # Cairo arcs go CW, our angles go CCW, so negate
    ctx.new_path()
    ctx.arc(cx, cy, r_outer, -a_start, -a_end)
    ctx.arc_negative(cx, cy, r_inner, -a_end, -a_start)
    ctx.close_path()
    ctx.set_source_rgba(*color_rgba)
    ctx.fill()


# ── Tick and Number Drawing ──────────────────────────────────

def _draw_ticks(ctx, cx, cy, radius, val_min, val_max,
                major_step, minor_step, major_len, minor_len,
                major_width, minor_width,
                redzone_start=None, hotzone_start=None):
    """Draw major and minor tick marks around a dial face."""
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    # Major ticks
    val = val_min
    while val <= val_max + 0.001:
        angle = _value_to_angle_rad(val, val_min, val_max)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        x1 = cx + (radius - major_len) * cos_a
        y1 = cy - (radius - major_len) * sin_a
        x2 = cx + (radius - 2) * cos_a
        y2 = cy - (radius - 2) * sin_a

        in_red = redzone_start is not None and val >= redzone_start
        in_hot = hotzone_start is not None and val >= hotzone_start

        if in_red:
            ctx.set_source_rgb(*_rgb(E36_REDZONE_TICK))
        elif in_hot:
            ctx.set_source_rgb(*_rgb(E36_HOT_ZONE))
        else:
            ctx.set_source_rgb(*_rgb(E36_TICK_MAJOR))

        ctx.set_line_width(major_width)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        val += major_step

    # Minor ticks
    if minor_step:
        val = val_min
        while val <= val_max + 0.001:
            # Skip if at a major tick position
            remainder = (val - val_min) % major_step
            if remainder < 0.001 or abs(remainder - major_step) < 0.001:
                val += minor_step
                continue

            angle = _value_to_angle_rad(val, val_min, val_max)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)

            x1 = cx + (radius - minor_len) * cos_a
            y1 = cy - (radius - minor_len) * sin_a
            x2 = cx + (radius - 2) * cos_a
            y2 = cy - (radius - 2) * sin_a

            in_red = redzone_start is not None and val >= redzone_start
            ctx.set_source_rgb(*_rgb(E36_REDZONE_TICK if in_red else E36_TICK_MINOR))
            ctx.set_line_width(minor_width)
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()
            val += minor_step


def _draw_numbers(ctx, cx, cy, radius, val_min, val_max,
                  major_step, number_fn, font_size, number_inset,
                  redzone_start=None):
    """Draw numbers around the dial circumference."""
    ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_size)

    nr = radius - number_inset

    val = val_min
    while val <= val_max + 0.001:
        label = number_fn(val)
        if label:
            angle = _value_to_angle_rad(val, val_min, val_max)
            nx = cx + nr * math.cos(angle)
            ny = cy - nr * math.sin(angle)

            extents = ctx.text_extents(label)
            tx = nx - extents.width / 2 - extents.x_bearing
            ty = ny - extents.height / 2 - extents.y_bearing

            in_red = redzone_start is not None and val >= redzone_start
            ctx.set_source_rgb(*_rgb(E36_REDZONE_TICK if in_red else E36_NUMBER))
            ctx.move_to(tx, ty)
            ctx.show_text(label)
        val += major_step


# ── Dial Face Renderers ──────────────────────────────────────

def render_tach_face():
    """Render the tachometer dial face (0-7000 RPM). Returns pygame Surface."""
    r = E36_TACH_RADIUS
    side = (r + PAD) * 2
    cx = cy = side // 2

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, side, side)
    ctx = cairo.Context(surface)

    # Black face circle
    ctx.arc(cx, cy, r + 2, 0, 2 * math.pi)
    ctx.set_source_rgb(*_rgb(E36_FACE_BG))
    ctx.fill()

    # Outer ring
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.set_source_rgb(*_rgb(E36_RING))
    ctx.set_line_width(1.5)
    ctx.stroke()

    # Red zone sector fill
    _draw_arc_sector(ctx, cx, cy, r - 2, r - E36_LG_MAJOR_LEN - 4,
                     E36_RPM_REDZONE, E36_RPM_MAX,
                     E36_RPM_MIN, E36_RPM_MAX,
                     _rgba(E36_REDZONE_FILL, 0.35))

    # Ticks
    _draw_ticks(ctx, cx, cy, r,
                E36_RPM_MIN, E36_RPM_MAX,
                1000, 200,
                E36_LG_MAJOR_LEN, E36_LG_MINOR_LEN,
                E36_LG_MAJOR_WIDTH, E36_LG_MINOR_WIDTH,
                redzone_start=E36_RPM_REDZONE)

    # Numbers (1-7, representing x1000)
    _draw_numbers(ctx, cx, cy, r,
                  E36_RPM_MIN, E36_RPM_MAX,
                  1000,
                  lambda v: str(int(v / 1000)) if v > 0 else None,
                  24, E36_LG_NUMBER_INSET,
                  redzone_start=E36_RPM_REDZONE)

    # Label "1/min x 1000"
    ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(11)
    ctx.set_source_rgb(*_rgb(CLR_TEXT_DIM))
    ext = ctx.text_extents("1/min \u00d7 1000")
    ctx.move_to(cx - ext.width / 2, cy + r * 0.55)
    ctx.show_text("1/min \u00d7 1000")

    return _cairo_to_pygame(surface)


def render_speed_face():
    """Render the speedometer dial face (0-240 km/h). Returns pygame Surface."""
    r = E36_SPD_RADIUS
    side = (r + PAD) * 2
    cx = cy = side // 2

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, side, side)
    ctx = cairo.Context(surface)

    # Black face circle
    ctx.arc(cx, cy, r + 2, 0, 2 * math.pi)
    ctx.set_source_rgb(*_rgb(E36_FACE_BG))
    ctx.fill()

    # Outer ring
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.set_source_rgb(*_rgb(E36_RING))
    ctx.set_line_width(1.5)
    ctx.stroke()

    # Ticks
    _draw_ticks(ctx, cx, cy, r,
                E36_SPD_MIN, E36_SPD_MAX,
                20, 10,
                E36_LG_MAJOR_LEN, E36_LG_MINOR_LEN,
                E36_LG_MAJOR_WIDTH, E36_LG_MINOR_WIDTH)

    # Numbers (20, 40, ... 240)
    _draw_numbers(ctx, cx, cy, r,
                  E36_SPD_MIN, E36_SPD_MAX,
                  20,
                  lambda v: str(int(v)) if v > 0 else None,
                  17, E36_LG_NUMBER_INSET)

    # Label "km/h"
    ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(11)
    ctx.set_source_rgb(*_rgb(CLR_TEXT_DIM))
    ext = ctx.text_extents("km/h")
    ctx.move_to(cx - ext.width / 2, cy + r * 0.55)
    ctx.show_text("km/h")

    return _cairo_to_pygame(surface)


def render_coolant_face():
    """Render coolant temperature dial face (C-H, no numbers). Returns pygame Surface."""
    r = E36_COOL_RADIUS
    side = (r + PAD) * 2
    cx = cy = side // 2

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, side, side)
    ctx = cairo.Context(surface)

    # Black face circle
    ctx.arc(cx, cy, r + 2, 0, 2 * math.pi)
    ctx.set_source_rgb(*_rgb(E36_FACE_BG))
    ctx.fill()

    # Outer ring
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.set_source_rgb(*_rgb(E36_RING))
    ctx.set_line_width(1.0)
    ctx.stroke()

    # Cold zone (blue) — first 25%
    _draw_arc_sector(ctx, cx, cy, r - 2, r - E36_SM_MAJOR_LEN - 4,
                     E36_COOL_MIN, E36_COOL_COLD,
                     E36_COOL_MIN, E36_COOL_MAX,
                     _rgba(E36_COLD_ZONE, 0.30))

    # Hot zone (red) — last 25%
    _draw_arc_sector(ctx, cx, cy, r - 2, r - E36_SM_MAJOR_LEN - 4,
                     E36_COOL_HOT, E36_COOL_MAX,
                     E36_COOL_MIN, E36_COOL_MAX,
                     _rgba(E36_HOT_ZONE, 0.30))

    # Ticks
    _draw_ticks(ctx, cx, cy, r,
                E36_COOL_MIN, E36_COOL_MAX,
                12.5, None,
                E36_SM_MAJOR_LEN, E36_SM_MINOR_LEN,
                E36_SM_MAJOR_WIDTH, E36_SM_MINOR_WIDTH,
                hotzone_start=E36_COOL_HOT)

    # C and H labels
    nr = r - E36_SM_NUMBER_INSET
    ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(16)

    # "C" at cold end
    a_c = _value_to_angle_rad(E36_COOL_MIN, E36_COOL_MIN, E36_COOL_MAX)
    ctx.set_source_rgb(*_rgb(E36_COLD_ZONE))
    ext = ctx.text_extents("C")
    ctx.move_to(cx + nr * math.cos(a_c) - ext.width / 2,
                cy - nr * math.sin(a_c) + ext.height / 2)
    ctx.show_text("C")

    # "H" at hot end
    a_h = _value_to_angle_rad(E36_COOL_MAX, E36_COOL_MIN, E36_COOL_MAX)
    ctx.set_source_rgb(*_rgb(E36_HOT_ZONE))
    ext = ctx.text_extents("H")
    ctx.move_to(cx + nr * math.cos(a_h) - ext.width / 2,
                cy - nr * math.sin(a_h) + ext.height / 2)
    ctx.show_text("H")

    return _cairo_to_pygame(surface)


def render_fuel_face():
    """Render fuel gauge dial face (E-F). Returns pygame Surface."""
    r = E36_FUEL_RADIUS
    side = (r + PAD) * 2
    cx = cy = side // 2

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, side, side)
    ctx = cairo.Context(surface)

    # Black face circle
    ctx.arc(cx, cy, r + 2, 0, 2 * math.pi)
    ctx.set_source_rgb(*_rgb(E36_FACE_BG))
    ctx.fill()

    # Outer ring
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.set_source_rgb(*_rgb(E36_RING))
    ctx.set_line_width(1.0)
    ctx.stroke()

    # Reserve zone (amber) — first 15%
    _draw_arc_sector(ctx, cx, cy, r - 2, r - E36_SM_MAJOR_LEN - 4,
                     E36_FUEL_MIN, E36_FUEL_RESERVE,
                     E36_FUEL_MIN, E36_FUEL_MAX,
                     _rgba(E36_RESERVE, 0.30))

    # Ticks
    _draw_ticks(ctx, cx, cy, r,
                E36_FUEL_MIN, E36_FUEL_MAX,
                12.5, None,
                E36_SM_MAJOR_LEN, E36_SM_MINOR_LEN,
                E36_SM_MAJOR_WIDTH, E36_SM_MINOR_WIDTH)

    # E and F labels
    nr = r - E36_SM_NUMBER_INSET
    ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(16)

    # "E" at empty end
    a_e = _value_to_angle_rad(E36_FUEL_MIN, E36_FUEL_MIN, E36_FUEL_MAX)
    ctx.set_source_rgb(*_rgb(E36_RESERVE))
    ext = ctx.text_extents("E")
    ctx.move_to(cx + nr * math.cos(a_e) - ext.width / 2,
                cy - nr * math.sin(a_e) + ext.height / 2)
    ctx.show_text("E")

    # "F" at full end
    a_f = _value_to_angle_rad(E36_FUEL_MAX, E36_FUEL_MIN, E36_FUEL_MAX)
    ctx.set_source_rgb(*_rgb(E36_NUMBER))
    ext = ctx.text_extents("F")
    ctx.move_to(cx + nr * math.cos(a_f) - ext.width / 2,
                cy - nr * math.sin(a_f) + ext.height / 2)
    ctx.show_text("F")

    return _cairo_to_pygame(surface)


# ── Needle Sprite Renderer ───────────────────────────────────

def render_needle_sprite(length, tail, base_width, tip_width):
    """Render a tapered needle sprite with pivot at center. Returns pygame Surface.

    The needle points to the RIGHT (+X) from the pivot. pygame.transform.rotozoom()
    rotates around the Surface center, which is the pivot point.
    """
    side = 2 * (length + tail + 10)
    cx = cy = side // 2

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, side, side)
    ctx = cairo.Context(surface)

    bh = base_width / 2
    th = tip_width / 2
    tailh = base_width / 2 + 1

    # Needle body (tapered trapezoid)
    ctx.new_path()
    ctx.move_to(cx - tail, cy - tailh)          # tail top
    ctx.line_to(cx, cy - bh)                    # base top
    ctx.line_to(cx + length, cy - th)           # tip top
    ctx.line_to(cx + length, cy + th)           # tip bottom
    ctx.line_to(cx, cy + bh)                    # base bottom
    ctx.line_to(cx - tail, cy + tailh)          # tail bottom
    ctx.close_path()
    ctx.set_source_rgb(*_rgb(E36_NEEDLE))
    ctx.fill_preserve()
    ctx.set_source_rgba(0, 0, 0, 0.4)
    ctx.set_line_width(0.5)
    ctx.stroke()

    # Counter-weight circle at tail
    ctx.arc(cx - tail, cy, tailh + 1, 0, 2 * math.pi)
    ctx.set_source_rgb(*_rgb(E36_NEEDLE_TAIL))
    ctx.fill()

    return _cairo_to_pygame(surface)


def render_large_needle():
    """Render the tach/speed needle sprite."""
    return render_needle_sprite(
        E36_NEEDLE_LG_LEN, E36_NEEDLE_LG_TAIL,
        E36_NEEDLE_LG_BASE, E36_NEEDLE_LG_TIP)


def render_small_needle():
    """Render the coolant/fuel needle sprite."""
    return render_needle_sprite(
        E36_NEEDLE_SM_LEN, E36_NEEDLE_SM_TAIL,
        E36_NEEDLE_SM_BASE, E36_NEEDLE_SM_TIP)
