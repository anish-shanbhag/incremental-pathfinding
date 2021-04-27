from time import time, sleep
from queue import PriorityQueue
import pygame
import math

from weight import WIDTH, get_weight

INITIAL_NODE_WIDTH = 64

node_width = INITIAL_NODE_WIDTH

path = set()
start = None
end = None
visualize = False

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

weight_image = pygame.image.load("weight.png")

pygame.display.set_caption("Pathfinding")
window = pygame.display.set_mode((WIDTH, WIDTH))

def draw_node(node, color):
  # draws a square with its top left corner at the node position
  pygame.draw.rect(
    window,
    color,
    # (x, y, width)
    (node[0], node[1], node_width, node_width)
  )

def draw():
  window.blit(weight_image, (0, 0))
  for node in path:
    draw_node(node, BLUE)
  if start is not None:
    draw_node(start, ORANGE)
  if end is not None:
    draw_node(end, TURQUOISE)

  pygame.display.update()

def get_neighbors(node):

  # returns all immediate neighbors of a node, including diagonal ones
  # neighbors are in the form (x, y, is_diagonal)

  # o o o     x = node
  # o x o     o = valid neighbor
  # o o o

  x, y = node
  neighbors = []

  if y < WIDTH - node_width:
    neighbors.append((x, y + node_width, False)) # south
    if x < WIDTH - node_width:
      neighbors.append((x + node_width, y + node_width, True)) # southeast
    if x > 0:
      neighbors.append((x - node_width, y + node_width, True)) # southwest
    
  if y > 0:
    neighbors.append((x, y - node_width, False)) # north
    if x < WIDTH - node_width:
      neighbors.append((x + node_width, y - node_width, True)) # northeast
    if x > 0:
      neighbors.append((x - node_width, y - node_width, True)) # northwest

  if x < WIDTH - node_width:
    neighbors.append((x + node_width, y, False)) # east
  
  if x > 0:
    neighbors.append((x - node_width, y, False)) # west

  return neighbors

def a_star(ignore_valid):
  global path

  def distance_to_end(node):
    # returns the A* heuristic, i.e. the distance from a node to the end node
    # if ignore_valid is False (if the incremental algorithm is being used), 
    # then 0 is returned because there is little benefit for using a heuristic
    if ignore_valid:
      """
      use this for Manhattan distance instead of Euclidean distance:
      return abs(node[0] - node[0]) + abs(end[1] - node[1])
      """
      return math.sqrt((end[0] - node[0]) ** 2 + (end[1] - node[1]) ** 2)
    else:
      return 0

  # - includes all nodes which can be visited next
  # - implemented as a min heap with elements in the following form:
  #   (score, count, node)
  open_set = PriorityQueue()
  open_set.put((0, 0, start))
  
  # - keeps track of the number of nodes in the open set
  # - breaks ties in case multiple nodes have the same score
  count = 0

  # - contains the score for each node
  # - lower scores are visited first 
  scores = { start: distance_to_end(start) }

  # - contains the weight for each node
  # - i.e., how costly it is to travel to that node
  # - weights are retrieved via the weight module
  weights = { start: get_weight(start) }

  # - contains the "parent" node for each node
  # - used to generate the path after each iteration of A*
  came_from = {}

  # - keeps track of which nodes have been visited already
  # - nodes which have already been visited are skipped in case the open set
  #   has multiple instances of the same node (this can happen if there are
  #   multiple ways to get to a node, one of which is shorter than another)
  closed = set()

  # - contains all nodes which A* is allowed to visit
  # - contains all nodes in the current path (from either the user or the
  #   previous iteration), as well as the neighbors of each node in the path
  valid = set()
  for node in path:
    valid.add(node)
    for x, y, is_diagonal in get_neighbors(node):
      valid.add((x, y))

  # A* iterates over the open_set until no nodes are open
  # if this happens, then no valid path from start to end exists
  while not open_set.empty():

    # set the current node to the node in the open set with the lowest score
    current = open_set.get()[2]
    
    # skip any nodes which have already been visited
    if current in closed:
      continue
    closed.add(current)

    # end the algorithm if the end node is visited
    if current == end:
      # construct the path using came_from
      path = set()
      current = came_from[current]
      while current != start:
        path.add(current)
        current = came_from[current]
      # return the end node's score, which measures the final cost of traveling
      # from the start node to the end node, also taking into account node_width
      # since a smaller grid size would result in a "more costly" path even
      # though the actual length remains the same
      return scores[end]

    # iterate over the current node's valid neighbors
    for x, y, is_diagonal in get_neighbors(current):
      neighbor = (x, y)
      # skip any neighbors which are invalid or have already been visited
      if neighbor not in closed and (ignore_valid or neighbor in valid):
        old_score = scores[neighbor] if neighbor in scores else float("inf")

        # the neighbor's score is the current node's score + the distance
        # between the nodes (1.4 is approx. sqrt(2) for diagonal nodes)
        new_score = scores[current] + node_width * (1.4 if is_diagonal else 1)

        # for default A*, add the difference between the heuristics
        # of the neighbor and its parent
        # TODO: may also want to memoize distance_to_end
        new_score += distance_to_end(neighbor) - distance_to_end(current)

        # store the neighbor's weight for more efficient access when
        # it is later chosen as the current node
        weights[neighbor] = get_weight(neighbor)

        # - in the current implementation, the score is increased only when the
        #   weight increases from the current node to its neighbor
        # - it is also multiplied by 100 to have a larger impact on searching
        #   since get_weight can only return values between 0 and 1
        new_score += max(0, weights[neighbor] - weights[current]) * WIDTH
        
        # - only update the node if its new score is less than an existing one
        # - accounts for small floating point errors
        if new_score - old_score < -1e-4:
          came_from[neighbor] = current
          scores[neighbor] = new_score
          count += 1
          open_set.put((scores[neighbor], count, neighbor))
          if count % 1000 == 0:
            pygame.event.pump()
          if visualize:
            draw_node(neighbor, RED)
            if count % 100 == 0:
              pygame.display.update()

def get_clicked_node():
  x, y = pygame.mouse.get_pos()
  return x // node_width * node_width, y // node_width * node_width

def set_node_width(new_node_width, include_start_end):
  global node_width, path, start, end
  # multiplier = node_width / new_node_width
  node_width = new_node_width

  # - reconstruct the path using the updated grid size
  #     oo  <-- a single node is split into 4 different ones which fill the
  #     oo      entire original node using the following positions: top left,
  #             middle left, top middle, and center middle
  # - the start and end nodes are also included only when the incremental
  #   algorithm is running
  old_path = path.copy()
  if include_start_end:
    old_path.add(start)
    old_path.add(end)
  
  # repositions a node to the nearest node on the new grid
  def snap_to_grid(node):
    return tuple(node_width * math.ceil(c / node_width) for c in node)
  start = snap_to_grid(start)
  end = snap_to_grid(end)

  path = set()
  for old_node in old_path:
    x, y = snap_to_grid(old_node)
    path.add((x, y))
    path.add((x + node_width, y))
    path.add((x, y + node_width))
    path.add((x + node_width, y + node_width))
  
  print(node_width, len(path))


def incremental_algorithm():
  # runs the incremental algorithm using an already existing path
  print("Running the incremental algorithm...")

  # adds the start and end nodes to the path so that they are included
  # when determining which nodes are valid
  global path, start, end

  start_time = time()
  while True:
    old_length = float("inf")
    new_length = 0
    # iteratively update the path with Dijkstra's algorithm until the new path
    # is no longer shorter than the one from the previous iteration 
    while new_length - old_length < -1e-06:
      old_length = new_length
      new_length = a_star(False)
      if new_length is None:
        print("No path was found from the start node to the end node.")
        return
      if visualize:
        draw()
    
    # cut the grid size in half as long as node_width remains >= 1
    global node_width
    halved_node_width = node_width // 2
    if halved_node_width < 1:
      # stop the algorithm
      print(
        "The incremental algorithm took",
        time() - start_time,
        "seconds to find a path with a length of",
        new_length
      )
      return
    set_node_width(halved_node_width, True)

def main():
  global path, start, end, node_width, visualize
  run = True
  while run:
    draw()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      pressed = pygame.mouse.get_pressed()

      # set start/end nodes when left mouse is clicked
      if pressed[0]:
        node = get_clicked_node()
        if not start and node != end:
          start = node

        elif not end and node != start:
          end = node
      
      # add to the path when middle mouse is clicked
      elif pressed[1]:
        node = get_clicked_node()
        if node != end and node != start and node not in path:
          path.add(node)

      # reset nodes when right mouse is clicked
      elif pressed[2]:
        node = get_clicked_node()
        if node == start:
          start = None
        elif node == end:
          end = None
        elif node in path:
          path.remove(node)

      if event.type == pygame.KEYDOWN:
        # run the algorithm when space bar is pressed
        if event.key == pygame.K_SPACE and start and end:
          incremental_algorithm()

         # Run regular A* pathfinding when tab is pressed
        elif event.key == pygame.K_TAB and start and end:
          print("Running regular A* pathfinding algorithm...")
          start_time = time()
          length = a_star(True)
          print(
            "A* took",
            time() - start_time,
            "seconds to find a path with a length of",
            length
          )

        # completely reset all nodes, including grid size, when R is pressed
        elif event.key == pygame.K_r:
          start = None
          end = None
          path = set()
          node_width = INITIAL_NODE_WIDTH
          print("Reset all nodes.")

        # toggle algorithm visualization when V is pressed
        elif event.key == pygame.K_v:
          global visualize
          visualize = not visualize
          print("Algorithm visualization is", "on" if visualize else "off")

        # increase node width when the up arrow is pressed
        elif event.key == pygame.K_UP:
          set_node_width(node_width * 2, False)

        # decrease node width when the down arrow is pressed
        elif event.key == pygame.K_DOWN:
          new_node_width = node_width // 2
          if new_node_width >= 1:
            set_node_width(new_node_width, False)

  pygame.quit()

main()