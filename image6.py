from skimage import io, color, filters
import matplotlib.pyplot as plt
img = io.imread('people.jpg')
gray = color.rgb2gray(img)

edges = filters.sobel(gray)
plt.imshow(edges)
plt.show()