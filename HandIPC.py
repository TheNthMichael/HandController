import socket
import struct
from sys import exc_info
import traceback
import logging
import time
from matplotlib.pyplot import sca
import numpy as np


class IPC:
    def __init__(self, address, port, maxBufferSize) -> None:
        if maxBufferSize > 0 and maxBufferSize < 10000:
            self.MAX_BUFFER_SIZE = maxBufferSize
        else:
            self.MAX_BUFFER_SIZE = 4000
        self.sock = socket.socket()
        socket.setdefaulttimeout(None)
        self.port = port
        self.addr = address
        self.sock.bind((self.addr, self.port))
        print("Socket created on ", self.addr, ":", self.port, "!")
        self.sock.listen(10)
        print("Socket Awaiting Connection...")
    
    def update(self, data, exitEvent):
        try:
            if exitEvent.is_set():
                raise Exception("External notice to close connection")
            # Accept returns when a port connects
            con, addr = self.sock.accept()
            bytesReceived = con.recv(self.MAX_BUFFER_SIZE)

            # We can convert the bytes received into a numpy array where each element
            # is defined by dtype.
            dataReceived = np.frombuffer(bytesReceived, dtype=np.float32)

            # We can convert the array data into a byteBuffer that can be sent over the socket
            byteData = struct.pack('%sf' % len(data), *data)
            con.sendall(byteData)
            con.close()
        except Exception as err:
            print("Exception in IPC update: ", err.with_traceback)
            # Empty array indicates exit.
            con.sendall(bytearray([]))
            con.close()
            if not exitEvent.is_set():
                exitEvent.set()

    """
    Deconstructor that handles socket closing.
    """
    def __del__(self):
        pass


"""
Separate ipc communication from the framerate of the camera which allows
for continous feed of values over socket connection even if there are
duplicates. (may not be needed)
"""
def ipcThread(webcam, handtracker, mouse, ipc, dataLock, exitEvent):
    try:
        while not exitEvent.is_set():
            # Gain access to webcam, handtracker, ipc, and mouse for data use
            #with dataLock:
            data = []
            #handtracker.rightHand.landmark[0]

            if handtracker.gestures.isDetected:
                rh = handtracker.rightHand.landmark
                #line.pxs.append(p.x * 640 / (scaleFactor * 10))
                #line.pys.append((1-p.y) * 480 / (scaleFactor * 10))
                #line.pzs.append(p.z * 300 + scaleFactor * 300)
                for i in range(21):
                    data.append(rh[i].x * webcam.width / (handtracker.scaleFactor * 10))
                    data.append((1 - rh[i].y) * webcam.height / (handtracker.scaleFactor * 10))
                    zFactor = (webcam.height + webcam.width) / 2
                    data.append(rh[i].z * 600 + 300 * handtracker.scaleFactor)
            else:
                # We use a one element array to indicate waiting
                data = [1]

            ipc.update(data, exitEvent)

    except Exception as err:
        print(err)
        exitEvent.set()