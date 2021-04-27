import math
from PIL import Image

WIDTH = 800

weight_image = Image.open("weight.png").convert("RGB")

def get_weight(pos, pos_width):
  return 1 - weight_image.getpixel((pos[0] * pos_width, pos[1] * pos_width))[0] / 255
  # return 1 - math.sqrt(((pos[0] * pos_width - WIDTH / 2) ** 2 + (pos[1] * pos_width - WIDTH / 2) ** 2) * 2 / WIDTH ** 2)