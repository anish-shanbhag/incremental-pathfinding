"""
Initial implementation of Dijkstra's algorithm visualization
"""

from queue import PriorityQueue
import pygame
from time import time

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

class Spot:
  def __init__(self, row, col):
    self.row = row
    self.col = col
    self.color = WHITE
    self.came_from = None

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

  def make_start(self):
    self.color = ORANGE

  def make_closed(self):
    self.color = RED

  def make_open(self):
    self.color = GREEN

  def make_barrier(self):
    self.color = BLACK

  def make_end(self):
    self.color = TURQUOISE

  def make_path(self):
    self.color = PURPLE
  
  def make_user_path(self):
    self.color = BLUE

  def draw(self):
    if self.color != WHITE:
      pygame.draw.rect(
        window,
        self.color,
        # (x, y, width)
        (self.row * SPOT_WIDTH, self.col * SPOT_WIDTH, SPOT_WIDTH, SPOT_WIDTH)
      )

def h(spot1, spot2):
  return abs(spot1.row - spot2.row) + abs(spot1.col - spot2.col)


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

def reconstruct_path(current):
  while current.came_from:
    current = current.came_from
    current.make_path()
    draw()


def algorithm(start, end):
  count = 0
  open_set = PriorityQueue()
  open_set.put((0, count, start))

  scores = {spot: float("inf") for row in grid for spot in row}
  scores[start] = 0

  open_set_hash = {start}

  while not open_set.empty():
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

    current = open_set.get()[2]
    open_set_hash.remove(current)

    if current == end:
      reconstruct_path(end)
      end.make_end()
      return True

    def add_neighbor(neighbor, is_diagonal):
      if not neighbor.is_barrier() and scores[neighbor] == float("inf"):
        neighbor.came_from = current
        scores[neighbor] = scores[current] + (1.4 if is_diagonal else 1)
        if neighbor not in open_set_hash:
          nonlocal count
          count += 1
          open_set.put((scores[neighbor], count, neighbor))
          open_set_hash.add(neighbor)
          neighbor.make_open()

    if current.row < ROWS - 1:
      south = grid[current.row + 1][current.col]
      add_neighbor(south, False)
      if current.col < ROWS - 1:
        southeast = grid[current.row + 1][current.col + 1]
        add_neighbor(southeast, True)
      if current.col > 0:
        southwest = grid[current.row + 1][current.col - 1]
        add_neighbor(southwest, True)

    if current.row > 0:
      north = grid[current.row - 1][current.col]
      add_neighbor(north, False)
      if current.col < ROWS - 1:
        northeast = grid[current.row - 1][current.col + 1]
        add_neighbor(northeast, True)
      if current.col > 0:
        northwest = grid[current.row - 1][current.col - 1]
        add_neighbor(northwest, True)

    if current.col < ROWS - 1:
      east = grid[current.row][current.col + 1]
      add_neighbor(east, False)
    if current.col > 0:
      west = grid[current.row][current.col - 1]
      add_neighbor(west, False)
      
    # draw()

    if current != start:
      current.make_closed()
  
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
        if spot != end and spot != start:
          spot.make_user_path()

      elif pressed[2]: # RIGHT
        spot = get_clicked_spot()
        spot.reset()
        if spot == start:
          start = None
        elif spot == end:
          end = None


      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and start and end:
          algorithm(start, end)

        if event.key == pygame.K_c:
          start = None
          end = None
          make_grid()

  pygame.quit()

main()