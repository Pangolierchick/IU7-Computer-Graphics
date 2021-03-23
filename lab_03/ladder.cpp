#include <vector>
#include <cstdio>
#include "ladder.hpp"
#include "dot.hpp"

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

static int getStep(dot_t& d1, dot_t& d2) {
    auto dx = abs(d2.getX() - d1.getX());
    auto dy = abs(d2.getY() - d1.getY());
    
    printf("dx %f\tdy %f\n", dx, dy);

    return ((int) std::min(dx, dy));
}

std::vector<int> getSteps(int step) {
    dot_t d1(0, 0);
    dot_t d2(10, 0);

    double angle = to_radians(step);
    int iters = (90 / step);

    std::vector<int> steps;

    for (int i = 0; i < iters; i++) {
        steps.push_back(getStep(d1, d2));
        rotate_dot(d2, angle);
    }

    return steps;
}


QChartView *getLadderPlot(int angle_step) {
    QChart *chart = new QChart();
    
    chart->setTitle("Ступеньки");
    chart->setAnimationOptions(QChart::SeriesAnimations);

    QValueAxis *axisX = new QValueAxis();
    // axisX->append("Ступеньки");
    chart->addAxis(axisX, Qt::AlignBottom);

    QValueAxis *axisY = new QValueAxis();
    chart->addAxis(axisY, Qt::AlignLeft);

    chart->legend()->setVisible(true);
    chart->legend()->setAlignment(Qt::AlignBottom);

    QChartView *chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);
    chartView->setMinimumSize(1000, 600);

    QSplineSeries* series = new QSplineSeries();

    axisX->setRange(0, 100);

    auto steps = getSteps(angle_step);
    double angle = 0;

    for (int step: steps) {
        printf("%lf\t%d\n", angle, step);

        series->append(angle, step);
        angle += angle_step;
    }

    chart->addSeries(series);
    
    series->attachAxis(axisX);
    series->attachAxis(axisY);

    return chartView;
}
