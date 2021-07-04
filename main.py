from cv2 import data
import pydirectinput as pag
import cv2
import math
from threading import Lock, Event, Thread
from HandTracker import HandTracker
from WebCam import WebCam
from HandIPC import IPC, ipcThread
from Mouse import Mouse, mouseThread

webcam = WebCam()
handtracker = HandTracker(webcam.width, webcam.height)
mouse = Mouse(6, webcam.width, webcam.height)
ipc = IPC('127.0.0.1', 5000, 4000)

dataLock = Lock()
exitEvent = Event()

print("Note: When using this application for mouse movement,\nall Mouse Movements will be scaled from (",
            webcam.width, ", ", webcam.height, ") to (", mouse.winSizeX, ", ", mouse.winSizeY, ").\nFor now inconsistent aspect ratio's may cause uneven movement.")

# Create a new thread if using Mouse or IPC to deal with frame constraints
#mThread = Thread(target=mouseThread, args=(webcam, handtracker, mouse, ipc, dataLock, exitEvent, ))
#mThread.start()

hThread = Thread(target=ipcThread, args=(webcam, handtracker, mouse, ipc, dataLock, exitEvent, ))
hThread.start()

while not exitEvent.is_set():
    # Gain access to webcam, handtracker, ipc, and mouse
    #with dataLock:
    # Get new frame
    webcam.update()

    if webcam.state_exit:
        exitEvent.set()
    # We do nothing until the first frame is set.
    if webcam.frame is None:
        continue
    
    # Get the labelled image after its been proccessed.
    labelledImage = handtracker.processFrame(webcam.frame)

    # Display image
    webcam.display(labelledImage)

#mThread.join()
hThread.join()
print("Exiting...")


