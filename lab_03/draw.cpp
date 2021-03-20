#include "draw.hpp"
#include "ui_mainwindow.h"

static inline double move_x_to_center(double x, double width) {
    return x + width / 2.0;
}

static inline double move_y_to_center(double y, double height) {
    return y + height / 2.0;
}

void drawPixel(drawScene_t &scene, dot_t& dot) {
    auto x = dot.getX();
    auto y = dot.getY();
    auto c = dot.getColor();

    QGraphicsScene *draw_scene = scene.getScene();
    QColor color(c.Red(), c.Green(), c.Blue());
    QPen pen(color);

    x = move_x_to_center(x, draw_scene->width());
    y = move_y_to_center(x, draw_scene->height());
    
    draw_scene->addLine(x, y, x + 1, y, pen);
}


void drawLine(drawScene_t &scene, const line_t& line) {
    auto dots = line.getDots();

    for (auto& dot: dots) {
        drawPixel(scene, dot);
    }
}
