#pragma once

#include "ui_mainwindow.h"
#include "dot.hpp"
#include "line.hpp"

struct drawScene {
    drawScene(QGraphicsScene *s): scene(s) {}

    QGraphicsScene *getScene() { return scene; }

    private:
        QGraphicsScene *scene;
};

using drawScene_t = struct drawScene;

void drawPixel(drawScene &scene, dot_t& dot);
void drawLine(drawScene_t &scene, const line_t& line);
