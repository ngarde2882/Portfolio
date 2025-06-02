cmake_minimum_required(VERSION 3.15)
project(Engine)

set(CMAKE_CXX_STANDARD 17)

add_executable(GameEngine
    src/main.cpp
    src/core/Application.cpp
    src/core/Time.cpp
)