# Rubik's Racer IDA* Solver

A **Python** and **Pygame** implementation of Rubik's Racer, using an IDA* solver.

## Prerequisites

* **Python 3.x**
* **C++ Compiler** (e.g., `g++`)

## Setup and Installation

1. Clone or download this repository
2. Install the required Python dependencies:
```bash
pip install -r requirements.txt
```
## Build Instructions

Before running the IDA* solver, you must compile the C++ heuristic function into a shared library so the Python script can utilize it.

1. Navigate to the `ida/` directory:
```bash
cd ida
```
2. Compile the C++ file based on your operating system.

**Mac / Linux:**
```bash
g++ -O3 -shared -fPIC -o heuristic.so heuristic.cpp
```
**Windows:**
```bash
g++ -O3 -shared -o heuristic.dll heuristic.cpp
```
Optionally, use the bash script `build.bash` (in the `ida/` directory) to compile for both **Mac / Linux** and **Windows**.

## Usage

**Play Manually:**
Launch the game normally. Use the arrow keys to slide the tiles. For movement, colored tiles slide into the position of the empty tile.
```bash
python render.py
```
**IDA\* Solver:**
Launch the game with the `ida` argument. The application will compute the optimal path and visually animate the solution.

```bash
python render.py ida
```