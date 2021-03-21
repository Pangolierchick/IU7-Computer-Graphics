#pragma once

#include <QWidget>
#include <QtCharts>



#define DDA_STR                 "DDA"
#define BRESENHAM_INT_STR       "Bresenham (int)"
#define BRESENHAM_FLOAT_STR     "Bresenham (float)" 
#define BRESENHAM_ANT_STR       "Bresenham (ant.)"
#define WU_STR                  "Wu"
#define LIB_STR                 "Lib"

QChartView* getChartView();
std::map<std::string, long> doBenchmarks();
