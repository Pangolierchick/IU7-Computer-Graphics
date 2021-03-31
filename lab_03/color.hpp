#pragma once

typedef enum colors_presets {
    PURPLE,
    BLACK,
    BLUE,
    GREEN,
    BACKGROUND
} colors_presets_t;


class Color {
    public:
        Color(): red(0), green(0), blue(0), alpha(255) {}
        Color(int a): red(0), green(0), blue(0), alpha(a) {}
        Color(int r, int g, int b, int a=255): red(r), green(g), blue(b), alpha(a) {}

        Color operator+=(const Color& c) {
            // this->red += c.red;
            // this->green += c.green;
            // this->blue += c.blue;

            this->alpha += c.alpha;

            checkForExceed(*this);

            return *this;
        }

        Color operator+() {
            Color temp(red, green, blue);

            // temp.red = red + c.red;
            // temp.green = green + c.green;
            // temp.blue = blue + c.blue;

            checkForExceed(temp);

            return temp;
        }

        int Red() { return red; }
        int Green() { return green; }
        int Blue() { return blue; }
        int Alpha() { return alpha; }

        void setRed(int v) { red = v; checkForExceed(*this); }
        void setGreen(int v) { green = v; checkForExceed(*this); }
        void setBlue(int v) { blue = v; checkForExceed(*this); }
        void setAlpha(int v) { alpha = v; checkForExceed(*this); }
    
        void presetColor(colors_presets_t c);

    private:
        void checkForExceed(Color &c) {
            if (c.red > 255)
                c.red = 255;

            if (c.green > 255)
                c.green = 255;

            if (c.blue > 255)
                c.blue = 255;

            if (c.alpha > 255)
                c.alpha = 255;
            
            if (c.alpha < 0) {
                c.alpha = 0;
            }
        }
        int red;
        int green;
        int blue;
        int alpha;
};




