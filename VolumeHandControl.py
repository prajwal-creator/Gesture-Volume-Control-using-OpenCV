import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wcam,hcam = 640,480                # width and height of the output which we can change if we want

cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ptime=0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()
minvol=volrange[0]
maxvol=volrange[1]
volbar = 400
volper=0

detector=htm.HandDetector(detectionCon=0.7)
while True:
    success,img = cap.read()       # success returns True if cam is working
    img=detector.findHands(img)
    lmlist = detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
        #print(lmlist[4],lmlist[8])
        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),10,(178,255,102),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (178,255,102), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(178,255,102),3)
        cv2.circle(img, (cx, cy), 10, (178,255,102), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        #print(length)
        # if length<50:
        #     cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)      # if length between the fingers is less then 50 then colour changes

        # hand range is between 50 to 200
        # volume range is between -65.25 to 0

        vol = np.interp(length,[50,200],[minvol,maxvol])
        volbar = np.interp(length,[50,200],[400,150])
        volper = np.interp(length,[50,200],[0,100])
        volume.SetMasterVolumeLevel(vol, None)
        #print(vol)
        cv2.rectangle(img, (50, 150), (85, 400), (173,216,230), 3)
        cv2.rectangle(img, (50, int(volbar)), (85, 400), (102,178,255), cv2.FILLED)
        cv2.putText(img,f'{int(volper)}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,178,102),3)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img,f'FPS: {int(fps)}',(60,60),cv2.FONT_HERSHEY_PLAIN,1,(102,0,204),2)
    cv2.imshow("Volume Modifier",img)
    cv2.waitKey(1)                # 1 millisecond delay
