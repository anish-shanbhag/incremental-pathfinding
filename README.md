# incremental-pathfinding

This is a work-in-progress implementation of an incremental pathfinding algorithm.

To run the visualization, either clone the repo or download the ZIP and extract it. Then, in the project directory, run `python pathfinding.py` to start the visualization. This will use the already-existing `weight.png` for the weighted regions; you can use a different image by replacing `original.jpg` with your own `original.jpg` or `original.png` and running `python image.py` to generate the new weight image.

# Visualization Controls

- **Left mouse button**: click anywhere to set the position of the start and end nodes. The algorithm will pathfind between these nodes and won't run until you've set both of them.
- **Middle mouse button**: hold and drag to draw a predefined path. If our incremental algorithm is used, then these nodes will be used in the algorithm.
- **Right mouse button**: resets a node, either making it no longer the start/end node or removing it from the path.
- **V key**: toggle the visualization of the pathfinding algorithms. If turned on, then the nodes which the algorithm searches will be highlighted in red. This significantly slows down the algorithms at large grid sizes, so it should be disabled when trying to analyze performance.
- **Up arrow**: increase the size of each node (increase grid size). This can be a bit wonky when there's already a path.
- **Down arrow**: decrease the size of each node (increase grid size).
- **R key**: resets all nodes. Removes the start/end nodes, removes the path, and resets the grid size to its initial value.
- **Tab key**: Runs the regular A* pathfinding algorithm to find the shortest path from the start node to the end node.
- **Space bar**: runs our incremental pathfinding algorithm. This will only work if there is already a path connecting the start and end nodes.

# General Notes

- Most output is currently printed to the console, including metrics for each algorithm after it runs.
- To use our incremental algorithm, set the grid size to a relatively large value and draw an approximate path from the start node to the end node. Alternatively, you can simply run the A* algorithm at that large grid size to generate the approximate path. Then, run our algorithm with the space bar.
- In the current implementation, moving from a lower weighted region to a higher weighted region is penalized, but moving from higher to lower is not. Additionally, traveling through a region with a continuous weight is not penalized. This implementation simulates traveling through mountains (where weights are elevation) but it may be changed in the future if needed.