import numpy as np
from PIL import Image, ImageEnhance

from weight import WIDTH, get_weight

weight_image = None

def update_image():
  updated_image = weight_image.resize((WIDTH, WIDTH)).convert("LA")
  contrast_image = ImageEnhance.Contrast(updated_image).enhance(2)
  contrast_image.save("weight.png")


def generate_image():
  pixels = np.zeros((WIDTH, WIDTH, 3), dtype=np.uint8)

  for x in range(WIDTH):
    for y in range(WIDTH):
      color = (1 - get_weight((x, y), 1)) * 255
      pixels[x, y] = [color, color, color]

  image = Image.fromarray(pixels)
  image.save("weight.png")

try:
  weight_image = Image.open("original.png")
  update_image()
except FileNotFoundError:
  try:
    weight_image = Image.open("original.jpg")
    update_image()
  except FileNotFoundError:
    generate_image()