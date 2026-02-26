from src.game_model import GameModel
from src.game_view import GameView
from src.game_controller import GameController

def main():
    """Start the 2048 game."""
    # Create root window

    # Create model and view
    model = GameModel()
    view = GameView()

    # Create controller (which connects model and view)
    controller = GameController(model, view)

    # Start the game
    controller.run()


if __name__ == "__main__":
    main()
