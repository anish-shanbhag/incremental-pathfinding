"""
Implementation of unweighted, static grid size trajectory optimization algorithm
"""

from time import time, sleep
from queue import PriorityQueue
import pygame

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

ROWS = 50
WIDTH = 800
SPOT_WIDTH = WIDTH // ROWS

pygame.display.set_caption("Pathfinding")
window = pygame.display.set_mode((WIDTH, WIDTH))

grid = []
user_path = []

class Spot:
  def __init__(self, row, col):
    self.row = row
    self.col = col
    self.came_from = None
    self.neighbors = None
    self.valid = False
    self.color = WHITE

  def is_closed(self):
    return self.color == RED

  def is_open(self):
    return self.color == GREEN

  def is_barrier(self):
    return self.color == BLACK

  def is_start(self):
    return self.color == ORANGE

  def is_end(self):
    return self.color == TURQUOISE

  def is_user_path(self):
    return self.color == BLUE

  def reset(self):
    self.color = WHITE
    if self in user_path:
      user_path.remove(self)

  def make_start(self):
    self.color = ORANGE

  def make_closed(self):
    self.color = RED

  def make_open(self):
    self.color = GREEN
    if self in user_path:
      user_path.remove(self)

  def make_barrier(self):
    self.color = BLACK

  def make_end(self):
    self.color = TURQUOISE

  def make_path(self):
    self.color = PURPLE
  
  def make_user_path(self):
    if self not in user_path:
      self.color = BLUE
      user_path.append(self)

  def reset_visited(self):
    self.valid = False
    if self.is_open() or self.is_closed() or (self.color == BLUE and not self in user_path):
      self.color = WHITE


  def get_valid_neighbors(self):
    neighbors = []
    def add_neighbor(neighbor, is_diagonal):
      if not neighbor.is_barrier():
        neighbors.append((neighbor, is_diagonal))

    if self.row < ROWS - 1:
      south = grid[self.row + 1][self.col]
      add_neighbor(south, False)
      if self.col < ROWS - 1:
        southeast = grid[self.row + 1][self.col + 1]
        #add_neighbor(southeast, True)
      if self.col > 0:
        southwest = grid[self.row + 1][self.col - 1]
        #add_neighbor(southwest, True)

    if self.row > 0:
      north = grid[self.row - 1][self.col]
      add_neighbor(north, False)
      if self.col < ROWS - 1:
        northeast = grid[self.row - 1][self.col + 1]
        #add_neighbor(northeast, True)
      if self.col > 0:
        northwest = grid[self.row - 1][self.col - 1]
        #add_neighbor(northwest, True)

    if self.col < ROWS - 1:
      east = grid[self.row][self.col + 1]
      add_neighbor(east, False)
    if self.col > 0:
      west = grid[self.row][self.col - 1]
      add_neighbor(west, False)

    return neighbors
    
  def draw(self):
    if self.color != WHITE:
      pygame.draw.rect(
        window,
        self.color,
        # (x, y, width)
        (self.row * SPOT_WIDTH, self.col * SPOT_WIDTH, SPOT_WIDTH, SPOT_WIDTH)
      )

def draw():
  window.fill(WHITE)

  # draw spots
  for row in grid:
    for spot in row:
      spot.draw()
  """
  # draw grid
  for i in range(ROWS):
    pygame.draw.line(window, GREY, (0, i * SPOT_WIDTH), (WIDTH, i * SPOT_WIDTH))
    for j in range(ROWS):
      pygame.draw.line(window, GREY, (j * SPOT_WIDTH, 0), (j * SPOT_WIDTH, WIDTH))
  """

  pygame.display.update()

def algorithm(start, end, ignore_valid):
  count = 0
  open_set = PriorityQueue()
  open_set.put((0, count, start))

  def h(spot):
    return abs(end.row - spot.row) + abs(end.col - spot.col)

  scores = {spot: float("inf") for row in grid for spot in row}
  scores[start] = h(start) if ignore_valid else 0

  open_set_hash = {start}

  global user_path
  complete_path = [start, end, *user_path]
  
          
  for row in grid:
    for spot in row:
      spot.reset_visited()

  for spot in complete_path:
    spot.valid = True
    for neighbor, _ in spot.get_valid_neighbors():
      neighbor.valid = True

  while not open_set.empty():
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

    current = open_set.get()[2]
    open_set_hash.remove(current)

    if current == end:
      user_path = []
      end.make_end()
      current = current.came_from
      while current is not start:
        current.make_user_path()
        current = current.came_from
      return scores[end]
      # return scores[end]

    for neighbor, is_diagonal in current.get_valid_neighbors():
      if scores[neighbor] == float("inf") and (ignore_valid or neighbor.valid):
        neighbor.came_from = current
        scores[neighbor] = scores[current] + ((1.4 if is_diagonal else 1) + (h(neighbor) if ignore_valid else 0))
        if neighbor not in open_set_hash:
          count += 1
          open_set.put((scores[neighbor], count, neighbor))
          open_set_hash.add(neighbor)
          neighbor.make_open()
      

    if current != start:
      current.make_closed()
    
    # draw()
  
  return False


def make_grid():
  global grid
  grid = [[Spot(i, j) for j in range(ROWS)] for i in range (ROWS)]

def get_clicked_spot():
  y, x = pygame.mouse.get_pos()

  row = y // SPOT_WIDTH
  col = x // SPOT_WIDTH
  return grid[row][col]

def main():
  make_grid()

  start = None
  end = None

  run = True
  while run:
    draw()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      pressed = pygame.mouse.get_pressed()

      if pressed[0]: # LEFT
        spot = get_clicked_spot()
        if not start and spot != end:
          start = spot
          start.make_start()

        elif not end and spot != start:
          end = spot
          end.make_end()

        elif spot != end and spot != start:
          spot.make_barrier()

      elif pressed[1]: # MIDDLE
        spot = get_clicked_spot()
        if spot != end and spot != start and not spot.is_barrier():
          spot.make_user_path()

      elif pressed[2]: # RIGHT
        spot = get_clicked_spot()
        spot.reset()
        if spot == start:
          start = None
        elif spot == end:
          end = None

      if event.type == pygame.KEYDOWN:
        global user_path
        if event.key == pygame.K_SPACE and start and end:
          old_length = float("inf")
          new_length = 0
          start_time = time()
          while True:
            old_length = new_length
            new_length = algorithm(start, end, False)
            # draw()
            if new_length == old_length:
              break
          print("User path took:", time() - start_time)
          user_path = []

        if event.key == pygame.K_TAB and start and end:
          start_time = time()
          algorithm(start, end, True)
          user_path = []
          print("A* took:", time() - start_time)

        if event.key == pygame.K_c:
          start = None
          end = None
          user_path = []
          make_grid()

  pygame.quit()

main()