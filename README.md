# Shortest Path Algorithm Visualizer

An interactive pathfinding visualizer built using **Python and Pygame** to demonstrate and compare **Dijkstra's Algorithm** and the **A* Search Algorithm** on a grid with user-defined obstacles.

## Project Overview

This project provides an interactive visualization of shortest-path algorithms.

Users can select a starting point and destination, create obstacles on the grid, and observe how different pathfinding algorithms explore nodes before determining the shortest available path.

The project demonstrates practical implementation of graph traversal, priority queues, heuristic search, and path reconstruction.

## Features

- Interactive grid-based interface
- Custom start and destination nodes
- User-defined obstacles and barriers
- Real-time algorithm visualization
- Shortest-path reconstruction
- Dijkstra's shortest path algorithm
- A* search algorithm
- Manhattan-distance heuristic
- Reset and clear-grid functionality

## Algorithms

### Dijkstra's Algorithm

Dijkstra's Algorithm finds the shortest path by repeatedly exploring the node with the minimum known distance from the starting node.

A priority queue implemented using Python's `heapq` module is used to efficiently select the next node for exploration.

### A* Search Algorithm

A* Search improves the direction of exploration by considering both:

- `g(n)` — actual cost from the starting node
- `h(n)` — estimated cost from the current node to the destination

The evaluation function is:

```text
f(n) = g(n) + h(n)
```

This project uses **Manhattan distance** as the heuristic:

```text
h(n) = |x1 - x2| + |y1 - y2|
```

For the four-directional grid used in this project, the heuristic guides the search toward the destination while preserving shortest-path optimality.

## Controls

| Control | Action |
|---|---|
| First Left Click | Set start node |
| Second Left Click | Set destination node |
| Additional Left Clicks | Create barriers |
| Right Click | Remove node or barrier |
| `D` | Run Dijkstra's Algorithm |
| `A` | Run A* Search |
| `R` | Reset search visualization |
| `C` | Clear the entire grid |

## Visualization

The application uses different colors to represent the state of the pathfinding process:

| Color | Meaning |
|---|---|
| Orange | Starting node |
| Purple | Destination node |
| Black | Barrier / obstacle |
| Green | Open / frontier node |
| Red | Explored node |
| Cyan | Final shortest path |
| White | Unvisited node |

## Technologies Used

- Python
- Pygame
- Python `heapq`
- Object-Oriented Programming
- Data Structures and Algorithms

## Concepts Demonstrated

- Graph traversal
- Priority queues
- Heaps
- Dijkstra's Algorithm
- A* Search Algorithm
- Manhattan-distance heuristic
- Path reconstruction
- Grid-based graph representation
- Interactive visualization

## How It Works

The grid is modeled as a graph where each traversable cell represents a node.

Each node can be connected to its valid neighboring cells in four directions:

- Up
- Down
- Left
- Right

Barrier cells are excluded from the available neighbors.

When an algorithm is executed, a priority queue determines which node should be explored next. The program stores predecessor information for visited nodes.

Once the destination is reached, the predecessor relationships are followed backward from the destination to reconstruct and visualize the shortest path.

## Installation

Clone or download this repository.

Install the required dependency:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python path_visualizer.py
```

## Example Usage

1. Launch the application.
2. Left-click once to select the starting node.
3. Left-click again to select the destination node.
4. Add barriers using additional left-clicks.
5. Press `D` to visualize Dijkstra's Algorithm.
6. Press `R` to reset the search visualization.
7. Press `A` to visualize A* Search.
8. Press `C` to clear the entire grid.

## Project Structure

```text
Shortest-Path-Visualizer/
├── path_visualizer.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Complexity

For a graph with `V` vertices and `E` edges, Dijkstra's Algorithm using a binary heap has a typical time complexity of:

```text
O((V + E) log V)
```

A* uses a similar priority-queue-based search, while the heuristic helps prioritize nodes that are estimated to be closer to the destination.

## Future Improvements

- Add Breadth-First Search (BFS)
- Add Depth-First Search (DFS)
- Display shortest-path length
- Display number of explored nodes
- Add algorithm execution speed controls
- Support weighted grid cells
- Add diagonal movement
- Add side-by-side algorithm comparison

## Author

**Karthikeyavarma**

IIT Madras
