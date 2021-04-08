#include "color.hpp"

QColor getColor(Colors c) {
    switch (c) {
        case Colors::BACKGROUND:
            return QColor(0xff, 0xff, 0xff);
        case Colors::BLACK:
            return QColor(0, 0, 0);
        case Colors::RED:
            return QColor(0xff, 0, 0);
        case Colors::PURPLE:
            return QColor(0x8a, 0x2b, 0xe2);
    }
}
