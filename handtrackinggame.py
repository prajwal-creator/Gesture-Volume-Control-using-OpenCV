import time
import cv2
import mediapipe as mp
import HandTrackingModule as htm

ptime = 0
ctime = 0
cap = cv2.VideoCapture(0)
detector = htm.HandDetector()
while True:
    succ, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    if len(lmlist) != 0:
        print(lmlist[4])
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
    cv2.imshow("image", img)
    cv2.waitKey(1)