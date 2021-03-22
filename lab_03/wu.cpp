#include <algorithm>
#include <cmath>
#include <vector>
#include "wu.hpp"
#include "logger.h"

static float fpart(float x) {
    return x - (int) x;
}

static float rfpart(float x) {
    return 1 - fpart(x);
}

static float ipart(float x) {
    return x - fpart(x);
}

static float myround(float x) {
    return ipart(x + 0.5);
}

static void wu_swap(float &x, float &y, int steep) {
    if (steep) {
        std::swap(x, y);
    }
}

static void get_endpoints(float x, float y, float m, float *px, float *py) {
    float x_e = round(x);
    float y_e = y + (x_e - x) * m;

    *px = round(x_e);
    *py = round(y_e);
}

line_t wu(dot_t &sd, dot_t &ed, Color &color) {
    float x_start = sd.getX();
    float y_start = sd.getY();

    float x_end = ed.getX();
    float y_end = ed.getY();

    const bool steep = abs(y_end - y_start) > abs(x_end - x_start);

    if (steep) {
        std::swap(x_start, y_start);
        std::swap(x_end, y_end);
    }

    if (x_end < x_start) {
        std::swap(x_start, x_end);
        std::swap(y_start, y_end);
    }

    const float dx = x_end - x_start;
    const float dy = y_end - y_start;
    const float gradient = (dx == 0) ? 1 : (dy / dx);

    std::vector<dot_t> dots;

    int xpx11;
    float intery;

    {
        float xend = round(x_start);
        float yend = y_start + gradient * (xend - x_start);
        float xgap = rfpart(x_start + 0.5);
        
        xpx11 = int(xend);

        const int ypx11 = ipart(yend);
        if (steep) {
            Color c = color;
            c.setAlpha(255 * rfpart(y_end) * xgap);
    
            dots.emplace_back(ypx11, xpx11, c);
            c.setAlpha(255 * fpart(y_end) * xgap);
    
            dots.emplace_back(ypx11 + 1, xpx11, c);
        } else {
            Color c = color;
            c.setAlpha(255 * rfpart(yend) * xgap);
    
            dots.emplace_back(xpx11, ypx11, c);
            c.setAlpha(255 * fpart(yend) * xgap);
    
            dots.emplace_back(xpx11 + 1, ypx11, c);

        }
        intery = yend + gradient;
    }

    int xpx12;
    {
        float xend = round(x_end);
        float yend = y_end + gradient * (xend - x_end);
        float xgap = rfpart(x_end + 0.5);
        
        xpx12 = int(xend);
        
        int ypx12 = ipart(yend);

        if (steep) {
            Color c = color;
            c.setAlpha(255 * rfpart(yend) * xgap);
            dots.emplace_back(ypx12, xpx12, c);

            c.setAlpha(255 * fpart(yend) * xgap);
            dots.emplace_back(ypx12 + 1, xpx12, c);
        } else {
            Color c = color;
            c.setAlpha(255 * rfpart(yend) * xgap);
            dots.emplace_back(xpx12, ypx12, c);
            c.setAlpha(255 * fpart(yend) * xgap);
            dots.emplace_back(xpx12, ypx12 + 1, c);
        }
    }

    if (steep) {
        for (int x = xpx11 + 1; x < xpx12; x++) {
            Color c = color;
            
            c.setAlpha(rfpart(intery) * 255);
            dots.emplace_back(ipart(intery), x, c);
            
            c.setAlpha(255 * fpart(intery));
            dots.emplace_back(ipart(intery) + 1, x, c);
            intery += gradient;
        }
    } else {
        for (int x = xpx11 + 1; x < xpx12; x++) {
            Color c = color;

            c.setAlpha(255 * rfpart(intery));
            dots.emplace_back(x, ipart(intery), c);
            
            c.setAlpha(255 * fpart(intery));
            dots.emplace_back(x, ipart(intery) + 1, c);
            intery += gradient;
        }
    }

    line_t line(dots);

    return line;
}
