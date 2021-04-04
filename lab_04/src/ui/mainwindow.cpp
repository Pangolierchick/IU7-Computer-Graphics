#include "mainwindow.hpp"
#include "./ui_mainwindow.h"

#include "draw.hpp"
#include "logger.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QGraphicsScene *scene = new QGraphicsScene(0, 0, 808, 600);
    
    ui->graphicsView->setScene(scene);

    // ui->graphicsView->fitInView(ui->graphicsView->scene()->sceneRect());
}

void MainWindow::resizeEvent(QResizeEvent* e)
{
    // ui->graphicsView->fitInView(ui->graphicsView->scene()->sceneRect());
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_add_circle_btn_clicked()
{
    Methods method = (Methods) ui->draw_method->currentIndex();

    QPen pen(QColor(0xff, 0, 0));
    drawArea area(ui->graphicsView->scene(), pen);

    point center(ui->circle_center_x->value(), ui->circle_center_y->value());

    float circle_rad = ui->circle_radius->value();
    int circles_num = ui->circle_num_box->value();
    int step = ui->circle_step_box->value();

    DBG_PRINT("Drawing %d circles with (%f %f) center and %f radius by %d method\n", circles_num, center.x, center.y, circle_rad, method);

    draw_circle_bundle(area, center, circle_rad, circles_num, step, method);
}

void MainWindow::on_add_ellipse_btn_clicked()
{

}

void MainWindow::on_clean_screen_btn_clicked()
{
    auto scene = ui->graphicsView->scene();

    printf("Scene: %p\n", scene);

    scene->clear();
}

void MainWindow::on_do_benchmarks_btn_clicked()
{
    // TODO
}
