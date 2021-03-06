#include <cmath>
#include <vector>
#include "dda.hpp"
#include "logger.h"

line_t dda(dot_t& sd, dot_t& ed, Color& color) {
    auto dx = ed.getX() - sd.getX();
    auto dy = ed.getY() - sd.getY();

    float l;

    if (fabs(dx) > fabs(dy))
        l = fabs(dx);
    else
        l = fabs(dy);
    
    dx /= l;
    dy /= l;

    float x = sd.getX();
    float y = sd.getY();

    std::vector<dot_t> dots;

    TRACE_PRINT("Pushing back: %lf %lf\n", x, y);

    dots.emplace_back(x, y, color);

    int i = 0;

    TRACE_PRINT("L is %lf\n", l);
    while (i < l) {
        x += dx;
        y += dy;

        TRACE_PRINT("Pushing back: %lf %lf\n", x, y);
        dots.emplace_back(round(x), round(y), color);

        i++;
    }

    line_t line(dots);

    return line;
}
