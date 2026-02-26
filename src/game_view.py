import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional


class GameView:
    """
    Handles all GUI rendering and user input for 2048.
    Uses Tkinter for cross-platform compatibility.
    """

    # Color scheme for tiles based on value
    TILE_COLORS = {
        0: "#cddc39",
        2: "#fce4ec",
        4: "#f8bbd0",
        8: "#f48fb1",
        16: "#f06292",
        32: "#ec407a",
        64: "#e91e63",
        128: "#c2185b",
        256: "#ad1457",
        512: "#880e4f",
        1024: "#6a1b9a",
        2048: "#4527a0",
        4096: "#311b92",
        8192: "#1a237e",
    }

    TEXT_COLORS = {
        0: "#000000",
        2: "#000000",
        4: "#000000",
        8: "#000000",
        16: "#000000",
        32: "#ffffff",
        64: "#ffffff",
        128: "#ffffff",
        256: "#ffffff",
        512: "#ffffff",
        1024: "#ffffff",
        2048: "#ffffff",
        4096: "#ffffff",
        8192: "#ffffff",
    }

    def __init__(self, grid_size: int = 4, cell_size: int = 100, padding: int = 10):
        """
        Initialize the game view.

        Args:
            grid_size: Size of the game grid (4x4)
            cell_size: Size of each cell in pixels
            padding: Padding between cells in pixels
        """
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.padding = padding

        # Calculate window size
        self.window_size = grid_size * cell_size + (grid_size + 1) * padding + 200

        # Create main window
        self.root = tk.Tk()
        self.root.title("2048 Game")
        self.root.resizable(False, False)
        self.root.geometry(f"{self.window_size}x{self.window_size + 100}")

        # Callbacks
        self.move_callback: Optional[Callable[[str], None]] = None
        self.new_game_callback: Optional[Callable[[], None]] = None
        self.undo_callback: Optional[Callable[[], None]] = None

        self._setup_ui()
        self._bind_keys()

    def _setup_ui(self) -> None:
        """Set up the user interface layout."""
        # Top frame for score and buttons
        top_frame = tk.Frame(self.root, bg="#fafafa", height=100)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        # Title
        title_label = tk.Label(
            top_frame,
            text="2048",
            font=("Helvetica", 32, "bold"),
            bg="#fafafa",
            fg="#3f51b5",
        )
        title_label.pack(side=tk.LEFT, padx=10)

        # Score frame
        score_frame = tk.Frame(top_frame, bg="#fafafa")
        score_frame.pack(side=tk.RIGHT, padx=10)

        tk.Label(
            score_frame,
            text="Score:",
            font=("Helvetica", 10, "bold"),
            bg="#fafafa",
            fg="#333333",
        ).pack()
        self.score_label = tk.Label(
            score_frame,
            text="0",
            font=("Helvetica", 16, "bold"),
            bg="#fafafa",
            fg="#3f51b5",
        )
        self.score_label.pack()

        tk.Label(
            score_frame,
            text="High Score:",
            font=("Helvetica", 10, "bold"),
            bg="#fafafa",
            fg="#333333",
        ).pack(pady=(10, 0))
        self.high_score_label = tk.Label(
            score_frame,
            text="0",
            font=("Helvetica", 16, "bold"),
            bg="#fafafa",
            fg="#e91e63",
        )
        self.high_score_label.pack()

        # Button frame
        button_frame = tk.Frame(self.root, bg="#fafafa")
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        self.new_game_btn = tk.Button(
            button_frame,
            text="New Game",
            command=self._on_new_game,
            font=("Helvetica", 10, "bold"),
            bg="#3f51b5",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2",
        )
        self.new_game_btn.pack(side=tk.LEFT, padx=5)

        self.undo_btn = tk.Button(
            button_frame,
            text="Undo",
            command=self._on_undo,
            font=("Helvetica", 10, "bold"),
            bg="#607d8b",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2",
        )
        self.undo_btn.pack(side=tk.LEFT, padx=5)

        # Instructions
        instructions = tk.Label(
            button_frame,
            text="Use arrow keys to move tiles",
            font=("Helvetica", 9),
            bg="#fafafa",
            fg="#666666",
        )
        instructions.pack(side=tk.RIGHT, padx=5)

        # Canvas for grid
        canvas_size = (
            self.grid_size * self.cell_size + (self.grid_size + 1) * self.padding
        )
        self.canvas = tk.Canvas(
            self.root,
            width=canvas_size,
            height=canvas_size,
            bg="#bbada0",
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=10)

        # Tile labels (for displaying numbers)
        self.tile_labels = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                label = tk.Label(
                    self.canvas,
                    text="",
                    font=("Helvetica", 24, "bold"),
                    width=4,
                    height=2,
                )
                label.place(
                    x=j * self.cell_size + (j + 1) * self.padding,
                    y=i * self.cell_size + (i + 1) * self.padding,
                    width=self.cell_size,
                    height=self.cell_size,
                )
                row.append(label)
            self.tile_labels.append(row)

    def _bind_keys(self) -> None:
        """Bind keyboard events for game controls."""
        self.root.bind("<Up>", lambda e: self._on_move("up"))
        self.root.bind("<Down>", lambda e: self._on_move("down"))
        self.root.bind("<Left>", lambda e: self._on_move("left"))
        self.root.bind("<Right>", lambda e: self._on_move("right"))
        self.root.bind("<Control-z>", lambda e: self._on_undo())

    def _on_move(self, direction: str) -> None:
        """Handle movement key press."""
        if self.move_callback:
            self.move_callback(direction)

    def _on_new_game(self) -> None:
        """Handle new game button press."""
        if self.new_game_callback:
            self.new_game_callback()

    def _on_undo(self) -> None:
        """Handle undo button press."""
        if self.undo_callback:
            self.undo_callback()

    def update_grid(self, grid) -> None:
        """
        Update the displayed grid with new values.

        Args:
            grid: 2D list or numpy array of tile values
        """
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = int(grid[i][j])
                label = self.tile_labels[i][j]

                if value == 0:
                    label.config(text="", bg="#cdc1b4", fg="#000000")
                else:
                    label.config(text=str(value))

                    # Get appropriate colors
                    bg_color = self.TILE_COLORS.get(value, self.TILE_COLORS[8192])
                    fg_color = self.TEXT_COLORS.get(value, self.TEXT_COLORS[8192])

                    label.config(bg=bg_color, fg=fg_color)

    def update_score(self, score: int, high_score: int) -> None:
        """
        Update displayed score and high score.

        Args:
            score: Current game score
            high_score: Highest score achieved
        """
        self.score_label.config(text=str(score))
        self.high_score_label.config(text=str(high_score))

    def show_game_over(self, score: int, high_score: int) -> None:
        """
        Show game over dialog.

        Args:
            score: Final score
            high_score: High score
        """
        messagebox.showinfo(
            "Game Over!",
            f"No more moves available.\n\nFinal Score: {score}\nHigh Score: {high_score}",
        )

    def show_win(self, score: int) -> None:
        """
        Show win dialog.

        Args:
            score: Current score when won
        """
        result = messagebox.showyesno(
            "You Won!",
            f"Congratulations! You reached 2048!\n\nCurrent Score: {score}\n\nContinue playing?",
        )
        return result

    def set_move_callback(self, callback: Callable[[str], None]) -> None:
        """Register callback for move events."""
        self.move_callback = callback

    def set_new_game_callback(self, callback: Callable[[], None]) -> None:
        """Register callback for new game events."""
        self.new_game_callback = callback

    def set_undo_callback(self, callback: Callable[[], None]) -> None:
        """Register callback for undo events."""
        self.undo_callback = callback

    def run(self) -> None:
        """Start the GUI event loop."""
        self.root.mainloop()

    def close(self) -> None:
        """Close the GUI window."""
        self.root.destroy()
