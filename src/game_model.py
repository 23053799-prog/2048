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

