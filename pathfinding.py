"""

initial grid size should be <= minimum width of all weighted regions
(can leave this up to user)


"""

from time import time, sleep
from queue import PriorityQueue
import pygame
import math

from weight import WIDTH, get_weight

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

ROWS = 200
POS_WIDTH = WIDTH // ROWS

weight_image = pygame.image.load("weight.png")

pygame.display.set_caption("Pathfinding")
window = pygame.display.set_mode((WIDTH, WIDTH))

pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 12)

grid = []
user_path = []
start = None
end = None

def draw_pos(pos, color):
  pygame.draw.rect(
    window,
    color,
    # (x, y, width)
    (pos[0] * POS_WIDTH, pos[1] * POS_WIDTH, POS_WIDTH, POS_WIDTH)
  )

def draw():
  window.blit(weight_image, (0, 0))
  for pos in user_path:
    draw_pos(pos, BLUE)
  if start is not None:
    draw_pos(start, ORANGE)
  if end is not None:
    draw_pos(end, TURQUOISE)
  
  """
  # draw grid
  for i in range(ROWS):
    pygame.draw.line(window, GREY, (0, i * SPOT_WIDTH), (WIDTH, i * SPOT_WIDTH))
    for j in range(ROWS):
      pygame.draw.line(window, GREY, (j * SPOT_WIDTH, 0), (j * SPOT_WIDTH, WIDTH))
  """

  pygame.display.update()

def get_valid_neighbors(pos):
  x, y = pos
  neighbors = []

  # neighbors are in the form (x, y, is_diagonal)

  if y < ROWS - 1:
    neighbors.append((x, y + 1, False))
    if x < ROWS - 1:
      neighbors.append((x + 1, y + 1, True))
    if x > 0:
      neighbors.append((x - 1, y + 1, True))
    
  if y > 0:
    neighbors.append((x, y - 1, False))
    if x < ROWS - 1:
      neighbors.append((x + 1, y - 1, True))
    if x > 0:
      neighbors.append((x - 1, y - 1, True))

  if x < ROWS - 1:
    neighbors.append((x + 1, y, False))
  
  if x > 0:
    neighbors.append((x - 1, y, False))

  return neighbors
"""
def get_valid_diagonal_neighbors(pos):
  x, y = pos
  neighbors = []

  if y < ROWS - 1:
    if x < ROWS - 1:
      neighbors.append((x + 1, y + 1))
    if x > 0:
      neighbors.append((x - 1, y + 1))

  if y > 0:
    if x < ROWS - 1:
      neighbors.append((x + 1, y - 1))
    if x > 0:
      neighbors.append((x - 1, y - 1))

  return neighbors
"""

def algorithm(start, end, ignore_valid):
  count = 0
  open_set = PriorityQueue()
  open_set.put((0, count, start))

  def distance_to_end(pos):
    if ignore_valid:
      # return abs(pos[0] - pos[0]) + abs(end[1] - pos[1])
      return math.sqrt((end[0] - pos[0]) ** 2 + (end[1] - pos[1]) ** 2)
    else:
      return 0

  scores = { start: distance_to_end(start) }
  
  weights = { start: get_weight(start, POS_WIDTH) }

  global user_path
  complete_path = [start, end, *user_path]
  
  """
  for row in grid:
    for spot in row:
      spot.reset_visited()
  """

  valid = {}

  for pos in complete_path:
    valid[pos] = True
    for x, y, is_diagonal in get_valid_neighbors(pos):
      valid[(x, y)] = True

  came_from = {}
  closed = {}

  print(start, end)

  while not open_set.empty():
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

    current = open_set.get()[2]
    
    if current in closed:
      continue
    closed[current] = True

    if current == end:
      user_path = []
      # end.make_end()
      current = came_from[current]
      while current != start:
        # current.make_user_path()
        user_path.append(current)
        current = came_from[current]
      return scores[end]

    for x, y, is_diagonal in get_valid_neighbors(current):
      neighbor = (x, y)
      if neighbor not in closed and (ignore_valid or neighbor in valid):
        old_score = scores[neighbor] if neighbor in scores else float("inf")
        new_score = scores[current] + (1.4 if is_diagonal else 1)
        # may also want to memoize distance_to_end
        new_score += distance_to_end(neighbor) - distance_to_end(current)
        weights[neighbor] = get_weight(neighbor, POS_WIDTH)
        new_score += max(0, weights[neighbor] - weights[current]) * 100
        if new_score < old_score:
          came_from[neighbor] = current
          scores[neighbor] = new_score
          count += 1
          open_set.put((scores[neighbor], count, neighbor))
          
          # text = font.render(str(math.floor(scores[neighbor])), False, (255, 0, 0))
          # window.blit(text, (neighbor[0] * POS_WIDTH, neighbor[1] * POS_WIDTH))
          pygame.draw.rect(
            window,
            RED,
            # (x, y, width)
            (neighbor[0] * POS_WIDTH, neighbor[1] * POS_WIDTH, POS_WIDTH, POS_WIDTH)
          )
          
          pygame.display.update()

    # draw()
  return False

"""
def make_grid():
  global grid
  grid = [[Spot(i, j) for j in range(ROWS)] for i in range (ROWS)]
"""

def get_clicked_pos():
  x, y = pygame.mouse.get_pos()
  return (x // POS_WIDTH, y // POS_WIDTH)

def main():
  # make_grid()

  run = True
  draw()
  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      pressed = pygame.mouse.get_pressed()

      global user_path, start, end

      if pressed[0]: # LEFT
        pos = get_clicked_pos()
        if not start and pos != end:
          start = pos
          draw()

        elif not end and pos != start:
          end = pos
          draw()

        # elif spot != end and spot != start:
          # spot.make_barrier()
      
      elif pressed[1]: # MIDDLE
        pos = get_clicked_pos()
        if pos != end and pos != start and pos not in user_path: # and not pos.is_barrier():
          user_path.append(pos)
          draw()

      elif pressed[2]: # RIGHT
        pos = get_clicked_pos()
        if pos == start:
          start = None
          draw()
        elif pos == end:
          end = None
          draw()
        elif pos in user_path:
          user_path.remove(pos)
          draw()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and start and end:
          old_length = float("inf")
          new_length = 0
          start_time = time()
          while True:
            old_length = new_length
            new_length = algorithm(start, end, False)
            draw()
            if abs(new_length - old_length) < 1e-06:
              break
          print("User path took:", time() - start_time)

        if event.key == pygame.K_TAB and start and end:
          start_time = time()
          algorithm(start, end, True)
          print("A* took:", time() - start_time)
          draw() # A* draw

        if event.key == pygame.K_c:
          start = None
          end = None
          user_path = []
          draw()
          # make_grid()

  pygame.quit()

main()