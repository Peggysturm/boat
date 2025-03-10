import cv2
cap = cv2.VideoCapture(2)


while True:
    re, fr = cap.read()
    cv2.imshow('Video', fr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break