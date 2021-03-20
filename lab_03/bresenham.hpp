#pragma once

#include "line.hpp"

line_t bresenham_int(dot_t& s, dot_t& e, color_t &color);
line_t bresenham_double(dot_t& s, dot_t& e, color_t &color);
line_t bresenham_antialiased(dot_t& s, dot_t& e, color_t &color);
