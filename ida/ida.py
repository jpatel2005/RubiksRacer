import ctypes
import os
import sys
from util import is_solved_1d, grid_to_tuple

# Iterative Deepening A* (IDA*) for Rubik's Racer
# Reference: https://en.wikipedia.org/wiki/Iterative_deepening_A*

# C++ bridge

lib_ext = '.dll' if os.name == 'nt' else '.so'
lib_name = f'heuristic{lib_ext}'
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'heuristic', lib_name))

# load C++ library
try:
    cpp_lib = ctypes.CDLL(lib_path)
except OSError:
    print(f"Error: Could not find the compiled C++ library at {lib_path}")
    sys.exit(1)

# define arg and return types for heuristic function
cpp_lib.get_heuristic_cost.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
cpp_lib.get_heuristic_cost.restype = ctypes.c_int

# dict to convert string colors to integers for C++ function
COLOR_TO_INT = {None: 0, 'R': 1, 'G': 2, 'B': 3, 'Y': 4, 'O': 5, 'W': 6}

# IDA* constants

FOUND = "FOUND"
NOT_FOUND = "NOT_FOUND"
INFINITY = float('inf')

# Helper functions

def heuristic(puzzle, target):
    puzzle_nums = [COLOR_TO_INT[c] for c in puzzle]
    target_nums = [COLOR_TO_INT[c] for c in target]
    # create C array types
    INT_ARRAY_25 = ctypes.c_int * 25
    c_puzzle = INT_ARRAY_25(*puzzle_nums)
    c_target = INT_ARRAY_25(*target_nums)
    # call C++ function and return cost
    return cpp_lib.get_heuristic_cost(c_puzzle, c_target)

def successors(state):
    succ = []
    empty_pos = state.index(None)
    # up (swap with +5)
    if empty_pos < 20:
        new_state = list(state)
        new_state[empty_pos], new_state[empty_pos+5] = new_state[empty_pos+5], new_state[empty_pos]
        succ.append(tuple(new_state))
    # down (swap with -5)
    if empty_pos >= 5:
        new_state = list(state)
        new_state[empty_pos], new_state[empty_pos-5] = new_state[empty_pos-5], new_state[empty_pos]
        succ.append(tuple(new_state))
    # left (swap with +1)
    if empty_pos % 5 != 4:
        new_state = list(state)
        new_state[empty_pos], new_state[empty_pos+1] = new_state[empty_pos+1], new_state[empty_pos]
        succ.append(tuple(new_state))
    # right (swap with -1)
    if empty_pos % 5 != 0:
        new_state = list(state)
        new_state[empty_pos], new_state[empty_pos-1] = new_state[empty_pos-1], new_state[empty_pos]
        succ.append(tuple(new_state))
    return succ

# Algorithm

def search(path, path_set, g, bound, target):
    node = path[-1]
    f = g + heuristic(node, target)
    if f > bound:
        return f
    if is_solved_1d(node, target):
        return FOUND
    minimum = INFINITY
    for succ in successors(node):
        if succ not in path_set:
            path.append(succ)
            path_set.add(succ)
            t = search(path, path_set, g+1, bound, target)
            if t == FOUND:
                return FOUND
            if t < minimum:
                minimum = t
            path.pop()
            path_set.remove(succ)
    return minimum

# Returns NOT_FOUND if no solution found, NONE if unsolvable (shouldn't happen), or (path, cost) if solution found
def ida_star(root_grid, target_grid):
    # convert 2d grids to 1d tuples
    root = grid_to_tuple(root_grid)
    target = grid_to_tuple(target_grid)
    bound = heuristic(root, target)
    path = [root]
    path_set = {root}
    while True:
        t = search(path, path_set, 0, bound, target)
        if t == FOUND:
            return (path, bound)
        if t == INFINITY:
            return NOT_FOUND
        bound = t