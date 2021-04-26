"""

initial grid size should be <= minimum width of all weighted regions
(can leave this up to user)


"""

from time import time, sleep
from queue import PriorityQueue
import pygame

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

ROWS = 50
SPOT_WIDTH = WIDTH // ROWS

weight_image = pygame.image.load("weight.png")

pygame.display.set_caption("Pathfinding")
window = pygame.display.set_mode((WIDTH, WIDTH))

grid = []
user_path = []
start = None
end = None

def draw_pos(pos, color):
  pygame.draw.rect(
    window,
    color,
    # (x, y, width)
    (pos[0] * SPOT_WIDTH, pos[1] * SPOT_WIDTH, SPOT_WIDTH, SPOT_WIDTH)
  )

def draw():
  window.blit(weight_image, (0, 0))
  for pos in user_path:
    draw_pos(pos, BLUE)
  if start is not None:
    draw_pos(start, ORANGE)
  if end is not None:
    draw_pos(start, TURQUOISE)
  
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

  if y < ROWS - 1:
    neighbors.append((x, y + 1))

  if y > 0:
    neighbors.append((x, y - 1))

  if x < ROWS - 1:
    neighbors.append((x + 1, y))
  
  if x > 0:
    neighbors.append((x - 1, y))

  return neighbors

def algorithm(start, end, ignore_valid):
  count = 0
  open_set = PriorityQueue()
  open_set.put((0, count, start))

  def h(spot):
    return abs(end[0] - spot[0]) + abs(end[1] - spot[1])

  scores = { start: h(start) if ignore_valid else 0 }

  open_set_hash = { start }

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
    for neighbor in get_valid_neighbors(pos):
      valid[neighbor] = True

  came_from = {}

  while not open_set.empty():
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

    current = open_set.get()[2]
    open_set_hash.remove(current)

    if current == end:
      user_path = []
      # end.make_end()
      current = came_from[current]
      while current != start:
        # current.make_user_path()
        user_path.append(current)
        current = came_from[current]
      return scores[end]

    for neighbor in get_valid_neighbors(current):
      if neighbor not in scores and (ignore_valid or neighbor in valid):
        came_from[neighbor] = current
        scores[neighbor] = scores[current] + (1 + (h(neighbor) if ignore_valid else 0)) + (get_weight(neighbor) - get_weight(current))
        if neighbor not in open_set_hash:
          count += 1
          open_set.put((scores[neighbor], count, neighbor))
          open_set_hash.add(neighbor)
    
    # draw()
  
  return False

"""
def make_grid():
  global grid
  grid = [[Spot(i, j) for j in range(ROWS)] for i in range (ROWS)]
"""

def get_clicked_pos():
  x, y = pygame.mouse.get_pos()
  return (x // SPOT_WIDTH, y // SPOT_WIDTH)

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
            print(new_length)
            draw()
            if new_length == old_length:
              break
          print("User path took:", time() - start_time)

        if event.key == pygame.K_TAB and start and end:
          start_time = time()
          algorithm(start, end, True)
          print("A* took:", time() - start_time)
          draw()

        if event.key == pygame.K_c:
          start = None
          end = None
          user_path = []
          draw()
          # make_grid()

  pygame.quit()

main()