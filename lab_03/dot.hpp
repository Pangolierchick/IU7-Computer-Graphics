#pragma once

#include "color.hpp"

using dot_t = struct dot;

struct dot {
    public:
        dot(double x, double y, color_t c): x(x), y(y), color(c) {}

        double getX() const { return this->x; }
        double getY() const { return this->y; }

        void setX(double x) { this->x = x; }
        void setY(double y) { this->y = y; }

        color_t& getColor() { return color; }

    private:
        double x;
        double y;
        color_t color;
};



