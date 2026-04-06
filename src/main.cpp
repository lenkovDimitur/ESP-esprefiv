#include <Arduino.h>
#include <lvgl.h>
#include <LovyanGFX.hpp>
#include "lgfx_config.h"
#include "gauge_cluster.h"

/* ── Display instance ───────────────────────────────────────────── */
static LGFX display;

/* ── LVGL draw buffer (double-buffered, ~10 lines) ──────────────── */
static const uint32_t DRAW_BUF_LINES = 20;
static lv_color_t draw_buf1[1024 * DRAW_BUF_LINES];
static lv_color_t draw_buf2[1024 * DRAW_BUF_LINES];
static lv_disp_draw_buf_t draw_buf_desc;
static lv_disp_drv_t      disp_drv;

/* ── Flush callback: LVGL → LovyanGFX ──────────────────────────── */
static void lvgl_flush_cb(lv_disp_drv_t *drv, const lv_area_t *area, lv_color_t *px_map)
{
  uint32_t w = area->x2 - area->x1 + 1;
  uint32_t h = area->y2 - area->y1 + 1;
  display.startWrite();
  display.setAddrWindow(area->x1, area->y1, w, h);
  display.writePixels((lgfx::rgb565_t *)px_map, w * h);
  display.endWrite();
  lv_disp_flush_ready(drv);
}

/* ── Touch read callback ─────────────────────────────────────────── */
static lv_indev_drv_t indev_drv;

static void lvgl_touch_cb(lv_indev_drv_t *drv, lv_indev_data_t *data)
{
  (void)drv;
  uint16_t tx, ty;
  if (display.getTouch(&tx, &ty)) {
    data->state   = LV_INDEV_STATE_PR;
    data->point.x = tx;
    data->point.y = ty;
  } else {
    data->state = LV_INDEV_STATE_REL;
  }
}

/* ── Demo animation state ────────────────────────────────────────── */
static ClusterData sim = {
  .rpm          = 800,
  .speed_kmh    = 0,
  .coolant_c    = 20,
  .fuel_pct     = 75,
  .check_engine = false,
  .oil_pressure = false,
  .battery_warn = false,
  .abs_warn     = false,
  .esp_warn     = false,
  .gear         = 0,
};

static int  sim_dir     = 1;
static bool sim_warm    = false;

static void simulate_data(void)
{
  // Animate RPM up and down for demo
  sim.rpm += sim_dir * 120;
  if (sim.rpm >= 7200) sim_dir = -1;
  if (sim.rpm <= 700)  sim_dir =  1;

  // Speed tracks RPM loosely
  sim.speed_kmh = (uint8_t)((sim.rpm - 700) / 26);
  if (sim.speed_kmh > 260) sim.speed_kmh = 260;

  // Gear from speed
  if      (sim.speed_kmh < 10)  sim.gear = 0; // N
  else if (sim.speed_kmh < 30)  sim.gear = 1;
  else if (sim.speed_kmh < 60)  sim.gear = 2;
  else if (sim.speed_kmh < 90)  sim.gear = 3;
  else if (sim.speed_kmh < 130) sim.gear = 4;
  else if (sim.speed_kmh < 170) sim.gear = 5;
  else                           sim.gear = 6;

  // Warm up coolant slowly
  if (!sim_warm && sim.coolant_c < 90) {
    sim.coolant_c++;
  } else {
    sim_warm = true;
    sim.coolant_c = 88 + (sim.rpm / 2000);
  }

  // Fuel drains slowly
  static uint32_t fuel_tick = 0;
  if (++fuel_tick % 200 == 0 && sim.fuel_pct > 0) sim.fuel_pct--;

  // Toggle battery warn when fuel low for demo
  sim.battery_warn = (sim.fuel_pct < 15);
}

/* ── setup() ─────────────────────────────────────────────────────── */
void setup()
{
  Serial.begin(115200);
  Serial.println("Gauge Cluster Booting...");

  /* Display init */
  display.init();
  display.setRotation(0);
  display.setBrightness(200);
  display.fillScreen(TFT_BLACK);

  /* LVGL init */
  lv_init();
  lv_disp_draw_buf_init(&draw_buf_desc, draw_buf1, draw_buf2,
                         1024 * DRAW_BUF_LINES);

  lv_disp_drv_init(&disp_drv);
  disp_drv.hor_res  = 1024;
  disp_drv.ver_res  = 600;
  disp_drv.flush_cb = lvgl_flush_cb;
  disp_drv.draw_buf = &draw_buf_desc;
  lv_disp_drv_register(&disp_drv);

  /* Touch init */
  lv_indev_drv_init(&indev_drv);
  indev_drv.type     = LV_INDEV_TYPE_POINTER;
  indev_drv.read_cb  = lvgl_touch_cb;
  lv_indev_drv_register(&indev_drv);

  /* Build gauge UI */
  gauge_cluster_init();
  gauge_cluster_update(sim);

  Serial.println("Ready.");
}

/* ── loop() ──────────────────────────────────────────────────────── */
static uint32_t last_update = 0;

void loop()
{
  lv_timer_handler();  // drive LVGL

  uint32_t now = millis();
  if (now - last_update >= 50) {    // update gauges at ~20 Hz
    last_update = now;
    simulate_data();
    gauge_cluster_update(sim);
  }
}
