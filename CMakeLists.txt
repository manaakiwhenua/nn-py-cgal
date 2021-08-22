cmake_minimum_required(VERSION 3.10.2)

project(nnpycgal)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -fopenmp")

# Fetch pybind11
include(FetchContent)

FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11
  GIT_TAG v2.6.2
)
FetchContent_MakeAvailable(pybind11)


set(SOURCE_DIR "src/nnpycgal")
include_directories(${SOURCE_DIR})

pybind11_add_module(nninterpol ${SOURCE_DIR}/nninterpol.cpp)

find_package(CGAL CONFIG REQUIRED)
target_link_libraries(nninterpol PRIVATE CGAL::CGAL)
