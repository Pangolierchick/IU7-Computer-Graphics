#include <algorithm>
#include <cmath>
#include <vector>
#include "wu.hpp"
#include "logger.h"

static void wu_swap(double &x, double &y, int steep) {
    if (steep) {
        std::swap(x, y);
    }
}

static void get_endpoints(double x, double y, double m, double *px, double *py) {
    double x_e = (int) x;
    double y_e = y + (x_e - x) * m;

    *px = x_e;
    *py = y_e;
}

line_t wu(dot_t &sd, dot_t &ed, Color &color) {
    double x_start = sd.getX();
    double y_start = sd.getY();

    double x_end = ed.getX();
    double y_end = ed.getY();

    double dx = x_end - x_start;
    double dy = y_end - y_start;

    auto steep = fabs(dx) < fabs(dy);

    if (steep) {
        std::swap(x_start, y_start);
        std::swap(x_end, y_end);
        std::swap(dx, dy);
    }

    if (x_end < x_start) {
        std::swap(x_start, x_end);
        std::swap(y_start, y_end);
    }

    double m = dy / dx;
    double intery = y_start + ((int) x_start) * m;

    std::vector<dot_t> dots;

    double px;
    double py;

    get_endpoints(x_start, y_start, m, &px, &py);

    double x_s = px + 1;

    double y_fract;
    double y_int_part;

    double y_e = y_start + (round(x_start) - x_start) * m;
    double x_gap = (int) (x_start + 0.5);

    y_fract = modf(y_e, &y_int_part);

    double dens1;
    double dens2;

    dens1 = y_fract * x_gap;
    dens2 = y_int_part * x_gap;


    Color color1(255.0 * dens2, 255.0 * dens2, 255.0);
    Color color2(255.0 * dens1, 255.0 * dens1, 255.0);

    wu_swap(px, py, steep);

    dots.emplace_back(px, py, color + color1);
    dots.emplace_back(px, py, color + color2);

    get_endpoints(x_end, y_end, m, &px, &py);

    double x_e = px;

    y_e = y_end + (round(x_end) - x_end) * m;
    x_gap = (int) (x_end + 0.5);

    y_fract = modf(y_e, &y_int_part);

    dens1 = y_fract * x_gap;
    dens2 = y_int_part * x_gap;

    wu_swap(px, py, steep);

    color1.setRed(255.0 * dens2);
    color1.setGreen(255.0 * dens2);
    color1.setBlue(255.0);

    color2.setRed(255.0 * dens1);
    color2.setGreen(255.0 * dens1);
    color2.setBlue(255.0);

    DBG_PRINT("Dens1: %lf\n", dens1);
    DBG_PRINT("Dens2: %lf\n", dens2);

    DBG_PRINT("Color1: %x %x %x\n", color1.Red(), color1.Green(), color1.Blue());
    DBG_PRINT("Color1: %x %x %x\n", color2.Red(), color2.Green(), color2.Blue());


    dots.emplace_back(px, py, color + color1);
    dots.emplace_back(px, py, color + color2);

    while (x_s < x_e) {
        double y = (int) intery;

        double dens1;
        double dens2;

        dens2 = modf(intery, &dens1);

        Color c1(255.0 * dens2, 255.0 * dens2, 255.0);
        Color c2(255.0 * dens1, 255.0 * dens1, 255.0);

        wu_swap(x_s, y, steep);
        dots.emplace_back(x_s, y, color + c1);

        y++;

        wu_swap(x_s, y, steep);
        dots.emplace_back(x_s, y, color + c2);

        intery += m;
        x_s++;
    }

    line_t line(dots);

    return line;
}
