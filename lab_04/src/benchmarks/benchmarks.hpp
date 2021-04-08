#pragma once

#include <QtCharts>

#define BRESENHAM_STR    "Брезенхем"
#define MIDDLE_POINT_STR "Средняя точка"
#define CANONICAL_STR    "Каноническое уравнение"
#define PARAMETRIC_STR   "Параметрическое уравнение"
#define LIB_STR          "Библиотечная функция"

std::map<std::string, long> doBenchmarks(float r);
QChartView *getBenchmarksPlot();
