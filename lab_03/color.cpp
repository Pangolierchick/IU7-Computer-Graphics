#include "color.hpp"

void Color::presetColor(colors_presets_t c) {
    switch (c) {
        case PURPLE:
            red   = 0x94;
            green = 0x00;
            blue  = 0xd3;
            break;
        
        case BACKGROUND:
            red   = 0xff;
            green = 0xff;
            blue  = 0xff;
            break;
        case BLACK:
            red = 0;
            green = 0;
            blue = 0;
            break;
        case BLUE:
            red = 0;
            green = 0;
            blue = 0xff;
            break;
        case GREEN:
            red = 0;
            green = 0xff;
            blue = 0;
            break;
    }
}
