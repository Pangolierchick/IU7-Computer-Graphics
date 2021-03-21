#pragma once

#include <QMainWindow>
#include <QListWidgetItem>
#include "./ui_mainwindow.h"
#include "color.hpp"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_draw_line_button_clicked();
    void resizeEvent(QResizeEvent* e);

    void on_draw_bundle_button_clicked();

    void on_clear_bundle_button_clicked();

    void on_compare_algos_button_clicked();

private:
    colors_presets_t get_color();
    Ui::MainWindow *ui;
};
