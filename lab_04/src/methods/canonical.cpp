#include <cmath>
#include "canonical.hpp"

void canonical_circle(drawArea &area, point &c, float r, bool draw) {
    for (int x = 0; x < (r / sqrtf(2.0f)) + 1; x++) {
        int y = sqrtf(r*r - x*x);

        if (draw) {
            plot_circle(area, c.x, x + c.x, c.y, y + c.y);
        }
    }
}

void canonical_ellipse(drawArea &area, point &c, float a, float b, bool draw) {
    for (int x = 0; x <= a + 1; x++) {
        int y = b * sqrtf(1.0f - (x * x) / (a * a));

        if (draw)
            plot_ellipse(area, c.x, x, c.y, y);
    }

    for (int y = 0; y <= b; y++) {
        int x = a * sqrt(1.0f - (y * y) / (b * b));

        if (draw)
            plot_ellipse(area, c.x, x, c.y, y);
    }
}
