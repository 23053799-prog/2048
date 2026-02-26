from typing import Optional

from src.game_model import GameModel
from src.game_view import GameView


class GameController:
    """
    Controls the flow of the 2048 game.
    Manages interactions between GameModel and GameView.
    """

    def __init__(self, model: GameModel, view: GameView):
        """
        Initialize the game controller.

        Args:
            model: GameModel instance
            view: GameView instance
        """
        self.model = model
        self.view = view
        self.won_notified = False

        # Register callbacks with view
        self.view.set_move_callback(self.on_move)
        self.view.set_new_game_callback(self.on_new_game)
        self.view.set_undo_callback(self.on_undo)

        # Initial display update
        self.update_display()

    def on_move(self, direction: str) -> None:
        """
        Handle a move event from the view.

        Args:
            direction: Direction of movement ('up', 'down', 'left', 'right')
        """
        moved = self.model.move(direction)

        if moved:
            self.update_display()

            # Check for win condition
            state = self.model.get_state()
            if state["won"] and not self.won_notified:
                self.won_notified = True
                continue_playing = self.view.show_win(state["score"])
                if not continue_playing:
                    self.on_new_game()

            # Check for game over condition
            if state["game_over"]:
                self.view.show_game_over(state["score"], state["high_score"])
                self.on_new_game()

    def on_new_game(self) -> None:
        """Handle new game request."""
        self.model.reset()
        self.won_notified = False
        self.update_display()

    def on_undo(self) -> None:
        """Handle undo request."""
        if self.model.undo():
            self.update_display()

        
    def update_display(self) -> None:
        """Update the view with current game state."""
        state = self.model.get_state()
        self.view.update_grid(state["grid"])
        self.view.update_score(state["score"], state["high_score"])

    def run(self) -> None:
        """Start the game."""
        self.view.run()
