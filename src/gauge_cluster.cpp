#include "gauge_cluster.h"
#include <stdio.h>

/* ── Screen dimensions ───────────────────────────────────────────── */
#define SCR_W  1024
#define SCR_H  600

/* ── Arc sweep geometry (LVGL: 0° = 3 o'clock, CCW positive) ──────
 * We want the gauge to go from ~220° (bottom-left) to ~320° (bottom-right),
 * spanning 260° — classic automotive style.
 *
 * LVGL arc angles: 0 = 3-o'clock, increases CW.
 * For a gauge that starts at 7 o'clock and ends at 5 o'clock:
 *   bg start = 135, bg end = 45  (220° sweep)
 */
#define ARC_START_ANGLE  135   // 7 o'clock
#define ARC_END_ANGLE    45    // 5 o'clock

/* ── Large gauge sizes ───────────────────────────────────────────── */
#define LARGE_ARC_D   290   // diameter of RPM / speed gauges
#define SMALL_ARC_D   140   // diameter of temp / fuel gauges

/* ── Widget handles ─────────────────────────────────────────────── */
static lv_obj_t *scr;

// Tachometer
static lv_obj_t *arc_rpm;
static lv_obj_t *arc_rpm_redzone;
static lv_obj_t *lbl_rpm_val;
static lv_obj_t *lbl_rpm_unit;

// Speedometer
static lv_obj_t *arc_spd;
static lv_obj_t *lbl_spd_val;
static lv_obj_t *lbl_spd_unit;
static lv_obj_t *lbl_gear;

// Coolant
static lv_obj_t *arc_temp;
static lv_obj_t *lbl_temp_val;

// Fuel
static lv_obj_t *arc_fuel;
static lv_obj_t *lbl_fuel_val;

// Telltales
static lv_obj_t *tell_ce;   // check engine
static lv_obj_t *tell_oil;
static lv_obj_t *tell_bat;
static lv_obj_t *tell_abs;
static lv_obj_t *tell_esp;

/* ── Helper: create a styled arc gauge ──────────────────────────── */
static lv_obj_t *make_arc(lv_obj_t *parent,
                           int x, int y,
                           int diameter,
                           lv_color_t arc_color,
                           int range_min, int range_max)
{
  lv_obj_t *arc = lv_arc_create(parent);
  lv_obj_set_size(arc, diameter, diameter);
  lv_obj_set_pos(arc, x, y);

  lv_arc_set_rotation(arc, 0);
  lv_arc_set_bg_angles(arc, ARC_START_ANGLE, ARC_END_ANGLE);
  lv_arc_set_range(arc, range_min, range_max);
  lv_arc_set_value(arc, range_min);

  // Remove the knob
  lv_obj_remove_style(arc, NULL, LV_PART_KNOB);
  lv_obj_clear_flag(arc, LV_OBJ_FLAG_CLICKABLE);

  // Background arc — dim
  lv_obj_set_style_arc_color(arc, CLR_ARC_BG, LV_PART_MAIN);
  lv_obj_set_style_arc_width(arc, 18, LV_PART_MAIN);
  lv_obj_set_style_arc_rounded(arc, true, LV_PART_MAIN);
  lv_obj_set_style_bg_opa(arc, LV_OPA_TRANSP, LV_PART_MAIN);
  lv_obj_set_style_border_width(arc, 0, LV_PART_MAIN);

  // Indicator arc — glowing color
  lv_obj_set_style_arc_color(arc, arc_color, LV_PART_INDICATOR);
  lv_obj_set_style_arc_width(arc, 18, LV_PART_INDICATOR);
  lv_obj_set_style_arc_rounded(arc, true, LV_PART_INDICATOR);

  return arc;
}

/* ── Helper: scale tick marks around a large arc ────────────────── */
static void draw_tick_marks(lv_obj_t *parent,
                             int cx, int cy, int outer_r,
                             int tick_count,
                             lv_color_t color)
{
  // Draw major tick marks using thin arcs (2° wide) evenly distributed
  float start_deg = 135.0f + 180.0f;  // convert LVGL to geometric degrees
  float sweep     = 270.0f;           // total sweep of gauge
  float step      = sweep / (tick_count - 1);

  for (int i = 0; i < tick_count; i++) {
    float angle_geo = start_deg + i * step;
    // Convert to radians
    float rad = angle_geo * 3.14159f / 180.0f;

    // Tick inner / outer positions
    int inner_r = outer_r - 20;
    int x0 = (int)(cx + inner_r * cos(rad));
    int y0 = (int)(cy + inner_r * sin(rad));
    int x1 = (int)(cx + outer_r * cos(rad));
    int y1 = (int)(cy + outer_r * sin(rad));

    // Draw as a short line object
    static lv_point_t pts[2];
    pts[0] = {(lv_coord_t)x0, (lv_coord_t)y0};
    pts[1] = {(lv_coord_t)x1, (lv_coord_t)y1};

    lv_obj_t *line = lv_line_create(parent);
    lv_line_set_points(line, pts, 2);
    lv_obj_set_style_line_color(line, color, LV_PART_MAIN);
    lv_obj_set_style_line_width(line, (i % 2 == 0) ? 3 : 1, LV_PART_MAIN);
    lv_obj_set_style_line_rounded(line, true, LV_PART_MAIN);
  }
}

/* ── Helper: telltale icon label ─────────────────────────────────── */
static lv_obj_t *make_telltale(lv_obj_t *parent,
                                int x, int y,
                                const char *icon,
                                lv_color_t active_color)
{
  lv_obj_t *cont = lv_obj_create(parent);
  lv_obj_set_size(cont, 56, 36);
  lv_obj_set_pos(cont, x, y);
  lv_obj_set_style_bg_color(cont, lv_color_hex(0x1E1E1E), LV_PART_MAIN);
  lv_obj_set_style_bg_opa(cont, LV_OPA_COVER, LV_PART_MAIN);
  lv_obj_set_style_border_color(cont, lv_color_hex(0x303030), LV_PART_MAIN);
  lv_obj_set_style_border_width(cont, 1, LV_PART_MAIN);
  lv_obj_set_style_radius(cont, 6, LV_PART_MAIN);
  lv_obj_clear_flag(cont, LV_OBJ_FLAG_SCROLLABLE);

  lv_obj_t *lbl = lv_label_create(cont);
  lv_label_set_text(lbl, icon);
  lv_obj_set_style_text_color(lbl, CLR_TEXT_DIM, LV_PART_MAIN);
  lv_obj_set_style_text_font(lbl, &lv_font_montserrat_12, LV_PART_MAIN);
  lv_obj_center(lbl);

  // Store active color in user_data (not used here, toggled in update())
  lv_obj_set_user_data(cont, (void *)active_color.full);
  (void)active_color;  // suppress warning — used in gauge_cluster_update

  return cont;
}

/* ─────────────────────────────────────────────────────────────────
 * gauge_cluster_init()
 * ───────────────────────────────────────────────────────────────── */
void gauge_cluster_init(void)
{
  scr = lv_scr_act();

  // Dark background
  lv_obj_set_style_bg_color(scr, CLR_BG, LV_PART_MAIN);
  lv_obj_set_style_bg_opa(scr, LV_OPA_COVER, LV_PART_MAIN);
  lv_obj_clear_flag(scr, LV_OBJ_FLAG_SCROLLABLE);

  /* ── Divider lines ────────────────────────────────────────────── */
  // Vertical center divider
  static lv_point_t vdiv[2] = {{512, 60}, {512, 520}};
  lv_obj_t *vline = lv_line_create(scr);
  lv_line_set_points(vline, vdiv, 2);
  lv_obj_set_style_line_color(vline, lv_color_hex(0x282828), LV_PART_MAIN);
  lv_obj_set_style_line_width(vline, 1, LV_PART_MAIN);

  /* ── Tachometer (left, center ~256, 280) ─────────────────────── */
  int rpm_x = (512 - LARGE_ARC_D) / 2;   // ~111
  int rpm_y = (SCR_H - LARGE_ARC_D) / 2 - 20; // ~135
  arc_rpm = make_arc(scr, rpm_x, rpm_y, LARGE_ARC_D, CLR_RPM_ARC, 0, 8000);

  // Red zone overlay arc (6000–8000) — separate arc on top, same position
  arc_rpm_redzone = lv_arc_create(scr);
  lv_obj_set_size(arc_rpm_redzone, LARGE_ARC_D, LARGE_ARC_D);
  lv_obj_set_pos(arc_rpm_redzone, rpm_x, rpm_y);
  lv_arc_set_rotation(arc_rpm_redzone, 0);
  lv_arc_set_bg_angles(arc_rpm_redzone, ARC_START_ANGLE, ARC_END_ANGLE);
  lv_arc_set_range(arc_rpm_redzone, 0, 8000);
  lv_arc_set_value(arc_rpm_redzone, 6000);        // permanent red zone marker
  lv_obj_remove_style(arc_rpm_redzone, NULL, LV_PART_KNOB);
  lv_obj_clear_flag(arc_rpm_redzone, LV_OBJ_FLAG_CLICKABLE);
  lv_obj_set_style_arc_color(arc_rpm_redzone, CLR_ARC_BG, LV_PART_MAIN);
  lv_obj_set_style_arc_width(arc_rpm_redzone, 18, LV_PART_MAIN);
  lv_obj_set_style_arc_color(arc_rpm_redzone, CLR_RED_ZONE, LV_PART_INDICATOR);
  lv_obj_set_style_arc_width(arc_rpm_redzone, 18, LV_PART_INDICATOR);
  lv_obj_set_style_arc_opa(arc_rpm_redzone, LV_OPA_50, LV_PART_INDICATOR);
  lv_obj_set_style_bg_opa(arc_rpm_redzone, LV_OPA_TRANSP, LV_PART_MAIN);
  lv_obj_set_style_border_width(arc_rpm_redzone, 0, LV_PART_MAIN);

  // RPM value label
  lbl_rpm_val = lv_label_create(scr);
  lv_label_set_text(lbl_rpm_val, "0");
  lv_obj_set_style_text_color(lbl_rpm_val, CLR_TEXT_MAIN, LV_PART_MAIN);
  lv_obj_set_style_text_font(lbl_rpm_val, &lv_font_montserrat_48, LV_PART_MAIN);
  lv_obj_set_pos(lbl_rpm_val, rpm_x + LARGE_ARC_D/2 - 60, rpm_y + LARGE_ARC_D/2 - 36);

  lbl_rpm_unit = lv_label_create(scr);
  lv_label_set_text(lbl_rpm_unit, "RPM x100");
  lv_obj_set_style_text_color(lbl_rpm_unit, CLR_TEXT_DIM, LV_PART_MAIN);
  lv_obj_set_style_text_font(lbl_rpm_unit, &lv_font_montserrat_12, LV_PART_MAIN);
  lv_obj_set_pos(lbl_rpm_unit, rpm_x + LARGE_ARC_D/2 - 38, rpm_y + LARGE_ARC_D/2 + 16);

  /* ── Speedometer (right, center ~768, 280) ───────────────────── */
  int spd_x = 512 + (512 - LARGE_ARC_D) / 2;  // ~623
  int spd_y = rpm_y;
  arc_spd = make_arc(scr, spd_x, spd_y, LARGE_ARC_D, CLR_SPD_ARC, 0, 260);

  lbl_spd_val = lv_label_create(scr);
  lv_label_set_text(lbl_spd_val, "0");
  lv_obj_set_style_text_color(lbl_spd_val, CLR_TEXT_MAIN, LV_PART_MAIN);
  lv_obj_set_style_text_font(lbl_spd_val, &lv_font_montserrat_48, LV_PART_MAIN);
  lv_obj_set_pos(lbl_spd_val, spd_x + LARGE_ARC_D/2 - 40, spd_y + LARGE_ARC_D/2 - 36);

  lbl_spd_unit = lv_label_create(scr);
  lv_label_set_text(lbl_spd_unit, "km/h");
  lv_obj_set_style_text_color(lbl_spd_unit, CLR_TEXT_DIM, LV_PART_MAIN);
  lv_obj_set_style_text_font(lbl_spd_unit, &lv_font_montserrat_14, LV_PART_MAIN);
  lv_obj_set_pos(lbl_spd_unit, spd_x + LARGE_ARC_D/2 - 22, spd_y + LARGE_ARC_D/2 + 16);

  // Gear indicator (center of speedometer)
  lbl_gear = lv_label_create(scr);
  lv_label_set_text(lbl_gear, "N");
  lv_obj_set_style_text_color(lbl_gear, lv_color_hex(0x00FF7F), LV_PART_MAIN);
  lv_obj_set_style_text_font(lbl_gear, &lv_font_montserrat_32, LV_PART_MAIN);
  lv_obj_set_pos(lbl_gear, spd_x + LARGE_ARC_D/2 - 12, spd_y + LARGE_ARC_D/2 + 40);

  /* ── Coolant temp (bottom-left) ──────────────────────────────── */
  int temp_x = 40;
  int temp_y = SCR_H - SMALL_ARC_D - 50;
  arc_temp = make_arc(scr, temp_x, temp_y, SMALL_ARC_D, CLR_TEMP_ARC, 40, 130);

  // "TEMP" label above
  lv_obj_t *lbl_temp_title = lv_label_create(scr);
  lv_label_set_text(lbl_temp_title, "COOLANT");
  lv_obj_set_style_text_color(lbl_temp_title, CLR_TEXT_DIM, LV_PART_MAIN);
  lv_obj_set_style_text_font(lbl_temp_title, &lv_font_montserrat_12, LV_PART_MAIN);
  lv_obj_set_pos(lbl_temp_title, temp_x + 20, temp_y - 20);

  lbl_temp_val = lv_label_create(scr);
  lv_label_set_text(lbl_temp_val, "--°C");
  lv_obj_set_style_text_color(lbl_temp_val, CLR_TEXT_MAIN, LV_PART_MAIN);
  lv_obj_set_style_text_font(lbl_temp_val, &lv_font_montserrat_16, LV_PART_MAIN);
  lv_obj_set_pos(lbl_temp_val, temp_x + SMALL_ARC_D/2 - 22, temp_y + SMALL_ARC_D/2 - 12);

  /* ── Fuel gauge (bottom-right) ───────────────────────────────── */
  int fuel_x = SCR_W - SMALL_ARC_D - 40;
  int fuel_y = temp_y;
  arc_fuel = make_arc(scr, fuel_x, fuel_y, SMALL_ARC_D, CLR_FUEL_ARC, 0, 100);

  lv_obj_t *lbl_fuel_title = lv_label_create(scr);
  lv_label_set_text(lbl_fuel_title, "FUEL");
  lv_obj_set_style_text_color(lbl_fuel_title, CLR_TEXT_DIM, LV_PART_MAIN);
  lv_obj_set_style_text_font(lbl_fuel_title, &lv_font_montserrat_12, LV_PART_MAIN);
  lv_obj_set_pos(lbl_fuel_title, fuel_x + 44, fuel_y - 20);

  lbl_fuel_val = lv_label_create(scr);
  lv_label_set_text(lbl_fuel_val, "--%");
  lv_obj_set_style_text_color(lbl_fuel_val, CLR_TEXT_MAIN, LV_PART_MAIN);
  lv_obj_set_style_text_font(lbl_fuel_val, &lv_font_montserrat_16, LV_PART_MAIN);
  lv_obj_set_pos(lbl_fuel_val, fuel_x + SMALL_ARC_D/2 - 18, fuel_y + SMALL_ARC_D/2 - 12);

  /* ── Telltale row (top center) ───────────────────────────────── */
  int tell_y   = 14;
  int tell_gap = 66;
  int tell_start = SCR_W/2 - (5 * tell_gap)/2;

  tell_ce  = make_telltale(scr, tell_start + 0*tell_gap, tell_y, "ENG",  CLR_WARN_YELLOW);
  tell_oil = make_telltale(scr, tell_start + 1*tell_gap, tell_y, "OIL",  CLR_WARN_RED);
  tell_bat = make_telltale(scr, tell_start + 2*tell_gap, tell_y, "BAT",  CLR_WARN_RED);
  tell_abs = make_telltale(scr, tell_start + 3*tell_gap, tell_y, "ABS",  CLR_WARN_YELLOW);
  tell_esp = make_telltale(scr, tell_start + 4*tell_gap, tell_y, "ESP",  CLR_WARN_YELLOW);

  /* ── Odometer / trip (bottom center) ────────────────────────── */
  lv_obj_t *lbl_odo = lv_label_create(scr);
  lv_label_set_text(lbl_odo, "TRIP  ---.- km");
  lv_obj_set_style_text_color(lbl_odo, CLR_TEXT_DIM, LV_PART_MAIN);
  lv_obj_set_style_text_font(lbl_odo, &lv_font_montserrat_14, LV_PART_MAIN);
  lv_obj_set_pos(lbl_odo, SCR_W/2 - 72, SCR_H - 28);
}

/* ─────────────────────────────────────────────────────────────────
 * gauge_cluster_update()  — call every frame with fresh data
 * ───────────────────────────────────────────────────────────────── */
void gauge_cluster_update(const ClusterData &d)
{
  /* RPM */
  lv_arc_set_value(arc_rpm, d.rpm);
  // Change arc color to red when in red zone
  if (d.rpm >= 6000) {
    lv_obj_set_style_arc_color(arc_rpm, CLR_RED_ZONE, LV_PART_INDICATOR);
  } else if (d.rpm >= 5000) {
    lv_obj_set_style_arc_color(arc_rpm, lv_color_hex(0xFF8C00), LV_PART_INDICATOR);
  } else {
    lv_obj_set_style_arc_color(arc_rpm, CLR_RPM_ARC, LV_PART_INDICATOR);
  }
  char buf[16];
  snprintf(buf, sizeof(buf), "%d", d.rpm / 100);
  lv_label_set_text(lbl_rpm_val, buf);

  /* Speed */
  lv_arc_set_value(arc_spd, d.speed_kmh);
  snprintf(buf, sizeof(buf), "%d", d.speed_kmh);
  lv_label_set_text(lbl_spd_val, buf);

  /* Gear */
  if (d.gear == 0)       lv_label_set_text(lbl_gear, "N");
  else if (d.gear == 7)  lv_label_set_text(lbl_gear, "R");
  else { snprintf(buf, sizeof(buf), "%d", d.gear); lv_label_set_text(lbl_gear, buf); }

  /* Coolant */
  lv_arc_set_value(arc_temp, d.coolant_c);
  snprintf(buf, sizeof(buf), "%d\xC2\xB0""C", d.coolant_c); // °C in UTF-8
  lv_label_set_text(lbl_temp_val, buf);
  if (d.coolant_c >= 110) {
    lv_obj_set_style_arc_color(arc_temp, CLR_RED_ZONE, LV_PART_INDICATOR);
  } else {
    lv_obj_set_style_arc_color(arc_temp, CLR_TEMP_ARC, LV_PART_INDICATOR);
  }

  /* Fuel */
  lv_arc_set_value(arc_fuel, d.fuel_pct);
  snprintf(buf, sizeof(buf), "%d%%", d.fuel_pct);
  lv_label_set_text(lbl_fuel_val, buf);
  if (d.fuel_pct <= 10) {
    lv_obj_set_style_arc_color(arc_fuel, CLR_WARN_RED, LV_PART_INDICATOR);
  } else {
    lv_obj_set_style_arc_color(arc_fuel, CLR_FUEL_ARC, LV_PART_INDICATOR);
  }

  /* Telltales — light up if active */
  auto set_tell = [](lv_obj_t *cont, bool active, lv_color_t col) {
    lv_obj_t *lbl = lv_obj_get_child(cont, 0);
    if (active) {
      lv_obj_set_style_bg_color(cont, lv_color_mix(col, lv_color_hex(0x1E1E1E), 60), LV_PART_MAIN);
      lv_obj_set_style_text_color(lbl, col, LV_PART_MAIN);
      lv_obj_set_style_border_color(cont, col, LV_PART_MAIN);
    } else {
      lv_obj_set_style_bg_color(cont, lv_color_hex(0x1E1E1E), LV_PART_MAIN);
      lv_obj_set_style_text_color(lbl, CLR_TEXT_DIM, LV_PART_MAIN);
      lv_obj_set_style_border_color(cont, lv_color_hex(0x303030), LV_PART_MAIN);
    }
  };

  set_tell(tell_ce,  d.check_engine,  CLR_WARN_YELLOW);
  set_tell(tell_oil, d.oil_pressure,  CLR_WARN_RED);
  set_tell(tell_bat, d.battery_warn,  CLR_WARN_RED);
  set_tell(tell_abs, d.abs_warn,      CLR_WARN_YELLOW);
  set_tell(tell_esp, d.esp_warn,      CLR_WARN_YELLOW);
}
