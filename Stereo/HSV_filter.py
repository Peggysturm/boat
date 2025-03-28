import sys
import cv2
import numpy as np
import time


def add_HSV_filter(frame, camera):
    # Blurring the frame
    blur = cv2.GaussianBlur(frame, (5, 5), 0)

    # Converting RGB to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    l_b_r = np.array([60, 110, 50])  # Lower limit for blue ball
    u_b_r = np.array([255, 255, 255])  # Upper limit for blue ball
    l_b_l = np.array([60, 110, 50])  # Lower limit for blue ball
    u_b_l = np.array([255, 255, 255])  # Upper limit for blue ball

    l_g_r = np.array([35, 100, 100])  # Lower limit for blue ball
    u_g_r = np.array([85, 255, 255])  # Upper limit for blue ball
    l_g_l = np.array([35, 100, 100])  # Lower limit for blue ball
    u_g_l = np.array([85, 255, 255])  # Upper limit for blue ball

    # l_b = np.array([140, 106, 0])        # LOWER LIMIT FOR BLUE COLOR!!!
    # u_b = np.array([255, 255, 255])

    # HSV-filter mask
    # mask = cv2.inRange(hsv, l_b_l, u_b_l)

    if (camera == 1):
        mask = cv2.inRange(hsv, l_g_r, u_g_r)
    else:
        mask = cv2.inRange(hsv, l_g_l, u_g_l)

    # Morphological Operation - Opening - Erode followed by Dilate - Remove noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    return mask
