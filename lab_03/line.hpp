#pragma once

#include <vector>
#include "dot.hpp"

struct line {
    public:
        line(std::vector<dot_t>& dots): dots(dots) {}
        line(line&& l): dots(l.dots) {}

        std::vector<dot_t>& getDots() const { return this->dots; }
        std::vector<dot_t>& getDots() { return this->dots; }

    private:
        std::vector<dot_t>& dots;
};

using line_t = struct line;
