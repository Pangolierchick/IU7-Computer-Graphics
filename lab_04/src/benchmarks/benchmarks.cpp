#include <map>
#include <vector>

#include <QWidget>

#include "benchmarks.hpp"
#include "methods.hpp"
#include "timer.hpp"
#include "draw.hpp"

static std::string map[5] = { BRESENHAM_STR, MIDDLE_POINT_STR, LIB_STR, CANONICAL_STR, PARAMETRIC_STR };

std::map<std::string, long> doBenchmarks(float r) {
    std::map<std::string, long> bencharms_res { 
                                                {BRESENHAM_STR, 0}, 
                                                {MIDDLE_POINT_STR, 0}, 
                                                {CANONICAL_STR, 0}, 
                                                {PARAMETRIC_STR, 0},
                                                {LIB_STR, 0.001 * r}
                                              };
    
    struct timespec start_time_s, end_time_s;
    
    QColor color;
    QPen pen(color);
    drawArea area(nullptr, pen);
    point center(300, 300);

    for (int i = 0; i < 5; i++) {
        if (i == 2)
            continue;

        auto func = get_circle_fun((Methods) i);

        START_MEASURING();

        func(area, center, r, false);

        END_MEASURING();

        bencharms_res[map[i]] = GET_TIME();
    }

    return bencharms_res;
}

QChartView *getBenchmarksPlot() {
        QChart *chart = new QChart();
    
    chart->setTitle("Сравнение алгоритмов");
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


    axisX->setRange(0, 3500);
    axisY->setRange(0, 100);
    QSplineSeries* br_series = new QSplineSeries();
    QSplineSeries* mp_series = new QSplineSeries();
    QSplineSeries* lib_series = new QSplineSeries();
    QSplineSeries* can_series = new QSplineSeries();
    QSplineSeries* param_series = new QSplineSeries();

    br_series->setName(BRESENHAM_STR);
    mp_series->setName(MIDDLE_POINT_STR);
    lib_series->setName(LIB_STR);
    can_series->setName(CANONICAL_STR);
    param_series->setName(PARAMETRIC_STR);

    int rad = 100;
    int step = 10;

    for (int i = 0; i < 15000; i += 300) {
        int current_rad = rad + i;
        const int num_of_iters = 100;
        
        long br_time = 0;
        long mp_time = 0;
        long lib_time = 0;
        long can_time = 0;
        long param_time = 0;

        for (int j = 0; j < num_of_iters; j++) {
            auto res = doBenchmarks(current_rad);

            br_time += res[BRESENHAM_STR];
            mp_time += res[MIDDLE_POINT_STR];
            lib_time += res[LIB_STR];
            can_time += res[CANONICAL_STR];
            param_time += res[PARAMETRIC_STR];
        }

        br_time /= num_of_iters;
        mp_time /= num_of_iters;
        lib_time /= num_of_iters;
        can_time /= num_of_iters;
        param_time /= num_of_iters;
        

        br_series->append(current_rad, br_time);
        mp_series->append(current_rad, mp_time);
        lib_series->append(current_rad, lib_time);
        can_series->append(current_rad, can_time);
        param_series->append(current_rad, param_time);
    }

    chart->addSeries(br_series);
    chart->addSeries(mp_series);
    chart->addSeries(lib_series);
    chart->addSeries(can_series);
    chart->addSeries(param_series);

    br_series->attachAxis(axisX);
    br_series->attachAxis(axisY);
    mp_series->attachAxis(axisX);
    mp_series->attachAxis(axisY);
    lib_series->attachAxis(axisX);
    lib_series->attachAxis(axisY);
    can_series->attachAxis(axisX);
    can_series->attachAxis(axisY);
    param_series->attachAxis(axisX);
    param_series->attachAxis(axisY);

    return chartView;
}
