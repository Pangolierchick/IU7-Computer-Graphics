#include <cmath>
#include "canonical.hpp"

void canonical_circle(drawArea &area, point &c, float r, bool draw=true) {
    for (float x = 0; x < r + 1.5; x++) {
        float y = roundf(sqrtf(r*r - x*x));

        if (draw)
            plot_circle(area, c.x, x, c.y, y);
    }
}

void canonical_ellipse(drawArea &area, point &c, float a, float b, bool draw=true) {
    for (float x = 0; x <= a + 1; x++) {
        float y = roundf(b * sqrtf(1.0f - (x * x) / (a * a)));

        if (draw)
            plot_ellipse(area, c.x, x, c.y, y);
    }

    for (float y = 0; y <= b; y++) {
        float x = roundf(a * sqrt(1.0f - (y * y) / (b * b)));

        if (draw)
            plot_ellipse(area, c.x, x, c.y, y);
    }
}
