import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.morphology import disk
from skimage.filters.rank import median

def bounding_box(path):
    img = cv2.imread('1stEdition01-428x700.jpg',0)
    edges = cv2.Canny(img,100,200)
    med = median(edges, disk(2))
    _, otsu = cv2.threshold(med, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    y_0 = 0
    y_1 = len(otsu) - 1
    x_0 = 0
    x_1 = len(otsu[0]) - 1
    while (np.mean(otsu[:, x_0]) < 1):
        x_0 = x_0 + 1
    while (np.mean(otsu[:, x_1]) < 1):
        x_1 = x_1 - 1
    while (np.mean(otsu[y_0]) < 2):
        y_0 = y_0 + 1
    while (np.mean(otsu[y_1]) < 2):
        y_1 = y_1 - 1
    y_0 = int(y_0 * .6)
    x_0 = int(x_0 * .6)
    y_1 = int(len(otsu) - (len(otsu) - y_1) * .6)
    x_1 = int(len(otsu[0]) - (len(otsu[0]) - x_1) * .6)
    img = img[y_0:y_1, x_0:x_1]
    plt.imshow(img)
    plt.show()
