import cv2
import matplotlib.pyplot as plt

img = cv2.imread('Mummy.jpg')  # read image
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert BGR → RGB for display

plt.imshow(img_rgb)
plt.axis('off')
plt.show()
