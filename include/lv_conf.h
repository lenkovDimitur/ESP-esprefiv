/**
 * lv_conf.h — LVGL 8.3 configuration for ESP32-S3 + 1024x600 display
 */
#if 1  /* Set this to "1" to enable */

#ifndef LV_CONF_H
#define LV_CONF_H

#include <stdint.h>

/*====================
   COLOR SETTINGS
 *====================*/
#define LV_COLOR_DEPTH 16
#define LV_COLOR_16_SWAP 0

/*====================
   MEMORY SETTINGS
 *====================*/
/* LVGL internal heap — use PSRAM if available */
#define LV_MEM_CUSTOM 0
#define LV_MEM_SIZE   (256U * 1024U)  /* 256 KB from internal RAM */

/*====================
   HAL SETTINGS
 *====================*/
#define LV_DISP_DEF_REFR_PERIOD  16   /* ~60 fps */
#define LV_INDEV_DEF_READ_PERIOD 30

/*====================
   FEATURE CONFIGURATION
 *====================*/
#define LV_DPI_DEF 130

/* Drawing */
#define LV_DRAW_COMPLEX 1
#define LV_SHADOW_CACHE_SIZE 0

/* Text */
#define LV_TXT_ENC LV_TXT_ENC_UTF8
#define LV_SPRINTF_CUSTOM 0

/*====================
   WIDGETS
 *====================*/
#define LV_USE_ARC         1
#define LV_USE_BAR         1
#define LV_USE_BTN         1
#define LV_USE_CANVAS      1
#define LV_USE_IMG         1
#define LV_USE_LABEL       1
#define LV_USE_LINE        1
#define LV_USE_METER       1
#define LV_USE_OBJ         1

/* Disable unneeded widgets to save flash */
#define LV_USE_ANIMIMG     0
#define LV_USE_BTNMATRIX   0
#define LV_USE_CALENDAR    0
#define LV_USE_CHART       0
#define LV_USE_CHECKBOX    0
#define LV_USE_COLORWHEEL  0
#define LV_USE_DROPDOWN    0
#define LV_USE_IMGBTN      0
#define LV_USE_KEYBOARD    0
#define LV_USE_LED         1
#define LV_USE_LIST        0
#define LV_USE_MENU        0
#define LV_USE_MSGBOX      0
#define LV_USE_ROLLER      0
#define LV_USE_SLIDER      0
#define LV_USE_SPAN        0
#define LV_USE_SPINBOX     0
#define LV_USE_SPINNER     0
#define LV_USE_SWITCH      0
#define LV_USE_TABLE       0
#define LV_USE_TABVIEW     0
#define LV_USE_TEXTAREA    0
#define LV_USE_TILEVIEW    0
#define LV_USE_WIN         0

/*====================
   THEMES
 *====================*/
#define LV_USE_THEME_DEFAULT 1
#define LV_THEME_DEFAULT_DARK 1
#define LV_USE_THEME_BASIC 0
#define LV_USE_THEME_MONO  0

/*====================
   FONTS
 *====================*/
#define LV_FONT_MONTSERRAT_12 1
#define LV_FONT_MONTSERRAT_14 1
#define LV_FONT_MONTSERRAT_16 1
#define LV_FONT_MONTSERRAT_20 1
#define LV_FONT_MONTSERRAT_24 1
#define LV_FONT_MONTSERRAT_32 1
#define LV_FONT_MONTSERRAT_48 1
#define LV_FONT_DEFAULT &lv_font_montserrat_14

/*====================
   LOGGING / DEBUG
 *====================*/
#define LV_USE_LOG 0
#define LV_USE_ASSERT_NULL          1
#define LV_USE_ASSERT_MALLOC        1
#define LV_USE_ASSERT_STYLE         0
#define LV_USE_ASSERT_MEM_INTEGRITY 0
#define LV_USE_ASSERT_OBJ           0

/*====================
   ANIMATION
 *====================*/
#define LV_USE_ANIMATION 1

#endif /* LV_CONF_H */
#endif /* End of "Content enable" */
