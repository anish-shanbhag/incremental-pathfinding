# - get_weight uses the darkness of a pixel to determine a node's weight
# - weight can only be between 0 and 1 in the current implementation
# - also exports WIDTH which defines both the size of the weight image
#   and the pygame window size

import math
from PIL import Image

WIDTH = 1024

weight_image = Image.open("weight.png").convert("RGB")

def get_weight(pos):
  return 1 - weight_image.getpixel((pos[0], pos[1]))[0] / 255
  """
  programmatically get weight via the distance from the center:
  return 1 - math.sqrt(((pos[0] * pos_width - WIDTH / 2) ** 2 + (pos[1] * pos_width - WIDTH / 2) ** 2) * 2 / WIDTH ** 2)
  """