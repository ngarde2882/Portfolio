#include "Application.h"
#include "Time.h"
#include <iostream>

void Application:: run() {
    bool running = true;
    Time time;

    while (running) {
        float dt = time.tick();

        // TODO: input.update();
        // TODO: game.update(dt);
        // TODO: renderer.draw();

        std::cout << "Delta Time: " << dt << "s\n";

        // Temporary exit condition for testing
        static int frames = 0;
        if (++frames > 100)
            running = false;
    }
}