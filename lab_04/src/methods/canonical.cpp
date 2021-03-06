#include <cmath>
#include "canonical.hpp"

void canonical_circle(drawArea &area, point &c, float r, bool draw) {
    for (float x = 0; x < (r / sqrtf(2.0f)) + 1; x++) {
        float y = roundf(sqrtf(r*r - x*x));

        if (draw) {
            plot_circle(area, c.x, x + c.x, c.y, y + c.y);
        }
    }
}

void canonical_ellipse(drawArea &area, point &c, float a, float b, bool draw) {
    for (float x = 0; x <= a + 1; x++) {
        float y = roundf(b * sqrtf(1.0f - (x * x) / (a * a)));

        if (draw)
            plot_ellipse(area, c.x, x, c.y, y);
    }

    for (float y = 0; y <= b; y++) {
        float x = a * sqrtf(1.0f - (y * y) / (b * b));

        if (draw)
            plot_ellipse(area, c.x, x, c.y, y);
    }
}
