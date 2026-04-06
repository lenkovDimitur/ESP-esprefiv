#pragma once
#include <lvgl.h>

/* ── Palette ─────────────────────────────────────────────────────── */
#define CLR_BG          lv_color_hex(0x0D0D0D)  // near-black
#define CLR_PANEL       lv_color_hex(0x161616)
#define CLR_RPM_ARC     lv_color_hex(0xFF4500)  // red-orange
#define CLR_SPD_ARC     lv_color_hex(0x00BFFF)  // deep sky blue
#define CLR_TEMP_ARC    lv_color_hex(0x00E5CC)  // teal
#define CLR_FUEL_ARC    lv_color_hex(0xFFD700)  // gold
#define CLR_ARC_BG      lv_color_hex(0x2A2A2A)
#define CLR_TEXT_MAIN   lv_color_hex(0xE8E8E8)
#define CLR_TEXT_DIM    lv_color_hex(0x606060)
#define CLR_RED_ZONE    lv_color_hex(0xFF1010)
#define CLR_WARN_YELLOW lv_color_hex(0xFFAA00)
#define CLR_WARN_RED    lv_color_hex(0xFF2020)

/* ── Gauge data (update these from CAN/K-line or test animation) ── */
struct ClusterData {
  uint16_t rpm;          // 0 – 8000
  uint8_t  speed_kmh;    // 0 – 260
  uint8_t  coolant_c;    // -40 – 150  (offset +40 stored as 0-190)
  uint8_t  fuel_pct;     // 0 – 100
  bool     check_engine;
  bool     oil_pressure;
  bool     battery_warn;
  bool     abs_warn;
  bool     esp_warn;
  uint8_t  gear;         // 0=N, 1-6, 7=R
};

/* ── Public API ──────────────────────────────────────────────────── */
void gauge_cluster_init(void);
void gauge_cluster_update(const ClusterData &d);
