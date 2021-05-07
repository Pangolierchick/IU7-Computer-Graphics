#include <cmath>
#include "bresenhem.hpp"
#include "logger.h"

void bresenhem_circle(drawArea &area, point &c, float r, bool draw) {
    int x = 0;
    int y = r;

    int d = 2 * (1 - r);

    if (draw) 
        plot_circle(area, c.x, x + c.x, c.y, y + c.y);

    while (y >= x) {
        if (d <= 0) {
            int buf = 2 * d + 2 * y - 1;
            x++;

            if (buf <= 0)
                d = d + 2 * x + 1;
            else {
                d = d + 2 * x - 2 * y + 2;
                y--;
            }
        } else {
            int buf = 2 * d - 2 * x - 1;
            y--;

            if (buf >= 0)
                d = d - 2 * y + 1;
            else {
                d = d + 2 * x - 2 * y + 2;
                x++;
            }
        }


        if (draw) 
            plot_circle(area, c.x, x + c.x, c.y, y + c.y);
    }
}

void bresenhem_ellipse(drawArea &area, point &c, float a, float b, bool draw) {
    int x = 0;
    int y = b;

    a = a * a;
    int d = b * b / 2.0f - a * b * 2 + a / 2.0f;
    b = b * b;

    if (draw)
        plot_ellipse(area, c.x, x, c.y, y);

    while (y > 0) {
        if (d <= 0) {
            int buf = 2.0f * d + 2.0f * a * y - a;
            x++;

            if (buf <= 0)
                d = d + 2.0f * b * x + b;
            else {
                y--;
                d = d + 2.0f * b * x - 2.0f * a * y + a + b;
            }
        } else {
            int buf = 2.0f * d - 2.0f * b * x - b;
            y--;

            if (buf >= 0)
                d = d - 2.0f * y * a + a;
            else {
                d = d + 2.0f * x * b - 2.0f * y * a + a + b;
                x++;
            }
        }

        if (draw)
            plot_ellipse(area, c.x, x, c.y, y);
    }
}
