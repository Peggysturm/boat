import cv2
cap = cv2.VideoCapture(2)
cap_2 = cv2.VideoCapture(0)


while True:
    re, fr = cap.read()
    re_2, fr_2 = cap_2.read()
    cv2.imshow('Video', fr)
    cv2.imshow('Video2', fr_2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break