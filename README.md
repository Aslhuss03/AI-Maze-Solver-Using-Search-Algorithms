README.md - Maze Runner: AI Search Algorithms Visualization

Project Overview

Maze Runner is an interactive Python application that visualizes and compares three fundamental AI search algorithms (A*, BFS, and DFS) solving maze navigation problems. Users can watch algorithms explore step-by-step, edit mazes in real-time, and analyze performance metrics.

Features

· Real-time Algorithm Visualization: Watch A*, BFS, and DFS search step-by-step
· Interactive Maze Editor: Add/remove walls, reposition start and goal points
· Multiple Algorithms: Compare performance of three search strategies
· Speed Control: Adjust visualization speed with slider
· Performance Metrics: Track path length, nodes expanded, and search patterns
· Pause/Resume: Control algorithm execution mid-search

Algorithms Implemented

1. A (A-Star)*: Optimal heuristic search using Manhattan distance
2. BFS (Breadth-First Search): Complete, optimal uniform-cost search
3. DFS (Depth-First Search): Depth-first exploration (non-optimal)

Installation & Requirements

Prerequisites

· Python 3.6 or higher
· Tkinter (usually included with Python)

Installation

1. Clone the repository:

git clone https://github.com/Aslhusx80/AI-Maze-Solver-Using-Search-Algorithms.git
cd AI-Maze-Solver-Using-Search-Algorithms
1. Run the application:

python maze_runner_V0.9.py
Note: No additional libraries needed - uses only Python standard libraries.

How to Use

Basic Controls

· Find Path: Run selected algorithm on current maze
· Regenerate Maze: Create new random maze (25% wall probability)
· Add/Remove Obstacles: Toggle edit mode to customize maze
· Restart: Clear current path and visited nodes
· Pause/Resume: Control algorithm execution
· Speed Slider: Adjust visualization speed (1-100)

Algorithm Selection

Use the dropdown menu to switch between:

· A*: Best for optimal paths with heuristic guidance
· BFS: Guarantees shortest path but explores more nodes
· DFS: May find paths quickly but not necessarily optimal

Maze Interaction

· Click empty cell in edit mode: Toggle wall on/off
· Click empty cell in normal mode: Move goal position
· Start position: Fixed at (0,0) - top-left corner
· Goal position: Default at (9,9) - bottom-right corner

Project Structure

maze_runner_V0.9.py
├── MazeGame class
│   ├── __init__() - GUI setup and initialization
│   ├── generate_random_maze() - Create random 10x10 maze
│   ├── draw_grid() - Visualize maze state
│   ├── start_pathfinding() - Begin algorithm execution
│   ├── step_astar() - A* algorithm implementation
│   ├── step_bfs() - BFS algorithm implementation
│   ├── step_dfs() - DFS algorithm implementation
│   └── reconstruct_path() - Build final path from search data
└── Global constants
    ├── CELL_SIZE = 40 pixels
    ├── GRID_ROWS = 10
    ├── GRID_COLS = 10
    └── WALL_PROB = 0.25
Visual Elements

· Green Square (S): Start position
· Red Square (G): Goal position
· Black Square (#): Wall/obstacle
· Light Blue Square (+): Visited node during search
· Yellow Square (*): Final path node
· Orange Highlight: Currently expanding node

Educational Value

This project demonstrates:

· How different search algorithms explore state spaces
· Trade-offs between optimality, completeness, and efficiency
· Heuristic function impact on search performance
· Real-time visualization of frontier expansion

Performance Metrics

When comparing algorithms, consider:

· Path Length: Number of steps in final solution
· Nodes Expanded: Total visited nodes during search
· Time Steps: Algorithm iterations until completion
· Frontier Size: Maximum simultaneous open nodes
· Success Rate: Ability to find paths in complex mazes

Future Enhancements

Planned features and improvements:

1. Additional algorithms (Dijkstra, Greedy Best-First)
2. Maze import/export functionality
3. Performance statistics display
4. Different heuristic functions
5. Variable grid sizes
6. Multiple agent simulation

License

This project is open-source and available for educational use.

uick Start: Run python maze_runner_V0.9.py and click "Find Path" to begin!
