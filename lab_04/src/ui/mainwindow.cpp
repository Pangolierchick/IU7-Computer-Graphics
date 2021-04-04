#include "mainwindow.hpp"
#include "./ui_mainwindow.h"

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


void MainWindow::on_pushButton_clicked()
{
}
