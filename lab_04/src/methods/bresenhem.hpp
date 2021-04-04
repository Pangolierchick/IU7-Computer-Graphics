#pragma once

#include "draw.hpp"

void bresenhem_circle(drawArea &area, point &c, float r, bool draw=true);
void bresenhem_ellipse(drawArea &area, point &c, float a, float b, bool draw=true);
