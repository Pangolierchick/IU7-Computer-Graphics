#include <cmath>
#include "parametric.hpp"

void parametric_circle(drawArea &area, point &c, float r, bool draw) {
    float l = roundf(M_PI * r / 2.0) / 2.0;

    for (float i = 0; i <= l; i++) {
        float x = roundf(r * cosf(i / r));
        float y = roundf(r * sinf(i / r));

        if (draw)
            plot_circle(area, c.x, x, c.y, y);
    }
}

void parametric_ellipse(drawArea &area, point &c, float a, float b, bool draw) {
    float m = std::max(a, b);
    float l = roundf(M_PI * m / 2.0f);

    for (float i = 0; i <= l; i++) {
        float x = roundf(a * cosf(i / m));
        float y = roundf(b * sinf(i / m));

        if (draw)
            plot_ellipse(area, c.x, x, c.y, y);
    }
}
