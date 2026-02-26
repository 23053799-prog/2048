import json
import os
from typing import List, Optional, Tuple

import numpy as np


class GameModel:
    """
    Handles all game logic for the 2048 game.
    Maintains game state, performs moves, merges, and score tracking.
    """

    def __init__(self, size: int = 4, high_score_file: str = "high_score.json"):
        """
        Initialize the game model.

        Args:
            size: Grid size (default 4x4)
            high_score_file: Path to store high scores
        """
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.score = 0
        self.high_score = 0
        self.high_score_file = high_score_file
        self.game_over = False
        self.won = False
        self.move_history = []  # For undo functionality

        self._load_high_score()
        self._spawn_initial_tiles()


    def _spawn_initial_tiles(self) -> None:
        """Spawn two random tiles (90% chance 2, 10% chance 4) at game start."""
        self._spawn_tile()
        self._spawn_tile()

    def _spawn_tile(self) -> None:
        """Spawn a single random tile (90% chance 2, 10% chance 4)."""
        empty_cells = np.argwhere(self.grid == 0)
        if len(empty_cells) > 0:
            row, col = empty_cells[np.random.randint(len(empty_cells))]
            value = 4 if np.random.random() < 0.1 else 2
            self.grid[row, col] = value


    def _move_line_left(self, line: np.ndarray) -> Tuple[np.ndarray, int]:
        """
        Compress and merge a single line to the left.

        Args:
            line: 1D array representing a row or column

        Returns:
            Tuple of (modified line, score gained from this move)
        """
        # Remove zeros and compress
        non_zero = line[line != 0]

        # Merge adjacent equal values (only once per move)
        merged = []
        skip = False
        score = 0

        for i in range(len(non_zero)):
            if skip:
                skip = False
                continue

            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged_value = non_zero[i] * 2
                merged.append(merged_value)
                score += merged_value
                skip = True
            else:
                merged.append(non_zero[i])

        # Pad with zeros to maintain size
        merged = np.array(merged, dtype=int)
        padded = np.zeros(len(line), dtype=int)
        padded[: len(merged)] = merged

        return padded, score

    def _rotate_grid_clockwise(self, grid: np.ndarray) -> np.ndarray:
        """Rotate grid 90 degrees clockwise."""
        return np.rot90(grid, k=-1)

    def _rotate_grid_counterclockwise(self, grid: np.ndarray) -> np.ndarray:
        """Rotate grid 90 degrees counterclockwise."""
        return np.rot90(grid, k=1)


    def move(self, direction: str) -> bool:
        """
        Execute a move in the specified direction.

        Args:
            direction: 'UP', 'DOWN', 'LEFT', or 'RIGHT'

        Returns:
            True if the move was valid and changed the grid, False otherwise
        """
        if self.game_over or self.won:
            return False

        # Store previous state for comparison
        previous_grid = self.grid.copy()
        previous_score = self.score

        # Save to history for undo
        self.move_history.append(
            {"grid": previous_grid.copy(), "score": previous_score}
        )

        direction = direction.upper()

        if direction == "LEFT":
            self._move_left()
        elif direction == "RIGHT":
            self._move_right()
        elif direction == "UP":
            self._move_up()
        elif direction == "DOWN":
            self._move_down()
        else:
            self.move_history.pop()
            return False

        # Check if the grid actually changed
        moved = not np.array_equal(self.grid, previous_grid)

        if moved:
            self._spawn_tile()
            self._check_game_state()
        else:
            # Undo the move if nothing changed
            self.move_history.pop()

        return moved

    def _move_left(self) -> None:
        """Move tiles left."""
        for i in range(self.size):
            new_line, score = self._move_line_left(self.grid[i, :])
            self.grid[i, :] = new_line
            self.score += score

    def _move_right(self) -> None:
        """Move tiles right."""
        for i in range(self.size):
            reversed_line = self.grid[i, ::-1]
            new_line, score = self._move_line_left(reversed_line)
            self.grid[i, :] = new_line[::-1]
            self.score += score

    def _move_up(self) -> None:
        """Move tiles up."""
        for j in range(self.size):
            column = self.grid[:, j]
            new_column, score = self._move_line_left(column)
            self.grid[:, j] = new_column
            self.score += score

    def _move_down(self) -> None:
        """Move tiles down."""
        for j in range(self.size):
            column = self.grid[:, j]
            reversed_column = column[::-1]
            new_column, score = self._move_line_left(reversed_column)
            self.grid[:, j] = new_column[::-1]
            self.score += score
