#include "mainwindow.hpp"
#include "./ui_mainwindow.h"

#include "logger.h"
#include "color.hpp"
#include "benchmarks.hpp"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QGraphicsScene *scene = new QGraphicsScene(0, 0, 808, 600);
    
    // ui->graphicsView->fitInView(scene->sceneRect());
    ui->graphicsView->setScene(scene);

}

void MainWindow::resizeEvent(QResizeEvent* e)
{
    // FIXME
    // ui->graphicsView->fitInView(ui->graphicsView->scene()->sceneRect());
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_add_circle_btn_clicked()
{
    Methods method = (Methods) ui->draw_method->currentIndex();

    QPen pen(getColor((Colors) ui->colorBox->currentIndex()));
    pen.setWidthF(0.7);
    drawArea area(ui->graphicsView->scene(), pen);

    point center(ui->circle_center_x->value(), ui->circle_center_y->value());

    float circle_rad = ui->circle_radius->value();
    int circles_num = ui->circle_num_box->value();
    int step = ui->circle_step_box->value();

    if ((Colors) ui->colorBox->currentIndex() == BACKGROUND && last_method < PARAMETRIC_METHOD && method != LIB_METHOD) {
        ui->graphicsView->scene()->clear();
    }

    last_method = method;

    draw_circle_bundle(area, center, circle_rad, circles_num, step, method);
}

void MainWindow::on_add_ellipse_btn_clicked()
{
    Methods method = (Methods) ui->draw_method->currentIndex();

    QPen pen(getColor((Colors) ui->colorBox->currentIndex()));
    pen.setWidthF(0.7);
    drawArea area(ui->graphicsView->scene(), pen);

    point center(ui->ellipse_center_x->value(), ui->ellipse_center_y->value());

    float a = ui->ellipse_halfax_x->value();
    float b = ui->ellipse_halfax_y->value();
    int num = ui->circle_num_box->value();
    int step = ui->circle_step_box->value();

    if ((Colors) ui->colorBox->currentIndex() == BACKGROUND && last_method < PARAMETRIC_METHOD && method != LIB_METHOD) {
        ui->graphicsView->scene()->clear();
    }

    last_method = method;

    draw_ellipse_bundle(area, center, a, b, num, step, method);
}

void MainWindow::on_clean_screen_btn_clicked()
{
    auto scene = ui->graphicsView->scene();

    scene->clear();
}

void MainWindow::on_do_benchmarks_btn_clicked()
{
    auto benchmarks_plot = getBenchmarksPlot();
    benchmarks_plot->show();
}
