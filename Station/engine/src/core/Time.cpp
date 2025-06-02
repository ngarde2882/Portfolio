#include "Time.h"

Time::Time() {
    lastTime = std::chrono::steady_clock::now();
}

float Time::tick() {
    auto now = std::chrono::steady_clock::now();
    std::chrono::duration<float> delta = now - lastTime;
    lastTime = now;
    return delta.count();
}