# 2048 Game - A Fully Functional Implementation

A complete, production-ready implementation of the classic 2048 puzzle game built with Python. This project demonstrates proper software architecture with MVC (Model-View-Controller) pattern separation, and clean code practices.

## Features

✅ **Complete 2048 Game Logic**
- 4×4 grid with tile movement in all directions (Up, Down, Left, Right)
- Smooth tile merging with proper collision detection
- Prevention of double-merging in a single move
- Random tile spawning (90% chance for 2, 10% chance for 4)

✅ **Modern GUI with Tkinter**
- Clean, responsive interface with color-coded tiles
- Real-time score tracking and high score persistence
- Win/Loss detection with popup notifications
- Smooth animations and visual feedback
- Keyboard controls (arrow keys for movement)

✅ **Score Management**
- Current game score tracking
- High score persistence using JSON file storage
- Automatic score updates on tile merges

✅ **Game Features**
- Undo functionality to revert moves
- New Game button to restart anytime
- Game Over detection when no moves remain
- Win detection when 2048 tile is created
- Ability to continue playing after winning

✅ **Architecture & Code Quality**
- MVC pattern for clean separation of concerns
- Comprehensive unit test suite (20+ tests)
- Type hints throughout codebase
- Well-documented functions and classes
- No external GUI dependencies beyond Tkinter (built-in)

## Project Structure

```
2048/
├── src/
│   ├── game_model.py          # Core game logic (Model layer)
│   ├── game_view.py           # Tkinter GUI (View layer)
│   └── game_controller.py     # Game flow orchestration (Controller layer)
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── high_score.json            # Auto-generated high score storage
```

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup

1. Clone or navigate to the project directory:
```bash
cd 2048
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

Start the game with:
```bash
python main.py
```

### Controls
- **Arrow Keys**: Move tiles (↑ ↓ ← →)
- **R Key**: Start new game
- **Ctrl+Z**: Undo last move
- **New Game Button**: Start fresh game
- **Undo Button**: Revert previous move

## Game Rules

1. **Objective**: Combine tiles to create a 2048 tile
2. **Movement**: Move tiles in any direction using arrow keys
3. **Merging**: When two tiles with the same value collide, they merge into one tile with their combined value
4. **Scoring**: Points are earned equal to the value of merged tiles
5. **Spawning**: After each move, a new tile (2 or 4) appears randomly
6. **Winning**: Reach the 2048 tile to win (but you can continue playing!)
7. **Game Over**: When no moves remain, the game ends

## Architecture (MVC Pattern)

### Model Layer (`game_model.py`)
Pure game logic with no GUI dependencies:
- Grid state management (4×4 NumPy array)
- Movement and merging algorithms
- Score calculation
- Win/Loss detection
- High score persistence

**Key Classes:**
- `GameModel`: Main game logic handler

**Key Methods:**
- `move(direction)`: Execute a move
- `_move_line_left()`: Core merging algorithm
- `_check_game_state()`: Win/Loss detection
- `reset()`: Restart the game
- `undo()`: Revert last move

### View Layer (`game_view.py`)
Tkinter GUI for user interaction:
- Grid rendering with color-coded tiles
- Score display
- Button controls
- User input handling
- Dialog boxes for notifications

**Key Classes:**
- `GameView`: Handles all GUI rendering and events

**Color Scheme:**
- Tile values are color-coded for better visual hierarchy
- Text colors automatically adjust for readability
- Background colors indicate tile values

### Controller Layer (`game_controller.py`)
Orchestrates Model and View interaction:
- Handles user input from View
- Updates Model state
- Refreshes View display
- Manages win/loss flow

**Key Classes:**
- `GameController`: Connects Model and View

**Enjoy the game! Aim for 2048 and beyond!** 🎮
