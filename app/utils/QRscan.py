import cv2
from pyzbar.pyzbar import decode
import numpy as np
import winsound

def scan ():
    fre = 2000
    dur = 500
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    camera = True
    while camera == True:
        success, frame = cap.read()
        for code in decode(frame):
            data = code.data.decode('utf-8')
            if data:
                winsound.Beep(fre, dur)
                pts = np.array([code.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (255, 0, 255), 5)
                camera = False
        cv2.imshow("test-scan", frame)
        cv2.waitKey(1)
    return {
        'data': data,
        'success': success
    }