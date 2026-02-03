"""
Conway's Game of Life - A cellular automaton simulation

The universe of the Game of Life is an infinite two-dimensional grid of cells,
each of which is in one of two states: alive or dead. Every cell interacts with
its eight neighbors. At each step:

1. Any live cell with 2 or 3 live neighbors survives
2. Any dead cell with exactly 3 live neighbors becomes alive
3. All other live cells die, and all other dead cells stay dead

This is a fun terminal-based implementation with colorful ASCII art!
"""

import os
import time
import random
from typing import Set, Tuple

# Cell type: (row, col) coordinate
Cell = Tuple[int, int]


class GameOfLife:
    """The Game of Life simulation engine."""

    def __init__(self, width: int = 60, height: int = 30):
        self.width = width
        self.height = height
        self.alive_cells: Set[Cell] = set()
        self.generation = 0

    def add_cell(self, row: int, col: int) -> None:
        """Add a living cell at the given position."""
        self.alive_cells.add((row, col))

    def remove_cell(self, row: int, col: int) -> None:
        """Remove a cell (kill it) at the given position."""
        self.alive_cells.discard((row, col))

    def is_alive(self, row: int, col: int) -> bool:
        """Check if a cell is alive."""
        return (row, col) in self.alive_cells

    def count_neighbors(self, row: int, col: int) -> int:
        """Count the number of alive neighbors for a cell."""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if (row + dr, col + dc) in self.alive_cells:
                    count += 1
        return count

    def step(self) -> None:
        """Advance the simulation by one generation."""
        new_alive = set()

        # Get all cells that need to be checked (alive cells + their neighbors)
        cells_to_check = set()
        for row, col in self.alive_cells:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    cells_to_check.add((row + dr, col + dc))

        # Apply the rules
        for row, col in cells_to_check:
            neighbors = self.count_neighbors(row, col)
            if self.is_alive(row, col):
                # Alive cell survives with 2 or 3 neighbors
                if neighbors in (2, 3):
                    new_alive.add((row, col))
            else:
                # Dead cell becomes alive with exactly 3 neighbors
                if neighbors == 3:
                    new_alive.add((row, col))

        self.alive_cells = new_alive
        self.generation += 1

    def clear(self) -> None:
        """Clear all cells."""
        self.alive_cells.clear()
        self.generation = 0

    def randomize(self, density: float = 0.3) -> None:
        """Fill the grid with random cells."""
        self.clear()
        for row in range(self.height):
            for col in range(self.width):
                if random.random() < density:
                    self.add_cell(row, col)

    def add_pattern(self, pattern: list[str], offset_row: int = 0, offset_col: int = 0) -> None:
        """Add a pattern to the grid. Use 'O' or '#' for alive cells."""
        for r, line in enumerate(pattern):
            for c, char in enumerate(line):
                if char in ('O', '#', '*'):
                    self.add_cell(r + offset_row, c + offset_col)

    def population(self) -> int:
        """Return the number of alive cells."""
        return len(self.alive_cells)


# =============================================================================
# FAMOUS PATTERNS
# =============================================================================

PATTERNS = {
    "glider": [
        ".O.",
        "..O",
        "OOO",
    ],
    "blinker": [
        "OOO",
    ],
    "toad": [
        ".OOO",
        "OOO.",
    ],
    "beacon": [
        "OO..",
        "OO..",
        "..OO",
        "..OO",
    ],
    "pulsar": [
        "..OOO...OOO..",
        ".............",
        "O....O.O....O",
        "O....O.O....O",
        "O....O.O....O",
        "..OOO...OOO..",
        ".............",
        "..OOO...OOO..",
        "O....O.O....O",
        "O....O.O....O",
        "O....O.O....O",
        ".............",
        "..OOO...OOO..",
    ],
    "glider_gun": [
        "........................O...........",
        "......................O.O...........",
        "............OO......OO............OO",
        "...........O...O....OO............OO",
        "OO........O.....O...OO..............",
        "OO........O...O.OO....O.O...........",
        "..........O.....O.......O...........",
        "...........O...O....................",
        "............OO......................",
    ],
    "lightweight_spaceship": [
        ".OOOO",
        "O...O",
        "....O",
        "O..O.",
    ],
    "r_pentomino": [
        ".OO",
        "OO.",
        ".O.",
    ],
    "diehard": [
        "......O.",
        "OO......",
        ".O...OOO",
    ],
    "acorn": [
        ".O.....",
        "...O...",
        "OO..OOO",
    ],
    "block": [
        "OO",
        "OO",
    ],
    "beehive": [
        ".OO.",
        "O..O",
        ".OO.",
    ],
    "loaf": [
        ".OO.",
        "O..O",
        ".O.O",
        "..O.",
    ],
}


# =============================================================================
# TERMINAL DISPLAY
# =============================================================================

# ANSI color codes for pretty output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    # Cell colors (cycle through these for visual interest)
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"

    # UI colors
    HEADER = "\033[94m"
    DIM = "\033[90m"


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def render(game: GameOfLife, use_color: bool = True) -> str:
    """Render the game state as a string."""
    lines = []

    # Header
    if use_color:
        lines.append(f"{Colors.HEADER}{Colors.BOLD}╔{'═' * (game.width + 2)}╗{Colors.RESET}")
        lines.append(f"{Colors.HEADER}║{Colors.RESET} {Colors.CYAN}Conway's Game of Life{Colors.RESET}{' ' * (game.width - 21)} {Colors.HEADER}║{Colors.RESET}")
        lines.append(f"{Colors.HEADER}╠{'═' * (game.width + 2)}╣{Colors.RESET}")
    else:
        lines.append(f"╔{'═' * (game.width + 2)}╗")
        lines.append(f"║ Conway's Game of Life{' ' * (game.width - 21)} ║")
        lines.append(f"╠{'═' * (game.width + 2)}╣")

    # Grid
    cell_chars = ['█', '▓', '●', '◆', '★']
    cell_colors = [Colors.CYAN, Colors.GREEN, Colors.YELLOW, Colors.MAGENTA, Colors.WHITE]

    for row in range(game.height):
        line = []
        for col in range(game.width):
            if game.is_alive(row, col):
                # Pick character and color based on position for visual variety
                idx = (row + col) % len(cell_chars)
                if use_color:
                    line.append(f"{cell_colors[idx]}{cell_chars[idx]}{Colors.RESET}")
                else:
                    line.append(cell_chars[idx])
            else:
                if use_color:
                    line.append(f"{Colors.DIM}·{Colors.RESET}")
                else:
                    line.append(' ')

        if use_color:
            lines.append(f"{Colors.HEADER}║{Colors.RESET} {''.join(line)} {Colors.HEADER}║{Colors.RESET}")
        else:
            lines.append(f"║ {''.join(line)} ║")

    # Footer with stats
    if use_color:
        lines.append(f"{Colors.HEADER}╠{'═' * (game.width + 2)}╣{Colors.RESET}")
        stats = f"Generation: {game.generation:5d} │ Population: {game.population():5d}"
        padding = game.width - len(stats) + 2
        lines.append(f"{Colors.HEADER}║{Colors.RESET} {Colors.GREEN}{stats}{Colors.RESET}{' ' * padding}{Colors.HEADER}║{Colors.RESET}")
        lines.append(f"{Colors.HEADER}╚{'═' * (game.width + 2)}╝{Colors.RESET}")
    else:
        lines.append(f"╠{'═' * (game.width + 2)}╣")
        stats = f"Generation: {game.generation:5d} | Population: {game.population():5d}"
        padding = game.width - len(stats) + 2
        lines.append(f"║ {stats}{' ' * padding}║")
        lines.append(f"╚{'═' * (game.width + 2)}╝")

    return '\n'.join(lines)


def run_simulation(
    game: GameOfLife,
    generations: int = 100,
    delay: float = 0.1,
    use_color: bool = True
) -> None:
    """Run the simulation for a number of generations."""
    try:
        for _ in range(generations):
            clear_screen()
            print(render(game, use_color))
            print(f"\n{Colors.DIM}Press Ctrl+C to stop{Colors.RESET}" if use_color else "\nPress Ctrl+C to stop")
            time.sleep(delay)
            game.step()

            # Stop if everything dies
            if game.population() == 0:
                print("\n💀 All cells have died! Game over." if use_color else "\nAll cells have died! Game over.")
                break
    except KeyboardInterrupt:
        print("\n\n👋 Simulation stopped!" if use_color else "\n\nSimulation stopped!")


def demo() -> None:
    """Run a demo showing various patterns."""
    game = GameOfLife(60, 25)

    # Add a glider gun - it creates infinite gliders!
    game.add_pattern(PATTERNS["glider_gun"], 2, 2)

    # Add some still lifes and oscillators
    game.add_pattern(PATTERNS["pulsar"], 8, 40)

    run_simulation(game, generations=200, delay=0.08)


if __name__ == "__main__":
    demo()
