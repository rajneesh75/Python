from PIL import Image

img = Image.open('Mummy.jpg')
img.show()
print(img.size, img.mode, img.format)