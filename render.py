from util import *
import pygame
 
pygame.init()
pygame.display.set_caption("Rubik's Racer")
 
# [width, height]
puzzle_size = 400
outer_border = 180
size = (puzzle_size + 2 * outer_border, puzzle_size + 2 * outer_border)
center = (size[0] // 2, size[1] // 2)
tile_size = (size[0] - 2 * outer_border) // 5 # 6px padding on each size, 2px between tiles
target_tile_size = tile_size // 3
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()
game = {
    "puzzle": generate_random_puzzle(),
    "target": generate_random_target(),
    "moves": []
}
game["empty_pos"] = find_empty_tile(game["puzzle"]) 
BLACK = color_to_rgb(None)
print(game.get("puzzle"))

# Helper functions

def draw_target(target):
    # draw 3x3 target in top right
    gap = 2
    n = len(target)
    target_size = target_tile_size * n + gap * (n-1)
    start = (puzzle_size + outer_border + (outer_border - target_size) // 2, (outer_border - target_size) // 2)
    # skip 1 and n-1 since only 3x3 center is relevant
    for row in range(1,n-1):
        for col in range(1,n-1):
            color = target[row][col]
            x = start[0] + col * (target_tile_size + 2)
            y = start[1] + row * (target_tile_size + 2)
            pygame.draw.rect(screen, color_to_rgb(color), (x, y, target_tile_size, target_tile_size))

def draw_grid(grid):
    gap = 2
    n = len(grid)
    grid_size = tile_size * n + gap * (n-1)
    start = (center[0] - grid_size // 2, center[1] - grid_size // 2)
    for row in range(n):
        for col in range(n):
            color = grid[row][col]
            x = start[0] + col * (tile_size + 2)
            y = start[1] + row * (tile_size + 2)
            pygame.draw.rect(screen, color_to_rgb(color), (x, y, tile_size, tile_size))

def process_move(move, game):
    r, c = game["empty_pos"]
    n = len(game["puzzle"])
    puzzle = game["puzzle"]
    if move == "UP" and r < n-1:
        puzzle[r][c], puzzle[r+1][c] = puzzle[r+1][c], puzzle[r][c]
        r += 1
    elif move == "DOWN" and r > 0:
        puzzle[r][c], puzzle[r-1][c] = puzzle[r-1][c], puzzle[r][c]
        r -= 1
    elif move == "LEFT" and c < n-1:
        puzzle[r][c], puzzle[r][c+1] = puzzle[r][c+1], puzzle[r][c]
        c += 1
    elif move == "RIGHT" and c > 0:
        puzzle[r][c], puzzle[r][c-1] = puzzle[r][c-1], puzzle[r][c]
        c -= 1
    game["empty_pos"] = (r, c)

# Main program loop
while not done:
    # Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game["moves"].append("UP")
            elif event.key == pygame.K_DOWN:
                game["moves"].append("DOWN")
            elif event.key == pygame.K_LEFT:
                game["moves"].append("LEFT")
            elif event.key == pygame.K_RIGHT:
                game["moves"].append("RIGHT")
    # Game logic
    if game["moves"]:
        move = game["moves"].pop(0)
        process_move(move, game)

    # Clear screen
    screen.fill(BLACK)
 
    # Drawing code
    draw_grid(game["puzzle"])
    draw_target(game["target"])

    # Update screen @ 60 FPS
    pygame.display.flip()
    clock.tick(60)
 
pygame.quit()