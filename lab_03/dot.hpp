#pragma once

#include "color.hpp"

using dot_t = struct dot;

struct dot {
    public:
        dot(): x(0), y(0) {}
        dot(double x, double y): x(x), y(y) {}
        dot(double x, double y, Color c): x(x), y(y), color(c) {}

        double getX() const { return this->x; }
        double getY() const { return this->y; }

        void setX(double x) { this->x = x; }
        void setY(double y) { this->y = y; }

        Color& getColor() { return color; }

    private:
        double x;
        double y;
        Color color;
};



