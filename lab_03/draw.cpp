#include <cmath>
#include <vector>
#include <omp.h>
#include <cstdio>
#include "draw.hpp"
#include "logger.h"
#include "uimanager.hpp"
#include "timer.hpp"

#define PI (333.0 / 106.0)

static inline float move_x_to_center(float x, float width) {
    return x + (width / 2.0);
}

static inline float move_y_to_center(float y, float height) {
    return y + (height / 2.0);
}

static inline float to_radians(float angle) {
    return angle * (PI / 180.0);
}

static void rotate_dot(dot_t& d, float angle, float xc=0, float yc=0) {
    float copy_x = d.getX();
    float copy_y = d.getY();

    d.setX(xc + (copy_x - xc) * cos(angle) - (copy_y - yc) * sin(angle));
    d.setY(yc + (copy_y - yc) * cos(angle) + (copy_x - xc) * sin(angle));
}

static void rotate_coord(float &x, float &y, float angle, float xc=0, float yc=0) {
    float copy_x = x;
    float copy_y = y;

    x = (xc + (copy_x - xc) * cos(angle) - (copy_y - yc) * sin(angle));
    y = (yc + (copy_y - yc) * cos(angle) + (copy_x - xc) * sin(angle));
}

void drawPixel(drawScene_t &scene, dot_t& dot) {
    auto x = dot.getX();
    auto y = dot.getY();
    auto c = dot.getColor();

    QGraphicsScene *draw_scene = scene.getScene();
    QColor color(c.Red(), c.Green(), c.Blue(), c.Alpha());
    QPen pen(color);
    
    draw_scene->addLine(x, y, x, y, pen);
}


void drawLine(drawScene_t &scene, const line_t& line) {
    auto dots = line.getDots();

    for (auto& dot: dots) {
        drawPixel(scene, dot);
    }
}

void drawPixelFromCenter(drawScene_t &scene, dot_t& dot) {
    auto x = dot.getX();
    auto y = dot.getY();
    auto c = dot.getColor();

    QGraphicsScene *draw_scene = scene.getScene();
    QColor color(c.Red(), c.Green(), c.Blue(), c.Alpha());
    QPen pen(color);
    pen.setWidthF(1);

    x = move_x_to_center(x, draw_scene->width());
    y = move_y_to_center(y, draw_scene->height());
    
    draw_scene->addLine(x, y, x + 0.5, y, pen);
}


void drawLineFromCenter(drawScene_t &scene, const line_t& line) {
    auto dots = line.getDots();

    for (auto& dot: dots) {
        drawPixelFromCenter(scene, dot);
    }
}

void drawLibLine(drawScene_t &scene, drawLine_t lineParams) {
    auto x1 = lineParams.d1.getX();
    auto y1 = lineParams.d1.getY();
    auto x2 = lineParams.d2.getX();
    auto y2 = lineParams.d2.getY();
    
    auto cp = lineParams.color;

    Color c;
    c.presetColor(cp);

    QGraphicsScene *draw_scene = scene.getScene();
    QColor color(c.Red(), c.Green(), c.Blue(), c.Alpha());
    QPen pen(color);
    pen.setWidthF(1);

    // x1 = move_x_to_center(x1, draw_scene->width());
    // y1 = move_y_to_center(y1, draw_scene->height());
    // x2 = move_x_to_center(x2, draw_scene->width());
    // y2 = move_y_to_center(y2, draw_scene->height());
    
    draw_scene->addLine(x1, y1, x2, y2, pen);
}

void cleanScreen(drawScene_t &scene) {
    auto draw_scene = scene.getScene();
    draw_scene->clear();
}

float get_len(float x, float y, float xc, float yc) {
    return (sqrt(pow(x - xc, 2) + pow(y - yc, 2)));
}

void drawBundle(drawScene_t &scene, drawBundle_t &bundleParams, drawMethods_t method) {
    float angle = to_radians(bundleParams.angle);

    int iters = 360.0 / bundleParams.angle;

    Color c;
    c.presetColor(bundleParams.color);

    auto draw_scene = scene.getScene();

    dot_t ds(draw_scene->width() / 2.0, draw_scene->height() / 2.0, c);

    std::vector<line_t> lines;
    std::vector<dot_t> right_dots;

    lines.resize(iters + 10);

    float left_c  = (draw_scene->width() / 2.0)  + bundleParams.radius;
    float right_c = (draw_scene->height() / 2.0) + bundleParams.radius;

    for (int i = 0; i < iters; i++) {
        right_dots.emplace_back(left_c, right_c, c);
        rotate_coord(left_c, right_c, angle, ds.getX(), ds.getY());
    }

    #pragma omp parallel for
    for (int i = 0; i < iters; i++) {

        drawLine_t draw_line;
        draw_line.d1 = ds;
        draw_line.d2 = right_dots[i];

        draw_line.color = bundleParams.color;

        line_t line = drawLineManager(method, draw_line);
        lines[i] = line;
    }

    for (int i = 0; i < iters; i++)
        drawLine(scene, lines[i]);
}

void drawLibBundle(drawScene_t &scene, drawBundle_t &bundleParams) {
    float angle = to_radians(bundleParams.angle);

    int iters = 360.0 / bundleParams.angle;

    Color c;
    c.presetColor(bundleParams.color);

    dot_t ds(0, 0, c);
    dot_t de(bundleParams.radius, bundleParams.radius, c);

    for (int i = 0; i < iters; i++) {
        drawLine_t draw_line;
        draw_line.d1 = ds;
        draw_line.d2 = de;
        draw_line.color = bundleParams.color;

        drawLibLine(scene, draw_line);

        rotate_dot(de, angle);
    }
}
