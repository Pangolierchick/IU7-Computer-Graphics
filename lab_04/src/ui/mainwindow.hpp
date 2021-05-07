#pragma once

#include <QMainWindow>

#include "draw.hpp"

#define DO_CALCS \
            if ((Colors) ui->colorBox->currentIndex() == BACKGROUND && last_method < PARAMETRIC_METHOD && method != LIB_METHOD) { \
                ui->graphicsView->scene()->clear();\
            }\

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Methods last_method = BRESENHEM_METHOD;
    Ui::MainWindow *ui;

private slots:
    void resizeEvent(QResizeEvent* e);
    void on_add_circle_btn_clicked();
    void on_add_ellipse_btn_clicked();
    void on_clean_screen_btn_clicked();
    void on_do_benchmarks_btn_clicked();
};
