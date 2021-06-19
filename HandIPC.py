import socket
import struct
import traceback
import logging
import time


class IPC:
    def __init__(self, address, port) -> None:
        # Error handling
        self.server_exit = False
        self.state_exit = False
        self.server_fail_exit = False

        self.sock = socket.socket()
        socket.setdefaulttimeout(None)
        self.port = port
        self.addr = address
        self.sock.bind((self.addr, self.port))
        print("Socket created on ", self.addr, ":", self.port, "!")
        self.sock.listen(10)
        print("Socket Awaiting Connection...")
    
    def update(self, data):
        pass

    """
    Returns whether this class found that the program should end.
    """
    @property
    def state_exit(self):
        return (self.server_exit or self.state_exit or self.server_fail_exit)

    """
    Deconstructor that handles socket closing.
    """
    def __del__(self):
        pass