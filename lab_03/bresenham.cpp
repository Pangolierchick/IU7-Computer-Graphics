#include <cmath>
#include <algorithm>
#include "bresenham.hpp"

static inline int signum(double val) {
    if (val < 0)
        return -1;

    return 1;
}

line_t bresenham_int(dot_t& sd, dot_t& ed, color_t& color) {
    auto x_start = sd.getX();
    auto y_start = sd.getY();
    
    auto x_end = ed.getX();
    auto y_end = ed.getY();

    int dx = x_end - x_start;
    int dy = y_end - y_start;

    auto x_sign = signum(dx);
    auto y_sign = signum(dy);

    dx = abs(dx);
    dy = abs(dy);

    int xx;
    int xy;
    int yx;
    int yy;

    if (dx > dy) {
        xx = x_sign;
        xy = 0;
        yx = 0;
        yy = y_sign;
    } else {
        std::swap(dx, dy);
        xx = 0;
        xy = y_sign;
        yx = x_sign;
        yy = 0;
    }

    int e = 2 * dy - dx;
    int y = 0;

    std::vector<dot_t> dots;

    int x = 0;
    while (x < dx + 1) {
        dot_t dot(x_start + x * xx + y * yx, y_start + x * xy + y * yy, color);

        dots.push_back(dot);

        if (e >= 0) {
            y++;
            e -= 2 * dx;
        }

        e += 2 * dy;

        x++;
    }

    line_t line(dots);

    return line;
}


line_t bresenham_double(dot_t& sd, dot_t& ed, color_t& color) {
    auto x_start = sd.getX();
    auto y_start = sd.getY();
    
    auto x_end = ed.getX();
    auto y_end = ed.getY();

    int dx = x_end - x_start;
    int dy = y_end - y_start;

    auto x_sign = signum(dx);
    auto y_sign = signum(dy);

    dx = abs(dx);
    dy = abs(dy);

    int xx;
    int xy;
    int yx;
    int yy;

    if (dx > dy) {
        xx = x_sign;
        xy = 0;
        yx = 0;
        yy = y_sign;
    } else {
        std::swap(dx, dy);
        xx = 0;
        xy = y_sign;
        yx = x_sign;
        yy = 0;
    }

    auto m = dy / dx;
    auto e = m - 0.5;
    auto y = 0;

    std::vector<dot_t> dots;

    int x = 0;
    while (x < dx + 1) {
        dot_t dot(x_start + x * xx + y * yx, y_start + x * xy + y * yy, color);

        dots.push_back(dot);

        if (e >= 0) {
            y++;
            e--;
        }

        e += m;

        x++;
    }

    line_t line(dots);

    return line;
}

line_t bresenham_antialiased(dot_t& sd, dot_t& ed, color_t& color) {
    auto x_start = sd.getX();
    auto y_start = sd.getY();
    
    auto x_end = ed.getX();
    auto y_end = ed.getY();

    int dx = x_end - x_start;
    int dy = y_end - y_start;

    auto x_sign = signum(dx);
    auto y_sign = signum(dy);

    dx = abs(dx);
    dy = abs(dy);

    int xx;
    int xy;
    int yx;
    int yy;

    if (dx > dy) {
        xx = x_sign;
        xy = 0;
        yx = 0;
        yy = y_sign;
    } else {
        std::swap(dx, dy);
        xx = 0;
        xy = y_sign;
        yx = x_sign;
        yy = 0;
    }

    auto m = dy / dx;
    auto e = 0.5;
    auto w = 1;
    auto y = 0;

    std::vector<dot_t> dots;

    int x = 0;
    while (x < dx + 1) {
        color_t new_color(0xff * e, 0xff * e, 0xff);
        new_color += color;

        dot_t dot(x_start + x * xx + y * yx, y_start + x * xy + y * yy, new_color);

        dots.push_back(dot);

        if (e >= w - m) {
            y++;
            e -= w;
        }
        e += m;

        x++;
    }

    line_t line(dots);

    return line;
}
