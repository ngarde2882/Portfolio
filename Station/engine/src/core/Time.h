#pragma once
#include <chrono>

class Time {
    public:
        Time();
        float tick();
    private:
        std::chrono::steady_clock::time_point lastTime;
};