#pragma once

#include <QGraphicsScene>


struct drawArea {
    QGraphicsScene *scene;
    QPen &pen;

    drawArea(QGraphicsScene *s, QPen &p): scene(s), pen(p) {}
    ~drawArea() {
        delete scene;
    }
};

struct point {
    float x;
    float y;
};

void plot_circle(drawArea &area, float cx, float x, float cy, float y);
void plot_ellipse(drawArea &area, float cx, float x, float cy, float y);
