import time
import pydirectinput as pag
import cv2
import math
from threading import Lock, Thread
from HandTracker import HandTracker
from WebCam import WebCam
from HandIPC import IPC


# map from map coordinates to pixel coordinates
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Mouse:
    def __init__(self, smoothingFactor, cameraWidth, cameraHeight) -> None:

        # This allows us to move the mouse past boarders which helps in my case of multiple monitors.
        pag.FAILSAFE = False

        # Higher numbers make the movement smoother however also cause lag.
        self.smoothingFactor = smoothingFactor

        # storing past data for smoothing formula
        self.pastXCoord = 0
        self.pastYCoord = 0

        # This is for the web cam and desktop size, we use it for scaling the aspect ratio of the camera to that of the desktop.
        self.cameraWidth = cameraWidth
        self.cameraHeight = cameraHeight
        winSize = pag.size()
        self.winSizeX = winSize[0]
        self.winSizeY = winSize[1]

        # Offsets used to deal with bounds issues with handtracker
        self.offsety = 0.2
        self.offsetx = self.offsety * (cameraHeight / self.winSizeY) * (cameraWidth / self.winSizeX)

    def update(self, gestures):
        xCoord = map(gestures.pointerX, self.offsetx, 1- self.offsetx, 0, self.winSizeX)
        yCoord = map(gestures.pointerY, self.offsety, 1 - self.offsety, 0, self.winSizeY)

        xSmoothed = self.pastXCoord + (xCoord - self.pastXCoord) / self.smoothingFactor
        ySmoothed = self.pastYCoord + (yCoord - self.pastYCoord) / self.smoothingFactor

        self.pastXCoord = xSmoothed
        self.pastYCoord = ySmoothed

        # Apparently this hogs resources if we don't add some delay.
        if gestures.isDetected:
            pag.moveTo(int(xSmoothed), int(ySmoothed), _pause=False)
        else:
            time.sleep(1/1000)
        """if handtrack.gestures.LMouseDown:
            pag.mouseDown(button='right')
            elif pastMouseDown:
                pag.mouseUp(button='right')
            pastMouseDown = handtrack.gestures.LMouseDown"""

"""
Separate mouse movement from the framerate of the camera which allows in 
between frame smoothing to occur. (catch up to last known value in between
frames. May need to adjust smoothingFactor to 1 / fps)
"""
def mouseThread(webcam, handtracker, mouse, ipc, dataLock, exitEvent):
    try:
        while not exitEvent.is_set():
            # Gain access to webcam, handtracker, ipc, and mouse for data use
            #with dataLock:
            mouse.update(handtracker.gestures)

    except Exception as err:
        print(err)
        exitEvent.set()
