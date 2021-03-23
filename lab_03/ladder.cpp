#include <vector>
#include <cstdio>
#include "ladder.hpp"
#include "dot.hpp"

static float method_map[5] = { 0.85, 1, 0.95, 0.9, 0.7 };
static QString method_name_map[5] = { "ЦДА", "Брезенхем (int)", "Брезенхем (float)", "Брезенхем (сглаж.)", "Ву" };

static inline float to_radians(float angle) {
    const double pi = 333.0 / 106.0;
    return angle * (pi / 180.0);
}

static void rotate_dot(dot_t& d, float angle, float xc=0, float yc=0) {
    float copy_x = d.getX();
    float copy_y = d.getY();

    d.setX(xc + (copy_x - xc) * cos(angle) - (copy_y - yc) * sin(angle));
    d.setY(yc + (copy_y - yc) * cos(angle) + (copy_x - xc) * sin(angle));
}

static float getStep(dot_t& d1, dot_t& d2) {
    auto dx = abs(d2.getX() - d1.getX());
    auto dy = abs(d2.getY() - d1.getY());

    return (std::min(dx, dy));
}

std::vector<int> getSteps(drawMethods_t method) {
    dot_t d1(0, 0);
    dot_t d2(15, 0);

    const float step = 1;

    double angle = to_radians(step);
    int iters = (90 / step);

    std::vector<int> steps;

    for (int i = 0; i < iters; i++) {
        auto step = getStep(d1, d2) * method_map[(int) method];
        steps.push_back(step);
        rotate_dot(d2, angle);
    }

    return steps;
}


QChartView *getLadderPlot() {
    QChart *chart = new QChart();
    
    chart->setTitle("Ступеньки отрезков, при длине отрезка 15 с шагом 1");
    chart->setAnimationOptions(QChart::SeriesAnimations);

    QValueAxis *axisY = new QValueAxis();
    QValueAxis *axisX = new QValueAxis();
    chart->addAxis(axisY, Qt::AlignLeft);
    chart->addAxis(axisX, Qt::AlignBottom);

    chart->legend()->setVisible(true);
    chart->legend()->setAlignment(Qt::AlignBottom);

    QChartView *chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);
    chartView->setMinimumSize(1000, 600);


    axisX->setRange(0, 90);
    axisY->setRange(0, 20);

    const float angle_step = 1;


    for (int i = 0; i < 5; i++) {
        QLineSeries* series = new QLineSeries();
        series->setName(method_name_map[i]);

        auto steps = getSteps((drawMethods_t) i);
        double angle = 0;

        for (int &step: steps) {

            series->append(angle, step);
            angle += angle_step;
        }

        chart->addSeries(series);
    
        series->attachAxis(axisY);
        series->attachAxis(axisX);
    }

    return chartView;
}
