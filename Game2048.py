import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 400, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# Define colors
BACKGROUND_COLOR = (250, 248, 239)
GRID_COLOR = (187, 173, 160)
EMPTY_CELL_COLOR = (205, 193, 180)
GAME_OVER_OVERLAY_COLOR = (238, 228, 218, 150)

# Define tile colors
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# Define text colors for tiles
TEXT_COLOR = {
    2: (119, 110, 101),
    4: (119, 110, 101),
    8: (249, 246, 242),
    16: (249, 246, 242),
    32: (249, 246, 242),
    64: (249, 246, 242),
    128: (249, 246, 242),
    256: (249, 246, 242),
    512: (249, 246, 242),
    1024: (249, 246, 242),
    2048: (249, 246, 242)
}

# Game variables
GRID_SIZE = 4
CELL_SIZE = 80
CELL_MARGIN = 10

# Fonts
FONT = pygame.font.Font(None, 36)

class Game2048:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        # Add a new tile (2 or 4) to an empty cell
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        # Move tiles in the specified direction
        moved = False
        if direction == "up":
            moved = self._move_vertical(range(GRID_SIZE))
        elif direction == "down":
            moved = self._move_vertical(range(GRID_SIZE - 1, -1, -1))
        elif direction == "left":
            moved = self._move_horizontal(range(GRID_SIZE))
        elif direction == "right":
            moved = self._move_horizontal(range(GRID_SIZE - 1, -1, -1))
        
        if moved:
            self.add_new_tile()
        return moved

    def _move_vertical(self, range_iter):
        moved = False
        for j in range(GRID_SIZE):
            column = [self.grid[i][j] for i in range_iter if self.grid[i][j] != 0]
            column = self.merge(column)
            for i, value in zip(range_iter, column + [0] * (GRID_SIZE - len(column))):
                if self.grid[i][j] != value:
                    moved = True
                self.grid[i][j] = value
        return moved

    def _move_horizontal(self, range_iter):
        moved = False
        for i in range(GRID_SIZE):
            row = [self.grid[i][j] for j in range_iter if self.grid[i][j] != 0]
            row = self.merge(row)
            for j, value in zip(range_iter, row + [0] * (GRID_SIZE - len(row))):
                if self.grid[i][j] != value:
                    moved = True
                self.grid[i][j] = value
        return moved

    def merge(self, line):
        # Merge tiles with the same value
        merged = []
        for tile in line:
            if merged and merged[-1] == tile:
                merged[-1] *= 2
                self.score += merged[-1]
            else:
                merged.append(tile)
        return merged

    def is_game_over(self):
        # Check if the game is over (no moves possible)
        if any(0 in row for row in self.grid):
            return False
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if j < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True

def draw_grid(game):
    # Draw the game grid and tiles
    SCREEN.fill(BACKGROUND_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = j * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
            y = i * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
            pygame.draw.rect(SCREEN, GRID_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
            if game.grid[i][j] != 0:
                pygame.draw.rect(SCREEN, TILE_COLORS.get(game.grid[i][j], (237, 194, 46)), (x, y, CELL_SIZE, CELL_SIZE))
                font = pygame.font.Font(None, 48)
                text = font.render(str(game.grid[i][j]), True, TEXT_COLOR.get(game.grid[i][j], (249, 246, 242)))
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                SCREEN.blit(text, text_rect)

    score_text = FONT.render(f"Score: {game.score}", True, (119, 110, 101))
    SCREEN.blit(score_text, (10, HEIGHT - 40))

def draw_game_over():
    # Draw the game over screen
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(GAME_OVER_OVERLAY_COLOR)
    SCREEN.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 72)
    text = font.render("Game Over!", True, (119, 110, 101))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(text, text_rect)

def main():
    game = Game2048()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move("up")
                elif event.key == pygame.K_DOWN:
                    game.move("down")
                elif event.key == pygame.K_LEFT:
                    game.move("left")
                elif event.key == pygame.K_RIGHT:
                    game.move("right")

        draw_grid(game)
        
        if game.is_game_over():
            draw_game_over()
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
        else:
            pygame.display.flip()
        
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
