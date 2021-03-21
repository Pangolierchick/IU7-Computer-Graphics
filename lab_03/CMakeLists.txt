cmake_minimum_required(VERSION 3.5)

project(lab_03 LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_PREFIX_PATH /usr/local/opt/qt5)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenMP REQUIRED)
find_package(Qt5 COMPONENTS Widgets Charts REQUIRED)

add_definitions(-Wall -Wextra)


set(PROJECT_SOURCES
        main.cpp
        mainwindow.cpp
        mainwindow.hpp
        mainwindow.ui
        draw.cpp
        draw.hpp
        line.hpp
        dot.hpp
        dda.cpp
        dda.hpp
        bresenham.cpp
        bresenham.hpp
        color.hpp
        wu.cpp
        wu.hpp
        commands.hpp
        uimanager.cpp
        uimanager.hpp
        errors.hpp
        color.cpp
        logger.h
        compare.cpp
        compare.hpp
        timer.hpp
)

add_executable(lab_03
    ${PROJECT_SOURCES}
)

target_link_libraries(lab_03 PRIVATE Qt5::Widgets Qt5::Charts PRIVATE OpenMP::OpenMP_CXX)
