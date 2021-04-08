cmake_minimum_required(VERSION 3.5)

project(lab_04 LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_PREFIX_PATH /usr/local/opt/qt5)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenMP REQUIRED)
find_package(Qt5 COMPONENTS Widgets Charts REQUIRED)

set(SRC_DIR ./src)
set(UI_DIR ${SRC_DIR}/ui)
set(METHODS_DIR ${SRC_DIR}/methods)
set(DRAW_DIR ${SRC_DIR}/draw)
set(BENCHMARK_DIR ${SRC_DIR}/benchmarks)

include_directories(${UI_DIR} ${METHODS_DIR} ${DRAW_DIR} ${SRC_DIR} ${BENCHMARK_DIR})

add_definitions(-Wall -Wextra)

set(PROJECT_SOURCES
        ${SRC_DIR}/main.cpp
        ${SRC_DIR}/logger.h
        ${UI_DIR}/mainwindow.cpp
        ${UI_DIR}/mainwindow.hpp
        ${UI_DIR}/color.cpp
        ${UI_DIR}/color.hpp
        ${UI_DIR}/mainwindow.ui
        ${METHODS_DIR}/bresenhem.cpp
        ${METHODS_DIR}/bresenhem.hpp
        ${METHODS_DIR}/canonical.cpp
        ${METHODS_DIR}/canonical.hpp
        ${METHODS_DIR}/middlep.cpp
        ${METHODS_DIR}/middlep.hpp
        ${METHODS_DIR}/parametric.cpp
        ${METHODS_DIR}/parametric.hpp
        ${METHODS_DIR}/methods.hpp
        ${DRAW_DIR}/draw.cpp
        ${DRAW_DIR}/draw.hpp
        ${BENCHMARK_DIR}/benchmarks.cpp
        ${BENCHMARK_DIR}/benchmarks.hpp
        ${BENCHMARK_DIR}/timer.hpp
)

add_executable(lab_04
    ${PROJECT_SOURCES}
)

target_link_libraries(lab_04 PRIVATE Qt5::Widgets Qt5::Charts PRIVATE OpenMP::OpenMP_CXX)

