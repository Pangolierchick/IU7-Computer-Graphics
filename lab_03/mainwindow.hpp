#pragma once

#include <QMainWindow>
#include <QListWidgetItem>

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
    // void on_methods_list_itemPressed(QListWidgetItem *item);

    void on_use_background_color_toggled(bool checked);

    void on_use_purple_color_toggled(bool checked);

private:
    Ui::MainWindow *ui;
};
