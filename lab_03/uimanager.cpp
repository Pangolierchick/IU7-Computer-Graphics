#include "uimanager.hpp"
#include "errors.hpp"
#include "draw.hpp"
#include "dda.hpp"
#include "bresenham.hpp"
#include "wu.hpp"
#include "logger.h"

int manager(drawScene_t& scene, action_t& action) {
    int rc = UKNOWN_CMD;

    DBG_PRINT("Manager called. #%d\n", action.cmd);

    switch (action.cmd) {
        case DRAW_LINE: {
            if (action.method == LIBRARY) {
                drawLibLine(scene, action.lineParams);
            } else {
                line_t line = drawLineManager(action.method, action.lineParams);
                drawLine(scene, line);
            }

            break;
        }
        
        case DRAW_BUNDLE: {
            if (action.method == LIBRARY) {
                drawLibBundle(scene, action.bundleParams);
            } else {
                drawBundle(scene, action.bundleParams, action.method);
            }
            break;
        }
        
        case CLEAN_SCREEN: {
            cleanScreen(scene);
            break;
        }
        
        case COMPARE_ALGORITHMS: {

            break;
        }
        
        case REDRAW: {

            break;
        }
        
        default:
            rc = UKNOWN_CMD;
            break;
    }

    return rc;
}

line_t drawLineManager(drawMethods_t method, drawLine_t& line) {
    Color color;
    color.presetColor(line.color);

    switch (method) {
        case DDA: {
            line_t new_line = dda(line.d1, line.d2, color);
            return new_line;
        }
        
        case BRESENHAM_INT: {
            line_t new_line = bresenham_int(line.d1, line.d2, color);
            return new_line;
        }
        
        case BRESENHAM_FLOAT: {
            line_t new_line = bresenham_double(line.d1, line.d2, color);
            return new_line;
        }
        
        case BRESENHAM_ANTIALIASING: {
            line_t new_line = bresenham_antialiased(line.d1, line.d2, color);
            return new_line;
        }
        
        case WU: {
            line_t new_line = wu(line.d1, line.d2, color);
            return new_line;
        }
        
        case LIBRARY:
            // TODO
            break;
        
        default:
            break;
    }
}
