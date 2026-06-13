#!/bin/bash
g++ -O3 -shared -fPIC -o heuristic.so heuristic.cpp # MacOS/Linux
g++ -O3 -shared -o heuristic.dll heuristic.cpp # Windows