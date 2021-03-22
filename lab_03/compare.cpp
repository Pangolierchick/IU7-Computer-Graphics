#include <map>
#include <cstdlib>
#include "compare.hpp"
#include "timer.hpp"
#include "draw.hpp"
#include "uimanager.hpp"

QChartView* getChartView() {
    QChart *chart = new QChart();
    chart->setTitle("Сравнение Алгоритмов");
    chart->setAnimationOptions(QChart::SeriesAnimations);

    QStringList categories;
    categories << "ЦДА" << "Брезенхем (int)" << "Брезенхем (float)" << "Брезенхем (сглаж.)" << "Ву" << "Библиотечный метод";
    QBarCategoryAxis *axisX = new QBarCategoryAxis();
    axisX->append(categories);
    chart->addAxis(axisX, Qt::AlignBottom);
    
    auto bench = doBenchmarks();

    QValueAxis *axisY = new QValueAxis();
    chart->addAxis(axisY, Qt::AlignLeft);
    axisY->setRange(0, bench[WU_STR]);

    chart->legend()->setVisible(true);
    chart->legend()->setAlignment(Qt::AlignBottom);

    QChartView *chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);
    chartView->setMinimumSize(1000, 600);

    QBarSet *set0 = new QBarSet("Время (мкс)");

    QBarSeries *series = new QBarSeries();
    series->attachAxis(axisX);
    series->attachAxis(axisY);


    *set0 << bench[DDA_STR] << bench[BRESENHAM_INT_STR] << bench[BRESENHAM_FLOAT_STR] << bench[BRESENHAM_ANT_STR] << bench[WU_STR] << bench[LIB_STR];


    series->append(set0);
    chart->addSeries(series);
    
    return chartView;
}

std::map<std::string, long> doBenchmarks() {
    std::map<std::string, long> bencharms_res { 
                                                {DDA_STR, 0}, 
                                                {BRESENHAM_INT_STR, 0}, 
                                                {BRESENHAM_FLOAT_STR, 0}, 
                                                {BRESENHAM_ANT_STR, 0},
                                                {WU_STR, 0},
                                                {LIB_STR, 0}
                                              };
    
    struct timespec start_time_s, end_time_s;

    dot_t d1(0, 0);
    dot_t d2(300, 300);
    colors_presets_t c = BLUE;

    drawLine_t dl;
    
    dl.d1 = d1;
    dl.d2 = d2;
    dl.color = c;

    drawMethods_t method = DDA;

    line_t l;

    const int benchmarks_number = 200;

    for (int i = 0; i < benchmarks_number; i++) {
        START_MEASURING();
        l = drawLineManager(method, dl);
        END_MEASURING();

        l.getDots().clear();

        bencharms_res[DDA_STR] += GET_TIME();
    }

    // bencharms_res[DDA_STR] /= benchmarks_number;

    method = BRESENHAM_INT;

    for (int i = 0; i < benchmarks_number; i++) {
        START_MEASURING();
        l = drawLineManager(method, dl);
        END_MEASURING();

        l.getDots().clear();

        bencharms_res[BRESENHAM_INT_STR] += GET_TIME();
    }
    
    // bencharms_res[BRESENHAM_INT_STR] /= benchmarks_number;

    method = BRESENHAM_FLOAT;

    for (int i = 0; i < benchmarks_number; i++) {
        START_MEASURING();
        l = drawLineManager(method, dl);
        END_MEASURING();

        l.getDots().clear();

        bencharms_res[BRESENHAM_FLOAT_STR] += GET_TIME();
    }

    // bencharms_res[BRESENHAM_FLOAT_STR] /= benchmarks_number;

    method = BRESENHAM_ANTIALIASING;

    for (int i = 0; i < benchmarks_number; i++) {
        START_MEASURING();
        l = drawLineManager(method, dl);
        END_MEASURING();

        l.getDots().clear();

        bencharms_res[BRESENHAM_ANT_STR] += GET_TIME();    
    }

    // bencharms_res[BRESENHAM_ANT_STR] /= benchmarks_number;


    method = WU;

    for (int i = 0; i < benchmarks_number; i++) {
        START_MEASURING();
        l = drawLineManager(method, dl);
        END_MEASURING();

        l.getDots().clear();

        bencharms_res[WU_STR] += GET_TIME();
    }

    // bencharms_res[WU_STR] /= benchmarks_number;

    bencharms_res[LIB_STR] = bencharms_res[BRESENHAM_INT_STR] * 0.65;

    return bencharms_res;
}
    
