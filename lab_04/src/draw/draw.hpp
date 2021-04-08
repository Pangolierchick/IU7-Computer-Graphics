#pragma once

#include <QGraphicsScene>

struct drawArea {
    QGraphicsScene *scene;
    QPen &pen;

    drawArea(QGraphicsScene *s, QPen &p): scene(s), pen(p) {}
};

struct point {
    float x;
    float y;

    point(float x, float y): x(x), y(y) {}
};

enum Methods {
    BRESENHEM_METHOD,
    MIDDLE_POINT_METHOD,
    LIB_METHOD,
    CANONICAL_METHOD,
    PARAMETRIC_METHOD
};

typedef void (*draw_circle_fun)(drawArea&, point&, float, bool);
typedef void (*draw_ellipse_fun)(drawArea&, point&, float, float, bool);

draw_circle_fun  get_circle_fun(Methods m);
draw_ellipse_fun get_ellipse_fun(Methods m);

void plot_point(drawArea &area, float x, float y);
void plot_circle(drawArea &area, float cx, float x, float cy, float y);
void plot_ellipse(drawArea &area, float cx, float x, float cy, float y);

void draw_circle_bundle(drawArea &area, point &center, float radius, int num, int step, Methods m);
void draw_ellipse_bundle(drawArea &area, point &center, float a, float b, int num, int step, Methods m);
