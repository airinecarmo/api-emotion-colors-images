import time
from copy import deepcopy
from numpy import dot
import cv2
import pathlib


def get_hsv_matriz_formatted(image_path):

    file = pathlib.Path(image_path)
    if not file.exists():
        return False
    else:
        img = cv2.imread(image_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hsv[:, :, 0] = dot(hsv[:, :, 0], 2.0)
        hsv[:, :, 1] = dot(hsv[:, :, 1], 0.39215686274509803)
        hsv[:, :, 2] = dot(hsv[:, :, 2], 0.39215686274509803)

        return hsv