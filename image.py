import numpy as np
from PIL import Image

from weight import WIDTH, get_weight

pixels = np.zeros((WIDTH, WIDTH, 3), dtype=np.uint8)

for x in range(WIDTH):
  for y in range(WIDTH):
    color = (1 - get_weight((x, y))) * 255
    pixels[x, y] = [color, color, color]

image = Image.fromarray(pixels)
image.save("weight.png")
