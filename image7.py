import pytesseract
import cv2
import matplotlib.pyplot as plt


img = cv2.imread('image_text.jpg')

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.axis('off')
plt.show()

text = pytesseract.image_to_string(img_rgb)
print(text)
