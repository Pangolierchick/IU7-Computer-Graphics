#include <iostream>
#include <QApplication>
#include "mainwindow.hpp"
#include "./ui_mainwindow.h"
#include "uimanager.hpp"
#include "commands.hpp"
#include "logger.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    color = PURPLE;

    QGraphicsScene *scene = new QGraphicsScene(0, 0, 720, 600, this);
    ui->graphicsView->setScene(scene);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_draw_line_button_clicked()
{
    DBG_PRINT("On draw line button called\n");
    action_t action;
    commands_t cmd = DRAW_LINE;
    drawLine_t linep;

    dot_t d1(ui->x_s_spin->value(), ui->y_s_spin->value());
    dot_t d2(ui->x_e_spin->value(), ui->y_e_spin->value());

    linep.d1 = d1;
    linep.d2 = d2;

    linep.color = get_color();

    drawScene_t draw_scene(ui->graphicsView->scene());

    action.cmd = cmd;
    action.method = (drawMethods_t) ui->draw_method->currentIndex();
    action.lineParams = linep;

    manager(draw_scene, action);
}

void MainWindow::on_draw_bundle_button_clicked()
{

}

void MainWindow::on_clear_bundle_button_clicked()
{

}


void MainWindow::on_compare_algos_button_clicked()
{

}


colors_presets_t MainWindow::get_color() {
    return BLUE;
}

void MainWindow::on_use_purple_color_clicked()
{
    color = PURPLE;
}

void MainWindow::on_use_background_color_clicked()
{
    color = BACKGROUND;
}
