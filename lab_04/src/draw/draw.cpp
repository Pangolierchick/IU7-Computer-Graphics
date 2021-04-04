#include "draw.hpp"
#include "methods.hpp"

draw_circle_fun get_circle_fun(Methods m) {
    switch (m) {
        case BRESENHEM_METHOD:
            return bresenhem_circle;
        case MIDDLE_POINT_METHOD:
            return middle_circle;
        case LIB_METHOD:
            break;
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
            break;
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

void plot_circle(drawArea &area, float cx, float x, float cy, float y) {
    addPoint(area.scene, cx + x, cy + y, area.pen);
    addPoint(area.scene, cx + x, cy - y, area.pen);
    addPoint(area.scene, cx - x, cy + y, area.pen);
    addPoint(area.scene, cx - x, cy - y, area.pen);
    addPoint(area.scene, cy + y, cx + x, area.pen);
    addPoint(area.scene, cy + y, cx - x, area.pen);
    addPoint(area.scene, cy - y, cx + x, area.pen);
    addPoint(area.scene, cy - y, cx - x, area.pen);
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
    for (int i = 0; i < num; i++) {
        draw_ellipse(area, center, a + i * step, b + i * step, m);
    }
}

