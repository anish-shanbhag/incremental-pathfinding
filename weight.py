WIDTH = 800

def get_weight(pos):
  return 1 - (((pos[0] - WIDTH / 2) ** 2 + (pos[1] - WIDTH / 2) ** 2) * 2 / WIDTH ** 2)