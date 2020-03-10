import cv2
import pathlib


def get_hsv_matriz_formatted(image_path):

    file = pathlib.Path(image_path)
    if not file.exists():
        return False
    else:
        img = cv2.imread(image_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        for i in range(0, len(hsv)):
            for j in range(0, len(hsv[i])):
                hsv[i][j][0] = int(hsv[i][j][0] * 2)
                hsv[i][j][1] = int((hsv[i][j][1] * 100) / 255)
                hsv[i][j][2] = int((hsv[i][j][2] * 100) / 255)

        return hsv