import random

class Game2048:
    def __init__(self):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        # Placeholder for move logic
        # You'll need to implement the actual sliding and merging here
        if direction in ["up", "down", "left", "right"]:
            # Perform the move
            # Add a new tile if the move was valid
            self.add_new_tile()

    def is_game_over(self):
        # Check if there are any empty cells
        if any(0 in row for row in self.grid):
            return False
        
        # Check if any adjacent cells have the same value
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                if (j < 3 and value == self.grid[i][j+1]) or \
                   (i < 3 and value == self.grid[i+1][j]):
                    return False
        
        return True
