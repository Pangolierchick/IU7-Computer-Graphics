#include <cmath>
#include <vector>
#include "dda.hpp"

line_t dda(dot_t& sd, dot_t& ed, color_t& color) {
    auto dx = ed.getX() - sd.getX();
    auto dy = ed.getY() - sd.getY();

    double l;

    if (fabs(dx) > fabs(dy))
        l = fabs(dx);
    else
        l = fabs(dy);
    
    dx /= l;
    dy /= l;

    double x = sd.getX();
    double y = sd.getY();

    std::vector<dot_t> dots;

    dots.emplace_back(x, y, color);

    int i = 0;
    while (i < l) {
        x += dx;
        y += dy;

        dots.emplace_back(x, y, color);

        i++;
    }

    return dots;
}
