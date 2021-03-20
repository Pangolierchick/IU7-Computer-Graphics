#include <iostream>
#include <QApplication>
#include "mainwindow.hpp"
#include "./ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_use_background_color_toggled(bool checked)
{
    std::cout << "background Toggled\n";
}

void MainWindow::on_use_purple_color_toggled(bool checked)
{
    std::cout << "purple Toggled\n";
}
