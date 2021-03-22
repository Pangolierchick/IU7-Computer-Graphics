#pragma once

#include "color.hpp"

using dot_t = struct dot;

struct dot {
    public:
        dot(): x(0), y(0) {}
        dot(float x, float y): x(x), y(y) {}
        dot(float x, float y, Color c): x(x), y(y), color(c) {}

        float getX() const { return this->x; }
        float getY() const { return this->y; }

        void setX(float x) { this->x = x; }
        void setY(float y) { this->y = y; }

        Color& getColor() { return color; }

    private:
        float x;
        float y;
        Color color;
};



