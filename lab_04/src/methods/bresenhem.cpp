#include <cmath>
#include "bresenhem.hpp"

void bresenhem_circle(drawArea &area, point &c, float r, bool draw) {
    float x = 0;
    float y = r;

    float d = 2 - 2 * r;

    if (draw)
        plot_circle(area, c.x, x, c.y, y);

    while (y >= x) {
        if (d <= 0) {
            float buf = 2 * d + 2 * y - 1;
            x++;

            if (buf <= 0)
                d = d + 2 * x + 1;
            else {
                d = d + 2 * x - 2 * y + 2;
                y--;
            }
        } else {
            float buf = 2 * d - 2 * x - 1;
            y--;

            if (buf >= 0)
                d = d - 2 * y + 1;
            else {
                d = d + 2 * x - 2 * y + 2;
                x++;
            }
        }

        if (draw)
            plot_circle(area, c.x, x, c.y, y);
    }
}

void bresenhem_ellipse(drawArea &area, point &c, float a, float b, bool draw) {
    float x = 0;
    float y = b;

    a = a * a;
    float d = roundf(b * b / 2.0f - a * b * 2.0f + a / 2.0f);
    b = b * b;

    if (draw)
        plot_ellipse(area, c.x, x, c.y, y);

    while (y > 0) {
        if (d <= 0) {
            float buf = 2.0f * d + 2.0f * a * y - a;
            x++;

            if (buf <= 0)
                d = d + 2.0f * b * x + b;
            else {
                y--;
                d = d + 2.0f * b * x - 2.0f * a * y + a + b;
            }
        } else {
            float buf = 2.0f * d - 2.0f * b * x - b;
            y--;

            if (buf >= 0)
                d = d - 2.0f * y * a + a;
            else {
                d = d + 2.0f * x * b - 2.0f * y * a + a + b;
                x--;
            }
        }

        if (draw)
            plot_ellipse(area, c.x, x, c.y, y);
    }
}
