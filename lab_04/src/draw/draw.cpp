#include "draw.hpp"

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
