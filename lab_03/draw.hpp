#pragma once

#include "color.hpp"
#include "dot.hpp"
#include "line.hpp"
#include "ui_mainwindow.h"


struct drawLine {
    dot_t d1;
    dot_t d2;

    colors_presets_t color;
};

struct drawBundle {
    float radius;
    float angle;
    colors_presets_t color;
};

enum drawMethods {
    DDA,
    BRESENHAM_INT,
    BRESENHAM_FLOAT,
    BRESENHAM_ANTIALIASING,
    WU,
    LIBRARY,
    UKNOWN_METHOD
};

struct drawScene {
    drawScene(): scene(nullptr) {}
    drawScene(QGraphicsScene *s): scene(s) {}

    QGraphicsScene *getScene() { return scene; }

    private:
        QGraphicsScene *scene;
};

using drawScene_t = struct drawScene;
using drawMethods_t = enum drawMethods;
using drawLine_t = struct drawLine;
using drawBundle_t = struct drawBundle;

void drawPixel(drawScene_t &scene, dot_t& dot);
void drawLine(drawScene_t &scene, const line_t& line);
void drawLibLine(drawScene_t &scene, drawLine_t lineParams);
void cleanScreen(drawScene_t &scene);
void drawBundle(drawScene_t &scene, drawBundle_t &bundleParams, drawMethods_t method);
void drawLibBundle(drawScene_t &scene, drawBundle_t &bundleParams);
