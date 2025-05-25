# Kmeans Visualizer

A simple interactive GUI application for visualizing and experimenting with the K-means clustering algorithm, built with Python and Pygame.

## Features
- Add, remove, and clear points on a canvas
- Adjust the number of clusters (k) dynamically
- Run K-means clustering and visualize the results
- Draw cluster boundaries
- View cluster statistics and centroids

## How to Run
1. Create a virtual environment (recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
   (On macOS/Linux: `source venv/bin/activate`)
2. Install dependencies:
   ```bash
   pip install pygame
   pip install -U scikit-learn
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Project Structure
```
main.py                # Entry point, contains the main game loop and UI logic
modules/
  constants.py         # Color, FPS, and window size constants
  drawer.py            # UI elements: Button, Label, Canvas, etc.
  gamepoolmanager.py   # (If used) Game state management
  textbox.py           # (If used) Textbox UI element
  uielement.py         # Base UI element classes
  utils.py             # Utility functions (e.g., show_msg)
```

## Controls
- **Add Point:** Click on the canvas
- **Remove Last Point:** Click "Remove Last Point"
- **Clear Canvas:** Click "Clear Canvas"
- **Run K-means:** Click "Run"
- **Draw Boundary:** Toggle cluster boundaries
- **Increase/Decrease k:** Use + and - buttons

## License
MIT
