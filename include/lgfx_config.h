/**
 * lgfx_config.h — LovyanGFX driver for Waveshare ESP32-S3-Touch-LCD-7
 *
 * Display:  1024 x 600, 16-bit RGB565, RGB parallel bus
 * Touch:    GT911 via I2C
 *
 * IMPORTANT: Verify pin numbers against your specific board revision.
 * Waveshare schematic: https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-7
 */
#pragma once

#define LGFX_USE_V1
#include <LovyanGFX.hpp>

class LGFX : public lgfx::LGFX_Device {
public:
  lgfx::Bus_RGB       _bus_instance;
  lgfx::Panel_RGB     _panel_instance;
  lgfx::Touch_GT911   _touch_instance;

  LGFX() {
    /* ── RGB bus ──────────────────────────────────── */
    {
      auto cfg = _bus_instance.config();

      cfg.panel         = &_panel_instance;

      cfg.pin_d0  = GPIO_NUM_8;   // B0
      cfg.pin_d1  = GPIO_NUM_3;   // B1
      cfg.pin_d2  = GPIO_NUM_46;  // B2
      cfg.pin_d3  = GPIO_NUM_9;   // B3
      cfg.pin_d4  = GPIO_NUM_1;   // B4
      cfg.pin_d5  = GPIO_NUM_5;   // G0
      cfg.pin_d6  = GPIO_NUM_6;   // G1
      cfg.pin_d7  = GPIO_NUM_7;   // G2
      cfg.pin_d8  = GPIO_NUM_15;  // G3
      cfg.pin_d9  = GPIO_NUM_16;  // G4
      cfg.pin_d10 = GPIO_NUM_4;   // G5
      cfg.pin_d11 = GPIO_NUM_45;  // R0
      cfg.pin_d12 = GPIO_NUM_48;  // R1
      cfg.pin_d13 = GPIO_NUM_47;  // R2
      cfg.pin_d14 = GPIO_NUM_21;  // R3
      cfg.pin_d15 = GPIO_NUM_14;  // R4

      cfg.pin_henable = GPIO_NUM_40; // DE
      cfg.pin_vsync   = GPIO_NUM_41; // VSYNC
      cfg.pin_hsync   = GPIO_NUM_39; // HSYNC
      cfg.pin_pclk    = GPIO_NUM_0;  // PCLK

      cfg.freq_write  = 15000000;    // 15 MHz — reduce if display is unstable
      cfg.hsync_polarity    = 0;
      cfg.hsync_front_porch = 8;
      cfg.hsync_pulse_width = 4;
      cfg.hsync_back_porch  = 8;
      cfg.vsync_polarity    = 0;
      cfg.vsync_front_porch = 8;
      cfg.vsync_pulse_width = 4;
      cfg.vsync_back_porch  = 8;
      cfg.pclk_idle_high    = 1;

      _bus_instance.config(cfg);
      _panel_instance.setBus(&_bus_instance);
    }

    /* ── Panel ─────────────────────────────────────── */
    {
      auto cfg = _panel_instance.config();
      cfg.memory_width  = 1024;
      cfg.memory_height = 600;
      cfg.panel_width   = 1024;
      cfg.panel_height  = 600;
      cfg.offset_x      = 0;
      cfg.offset_y      = 0;
      _panel_instance.config(cfg);
    }

    /* ── Backlight (GPIO2) ──────────────────────────── */
    {
      auto cfg = _panel_instance.config_detail();
      cfg.pin_cs           = -1;
      cfg.pin_rst          = -1;
      cfg.pin_busy         = -1;
      _panel_instance.config_detail(cfg);
    }

    /* ── Touch (GT911, I2C0) ────────────────────────── */
    {
      auto cfg = _touch_instance.config();
      cfg.x_min        = 0;
      cfg.x_max        = 1023;
      cfg.y_min        = 0;
      cfg.y_max        = 599;
      cfg.pin_int      = GPIO_NUM_38;
      cfg.pin_rst      = GPIO_NUM_NC;
      cfg.bus_shared   = false;
      cfg.offset_rotation = 0;
      cfg.i2c_port     = I2C_NUM_0;
      cfg.i2c_addr     = 0x5D;
      cfg.pin_sda      = GPIO_NUM_19;
      cfg.pin_scl      = GPIO_NUM_20;
      cfg.freq         = 400000;
      _touch_instance.config(cfg);
      _panel_instance.setTouch(&_touch_instance);
    }

    setPanel(&_panel_instance);
  }
};
