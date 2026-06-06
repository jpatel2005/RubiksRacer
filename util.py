import random

COLORS = ['R', 'G', 'B', 'Y', 'O', 'W']

def color_to_rgb(color):
    if color == 'R':
        return (255, 0, 0)
    elif color == 'G':
        return (0, 255, 0)
    elif color == 'B':
        return (0, 0, 255)
    elif color == 'Y':
        return (255, 255, 0)
    elif color == 'O':
        return (255, 165, 0)
    elif color == 'W':
        return (255, 255, 255)
    elif color == None:
        return (0, 0, 0)
    else:
        raise ValueError(f"Unknown color: {color}")

def generate_random_puzzle():
    # each color appears 4 times (4 * 6 = 24), plus one empty slot
    pool = [c for c in COLORS for _ in range(4)] 
    pool.append(None) # add empty slot
    random.shuffle(pool)
    grid = [pool[i:i+5] for i in range(0,25,5)]
    return grid

def generate_random_target():
    # target is just a random colored 3x3 in the center
    pool = [c for c in COLORS for _ in range(4)]
    random.shuffle(pool)
    center = [pool[i:i+3] for i in range(0,9,3)]
    grid = [[None] * 5 for _ in range(5)]
    # update grid
    for r in range(3):
        for c in range(3):
            grid[r+1][c+1] = center[r][c]

    return grid

def is_solved(puzzle, target):
    # check if 3x3 center matches target
    for r in range(1,4):
        for c in range(1,4):
            if puzzle[r][c] != target[r][c]:
                return False
    return True

# puzzle is a 1d tuple
def is_solved_1d(puzzle, target):
    # check if 3x3 center matches target
    for r in range(1,4):
        for c in range(1,4):
            if puzzle[5*r+c] != target[5*r+c]:
                return False
    return True

def find_empty_tile(puzzle):
    for r in range(5):
        for c in range(5):
            if puzzle[r][c] == None:
                return (r,c)
    raise ValueError("No empty tile found in puzzle")

def grid_to_tuple(grid):
    return tuple(tile for row in grid for tile in row)

def get_moves_from_path(path):
    moves = []
    for i in range(len(path)-1):
        a = path[i]
        b = path[i+1]
        idx_a = a.index(None)
        idx_b = b.index(None)
        if idx_b == idx_a + 5:
            moves.append("UP")
        elif idx_b == idx_a - 5:
            moves.append("DOWN")
        elif idx_b == idx_a + 1:
            moves.append("LEFT")
        elif idx_b == idx_a - 1:
            moves.append("RIGHT")
        else:
            raise ValueError("Invalid path")
    return moves