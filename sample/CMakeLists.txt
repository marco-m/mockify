cmake_minimum_required(VERSION 2.8.4)
project(mockify)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -W -Wall -Wextra -Werror")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -W -Wall -Wextra -Werror -std=c++11")

add_executable(main
    main.c
    uut.c
    deps.c
)

add_executable(test_main
    test_main.cpp
    uut.c
)