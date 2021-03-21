#pragma once

#include "commands.hpp"
#include "line.hpp"
#include "draw.hpp"

struct action {
    commands_t cmd;
    drawMethods_t method;
    drawLine_t lineParams;
    drawBundle_t bundleParams;
};

using action_t = struct action;

int manager(drawScene_t& scene, action_t& action);
line_t drawLineManager(drawMethods_t method, drawLine_t& line);
