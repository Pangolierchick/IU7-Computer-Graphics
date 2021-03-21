#include <algorithm>
#include <cmath>
#include <vector>
#include "wu.hpp"
#include "logger.h"

static double fpart(double x) {
    return x - (int) x;
}

static double rfpart(double x) {
    return 1 - fpart(x);
}

static void wu_swap(double &x, double &y, int steep) {
    if (steep) {
        std::swap(x, y);
    }
}

static void get_endpoints(double x, double y, double m, double *px, double *py) {
    double x_e = round(x);
    double y_e = y + (x_e - x) * m;

    *px = round(x_e);
    *py = round(y_e);
}

line_t wu(dot_t &sd, dot_t &ed, Color &color) {
    double x_start = sd.getX();
    double y_start = sd.getY();

    double x_end = ed.getX();
    double y_end = ed.getY();

    double dx = x_end - x_start;
    double dy = y_end - y_start;

    int steep = fabs(dx) < fabs(dy);

    if (steep) {
        std::swap(x_start, y_start);
        std::swap(x_end, y_end);
        std::swap(dx, dy);
    }

    if (x_end < x_start) {
        std::swap(x_start, x_end);
        std::swap(y_start, y_end);
    }


    DBG_PRINT("xs = %lf\tys = %lf\n", x_start, y_start);
    double m = dy / dx;
    double intery = y_start + rfpart(x_start) * m;

    DBG_PRINT("Intery = %lf\n", intery);

    std::vector<dot_t> dots;

    double px;
    double py;

    get_endpoints(x_start, y_start, m, &px, &py);

    double x_s = px + 1;

    double y_fract;
    double y_int_part;

    double y_e = y_start + (round(x_start) - x_start) * m;
    double x_gap = rfpart((x_start + 0.5));

    double dens1;
    double dens2;

    dens1 = rfpart(y_e) * x_gap;
    dens2 = fpart(y_e)  * x_gap;


    Color color1(255.0 * dens2, 255.0 * dens2, 255.0);
    Color color2(255.0 * dens1, 255.0 * dens1, 255.0);

    wu_swap(px, py, steep);

    DBG_PRINT("px, py %lf %lf\n", px, py);

    dots.emplace_back(px, py, color + color1);
    dots.emplace_back(px, py, color + color2);

    wu_swap(px, py, steep);

    get_endpoints(x_end, y_end, m, &px, &py);

    double x_e = px;

    y_e = y_end + (round(x_end) - x_end) * m;
    x_gap = rfpart(x_end + 0.5);

    dens1 = rfpart(y_e) * x_gap;
    dens2 = fpart(y_e)  * x_gap;

    color1.setRed(255.0 * dens2);
    color1.setGreen(255.0 * dens2);
    color1.setBlue(255.0);

    color2.setRed(255.0 * dens1);
    color2.setGreen(255.0 * dens1);
    color2.setBlue(255.0);

    wu_swap(px, py, steep);

    DBG_PRINT("px, py %lf %lf\n", px, py);

    dots.emplace_back(px, py, color + color1);
    dots.emplace_back(px, py, color + color2);
    wu_swap(px, py, steep);

    DBG_PRINT("xs and xe: %lf %lf\n", x_s, x_e);

    while (x_s < x_e) {
        double x = x_s;
        double y = round(intery);

        double dens1 = rfpart(intery) * x_gap;
        double dens2 = fpart(intery)  * x_gap;

        Color c1(255.0 * dens2, 255.0 * dens2, 255.0);
        Color c2(255.0 * dens1, 255.0 * dens1, 255.0);


        wu_swap(x, y, steep);
        DBG_PRINT("#1 x_s, y %lf %lf\n", x_s, y);
        dots.emplace_back(x, y, color + c1);

        y++;
        DBG_PRINT("#2 x_s, y %lf %lf\n", x_s, y);
        dots.emplace_back(x, y, color + c2);
        wu_swap(x, y, steep);
        y--;

        DBG_PRINT("y = %lf\n", y);

        intery += m;
        x_s++;
    }

    line_t line(dots);

    return line;
}
