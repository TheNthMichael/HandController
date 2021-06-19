import pydirectinput as pag
import cv2
import math
from threading import Lock, Thread
from HandTracker import HandTracker
from WebCam import WebCam
from HandIPC import IPC
from Mouse import Mouse, mouseThread

webcam = WebCam()
handtracker = HandTracker(webcam.width, webcam.height)
mouse = Mouse(4, webcam.width, webcam.height)
ipc = IPC('127.0.0.1', 5000)

dataLock = Lock()

print("Note: When using this application for mouse movement,\nall Mouse Movements will be scaled from (",
            webcam.width, ", ", webcam.height, ") to (", mouse.winSizeX, ", ", mouse.winSizeY, ").\nFor now inconsistent aspect ratio's may cause uneven movement.")

# Create a new thread if using Mouse or IPC to deal with frame constraints
mThread = Thread(target=mouseThread, args=(webcam, handtracker, mouse, ipc, dataLock,))
mThread.start()

# create a callback function to handle exceptions in created threads.
callback = lambda thread, exception : {
    print("Exception in calling thread ", thread, " : ", exception)
}

while ("""AnyErrors"""):
    webcam.update()
