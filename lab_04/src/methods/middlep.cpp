#include <cmath>
#include "middlep.hpp"

void middle_circle(drawArea &area, point &c, float r, bool draw) {
    float x = 0;
    float y = r;

    float d = 1.25f - r;

    while (x <= y) {
        if (draw)
            plot_circle(area, c.x, x, c.y, y);
        
        x++;

        if (d < 0)
            d += 2 * x + 1;
        else {
            d += 2 * x - 2 * y + 5;
            y--;
        }
    }
}


void middle_ellipse(drawArea &area, point &c, float a, float b, bool draw) {
    float x = 0;
    float y = b;
    
    float a2 = a * a;
    float b2 = b * b;

    float ad = 2 * a2;
    float bd = 2 * b2;

    float mid = a2 / sqrtf(a2 + b2);
    float f = b2 - a2 * b + 0.25f * a2;

    float dx = 0;
    float dy = -ad * y;

    while (x <= mid) {
        if (draw)
            plot_ellipse(area, c.x, x, c.y, y);

        if (f > 0) {
            y--;
            dy += ad;
            f += dy;
        }

        x++;
        dx += bd;
        f += dx + b2;
    }

    f += -b2 * (x + 0.75f) - a2 * (y - 0.75f);

    while (y >= 0) {
        if (draw)
            plot_ellipse(area, c.x, x, c.y, y);
        
        if (f <= 0) {
            x++;
            dx += bd;
            f  += dx;
        }

        y--;
        dy += ad;
        f += a2 + dy;
    }
}
