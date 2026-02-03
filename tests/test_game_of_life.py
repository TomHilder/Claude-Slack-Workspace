"""Tests for Conway's Game of Life implementation."""

import pytest
from src.game_of_life import GameOfLife, PATTERNS


class TestGameOfLife:
    """Test the core GameOfLife class."""

    def test_init_creates_empty_grid(self):
        """A new game should start with no alive cells."""
        game = GameOfLife(10, 10)
        assert game.population() == 0
        assert game.generation == 0

    def test_add_cell(self):
        """Adding a cell should make it alive."""
        game = GameOfLife(10, 10)
        game.add_cell(5, 5)
        assert game.is_alive(5, 5)
        assert game.population() == 1

    def test_remove_cell(self):
        """Removing a cell should kill it."""
        game = GameOfLife(10, 10)
        game.add_cell(5, 5)
        game.remove_cell(5, 5)
        assert not game.is_alive(5, 5)
        assert game.population() == 0

    def test_remove_nonexistent_cell_is_safe(self):
        """Removing a cell that doesn't exist should not raise an error."""
        game = GameOfLife(10, 10)
        game.remove_cell(5, 5)  # Should not raise
        assert game.population() == 0

    def test_count_neighbors(self):
        """Neighbor counting should work correctly."""
        game = GameOfLife(10, 10)
        # Add neighbors around (5, 5)
        game.add_cell(4, 4)  # top-left
        game.add_cell(4, 5)  # top
        game.add_cell(5, 6)  # right
        assert game.count_neighbors(5, 5) == 3

    def test_count_neighbors_all_eight(self):
        """Counting all 8 neighbors should work."""
        game = GameOfLife(10, 10)
        # Surround (5, 5) with 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr != 0 or dc != 0:
                    game.add_cell(5 + dr, 5 + dc)
        assert game.count_neighbors(5, 5) == 8

    def test_clear(self):
        """Clear should remove all cells and reset generation."""
        game = GameOfLife(10, 10)
        game.add_cell(1, 1)
        game.add_cell(2, 2)
        game.step()
        game.clear()
        assert game.population() == 0
        assert game.generation == 0


class TestGameRules:
    """Test the rules of Conway's Game of Life."""

    def test_lonely_cell_dies(self):
        """A cell with fewer than 2 neighbors dies."""
        game = GameOfLife(10, 10)
        game.add_cell(5, 5)
        game.add_cell(5, 6)  # One neighbor
        game.step()
        assert not game.is_alive(5, 5)
        assert not game.is_alive(5, 6)

    def test_cell_survives_with_two_neighbors(self):
        """A cell with exactly 2 neighbors survives."""
        game = GameOfLife(10, 10)
        # Horizontal line of 3 (blinker)
        game.add_cell(5, 4)
        game.add_cell(5, 5)
        game.add_cell(5, 6)
        game.step()
        # Center cell should survive (rotates to vertical)
        assert game.is_alive(5, 5)

    def test_cell_survives_with_three_neighbors(self):
        """A cell with exactly 3 neighbors survives."""
        game = GameOfLife(10, 10)
        # Make a cell with 3 neighbors
        game.add_cell(5, 5)  # The cell
        game.add_cell(4, 5)  # neighbor
        game.add_cell(5, 4)  # neighbor
        game.add_cell(4, 4)  # neighbor
        game.step()
        assert game.is_alive(5, 5)

    def test_cell_dies_with_overpopulation(self):
        """A cell with more than 3 neighbors dies."""
        game = GameOfLife(10, 10)
        game.add_cell(5, 5)  # The cell
        game.add_cell(4, 4)
        game.add_cell(4, 5)
        game.add_cell(4, 6)
        game.add_cell(5, 4)  # 4 neighbors - overpopulation
        game.step()
        assert not game.is_alive(5, 5)

    def test_dead_cell_with_three_neighbors_becomes_alive(self):
        """A dead cell with exactly 3 neighbors becomes alive."""
        game = GameOfLife(10, 10)
        # Three cells in an L shape
        game.add_cell(4, 4)
        game.add_cell(4, 5)
        game.add_cell(5, 4)
        # Cell at (5, 5) has exactly 3 neighbors
        assert not game.is_alive(5, 5)
        game.step()
        assert game.is_alive(5, 5)


class TestFamousPatterns:
    """Test famous Game of Life patterns."""

    def test_blinker_oscillates(self):
        """The blinker should oscillate with period 2."""
        game = GameOfLife(10, 10)
        game.add_pattern(PATTERNS["blinker"], 5, 4)

        # Initial state: horizontal
        assert game.is_alive(5, 4)
        assert game.is_alive(5, 5)
        assert game.is_alive(5, 6)

        # After step: should be vertical
        game.step()
        assert game.is_alive(4, 5)
        assert game.is_alive(5, 5)
        assert game.is_alive(6, 5)
        assert not game.is_alive(5, 4)
        assert not game.is_alive(5, 6)

        # After another step: back to horizontal
        game.step()
        assert game.is_alive(5, 4)
        assert game.is_alive(5, 5)
        assert game.is_alive(5, 6)

    def test_block_is_still_life(self):
        """The block should never change (still life)."""
        game = GameOfLife(10, 10)
        game.add_pattern(PATTERNS["block"], 5, 5)

        initial_cells = game.alive_cells.copy()

        # Run for several generations
        for _ in range(10):
            game.step()
            assert game.alive_cells == initial_cells

    def test_glider_moves(self):
        """The glider should move diagonally."""
        game = GameOfLife(20, 20)
        game.add_pattern(PATTERNS["glider"], 5, 5)

        initial_population = game.population()

        # Run for 4 generations (one full cycle)
        for _ in range(4):
            game.step()

        # Population should remain the same
        assert game.population() == initial_population

        # Glider should have moved (check it's not in the same spot)
        assert not (game.is_alive(5, 6) and game.is_alive(6, 7) and game.is_alive(7, 5))

    def test_all_patterns_are_valid(self):
        """All patterns should be loadable and have cells."""
        for name, pattern in PATTERNS.items():
            game = GameOfLife(100, 100)
            game.add_pattern(pattern, 10, 10)
            assert game.population() > 0, f"Pattern {name} should have alive cells"


class TestPatterns:
    """Test pattern loading functionality."""

    def test_add_pattern(self):
        """Patterns should be loaded correctly."""
        game = GameOfLife(10, 10)
        pattern = [
            ".O.",
            "..O",
            "OOO",
        ]
        game.add_pattern(pattern, 0, 0)

        assert game.is_alive(0, 1)
        assert game.is_alive(1, 2)
        assert game.is_alive(2, 0)
        assert game.is_alive(2, 1)
        assert game.is_alive(2, 2)
        assert not game.is_alive(0, 0)

    def test_add_pattern_with_offset(self):
        """Patterns should respect offset."""
        game = GameOfLife(20, 20)
        game.add_pattern(["OO", "OO"], 5, 10)

        assert game.is_alive(5, 10)
        assert game.is_alive(5, 11)
        assert game.is_alive(6, 10)
        assert game.is_alive(6, 11)


class TestRandomize:
    """Test random initialization."""

    def test_randomize_creates_cells(self):
        """Randomize should create some cells."""
        game = GameOfLife(50, 50)
        game.randomize(density=0.3)
        # With 30% density on 2500 cells, we expect ~750 cells
        # Allow for some variance
        assert 500 < game.population() < 1000

    def test_randomize_with_zero_density(self):
        """Zero density should create no cells."""
        game = GameOfLife(50, 50)
        game.randomize(density=0.0)
        assert game.population() == 0

    def test_randomize_with_full_density(self):
        """Full density should fill all cells."""
        game = GameOfLife(10, 10)
        game.randomize(density=1.0)
        assert game.population() == 100


class TestGeneration:
    """Test generation tracking."""

    def test_generation_increments(self):
        """Generation should increment with each step."""
        game = GameOfLife(10, 10)
        game.add_cell(5, 5)
        assert game.generation == 0
        game.step()
        assert game.generation == 1
        game.step()
        assert game.generation == 2

    def test_generation_resets_on_clear(self):
        """Clear should reset generation to 0."""
        game = GameOfLife(10, 10)
        game.step()
        game.step()
        game.clear()
        assert game.generation == 0
