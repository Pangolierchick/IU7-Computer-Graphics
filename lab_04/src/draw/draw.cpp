#include <cstdio>
#include "draw.hpp"
#include "methods.hpp"

static void lib_circle(drawArea &area, point &c, float r, bool draw=true) {
    area.scene->addEllipse(c.x - r, c.y - r, 2 * r, 2 * r, area.pen);
}

static void lib_ellipse(drawArea &area, point &c, float a, float b,bool draw=true) {
    area.scene->addEllipse(c.x - a, c.y - b, 2 * a, 2 * b, area.pen);
}

draw_circle_fun get_circle_fun(Methods m) {
    switch (m) {
        case BRESENHEM_METHOD:
            return bresenhem_circle;
        case MIDDLE_POINT_METHOD:
            return middle_circle;
        case LIB_METHOD:
            return lib_circle;
        case CANONICAL_METHOD:
            return canonical_circle;
        case PARAMETRIC_METHOD:
            return parametric_circle;
        default:
            return nullptr;
    }
}

draw_ellipse_fun get_ellipse_fun(Methods m) {
    switch (m) {
        case BRESENHEM_METHOD:
            return bresenhem_ellipse;
        case MIDDLE_POINT_METHOD:
            return middle_ellipse;
        case LIB_METHOD:
            return lib_ellipse;
        case CANONICAL_METHOD:
            return canonical_ellipse;
        case PARAMETRIC_METHOD:
            return parametric_ellipse;
        default:
            return nullptr;
    }
}


static void addPoint(QGraphicsScene *view, float x, float y, const QPen& pen=QPen()) {
    view->addLine(x, y, x, y, pen);
}

void plot_point(drawArea &area, float x, float y) {
    addPoint(area.scene, x, y, area.pen);
}

void plot_circle(drawArea &area, float cx, float x, float cy, float y) {
    plot_point(area, x, y);
    plot_point(area, 2*cx - x, y);
    plot_point(area, x, 2*cy - y);
    plot_point(area, 2*cx - x, 2*cy - y);
    plot_point(area, y + cx - cy, x + cy - cx);
    plot_point(area, -y + cx + cy, x + cy - cx);
    plot_point(area, y + cx - cy, -x + cy + cx);
    plot_point(area, -y + cx + cy, -x + cy + cx);
}


void plot_ellipse(drawArea &area, float cx, float x, float cy, float y) {
    addPoint(area.scene, cx + x, cy + y, area.pen);
    addPoint(area.scene, cx + x, cy - y, area.pen);
    addPoint(area.scene, cx - x, cy + y, area.pen);
    addPoint(area.scene, cx - x, cy - y, area.pen);
}

void draw_circle(drawArea &area, point &center, float radius, Methods m) {
    draw_circle_fun fun = get_circle_fun(m);

    fun(area, center, radius, true);
}


void draw_ellipse(drawArea &area, point &center, float a, float b, Methods m) {
    draw_ellipse_fun fun = get_ellipse_fun(m);

    fun(area, center, a, b, true);
}

void draw_circle_bundle(drawArea &area, point &center, float radius, int num, int step, Methods m) {
    for (int i = 0; i < num; i++) {
        draw_circle(area, center, radius + i * step, m);
    }
}

void draw_ellipse_bundle(drawArea &area, point &center, float a, float b, int num, int step, Methods m) {
    float k = a / b;

    for (int i = 0; i < num; i++) {
        draw_ellipse(area, center, a, b, m);

        b += step;
        a = b * k;
    }
}

