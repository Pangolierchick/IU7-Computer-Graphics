#pragma once

using color_t = struct color;

struct color {
    public:
        color(int r, int g, int b): red(r), green(g), blue(b) {}
        color(const color& c): red(c.red), green(c.green), blue(c.blue) {}
        color(color&& c): red(c.red), green(c.green), blue(c.blue) {}

        color_t operator+=(const color_t& c) {
            this->red += c.red;
            this->green += c.green;
            this->blue += c.blue;

            return *this;
        }

        int Red() { return red; }
        int Green() { return green; }
        int Blue() { return blue; }

    private:
        int red;
        int green;
        int blue;
};

