import pygame
import random

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS
WHITE, BLACK, GREEN, RED, BLUE, GRAY = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255), (200, 200, 200)

# Directions for maze generation (row, col)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

class Maze:
    def __init__(self):
        self.grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]  # 1: Wall, 0: Path
        self.generate_maze()
        self.player_pos = (0, 0)  # Player starts at top-left
        self.exit_pos = (ROWS - 1, COLS - 1)  # Exit at bottom-right
        self.won = False

    def generate_maze(self, start=(0, 0)):
        """Generates a random maze using DFS-based backtracking."""
        stack = [start]
        visited = set()
        visited.add(start)

        while stack:
            r, c = stack[-1]
            self.grid[r][c] = 0  # Mark as path

            neighbors = [(r + dr * 2, c + dc * 2) for dr, dc in DIRECTIONS
                         if 0 <= r + dr * 2 < ROWS and 0 <= c + dc * 2 < COLS and (r + dr * 2, c + dc * 2) not in visited]

            if neighbors:
                nr, nc = random.choice(neighbors)
                self.grid[r + (nr - r) // 2][c + (nc - c) // 2] = 0  # Remove wall
                stack.append((nr, nc))
                visited.add((nr, nc))
            else:
                stack.pop()

    def move_player(self, dr, dc):
        """Moves the player if the path is open."""
        if self.won:
            return  # Stop movement after winning

        r, c = self.player_pos
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and self.grid[nr][nc] == 0:
            self.player_pos = (nr, nc)

        # Check win condition
        if self.player_pos == self.exit_pos:
            self.won = True

    def draw(self):
        """Draws the maze, player, and exit."""
        for r in range(ROWS):
            for c in range(COLS):
                color = WHITE if self.grid[r][c] == 0 else BLACK
                pygame.draw.rect(screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw exit (destination)
        er, ec = self.exit_pos
        pygame.draw.rect(screen, RED, (ec * CELL_SIZE, er * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw player
        pr, pc = self.player_pos
        pygame.draw.rect(screen, GREEN, (pc * CELL_SIZE, pr * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Display win message
        if self.won:
            font = pygame.font.Font(None, 50)
            text = font.render("You Win! Press R to Restart", True, BLUE)
            screen.blit(text, (WIDTH // 4, HEIGHT // 2))

        pygame.display.flip()

# Main function
def main():
    maze = Maze()
    running = True

    while running:
        screen.fill(GRAY)
        maze.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    maze.move_player(-1, 0)
                elif event.key == pygame.K_DOWN:
                    maze.move_player(1, 0)
                elif event.key == pygame.K_LEFT:
                    maze.move_player(0, -1)
                elif event.key == pygame.K_RIGHT:
                    maze.move_player(0, 1)
                elif event.key == pygame.K_r:  # Press 'R' to regenerate maze
                    maze = Maze()

        pygame.time.delay(50)  # Small delay for smoother movement

    pygame.quit()

if __name__ == "__main__":
    main()
