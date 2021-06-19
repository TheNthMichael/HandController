import cv2
import math

class WebCam:
    def __init__(self) -> None:
        # For webcam input:
        self.cap = cv2.VideoCapture(0)
        # these are floats
        self.width  = self.cap.get(3)
        self.height = self.cap.get(4)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame = None
        self.user_exit = False
        self.cap_fail_exit = False

    def update(self):
        success, image = self.cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            return
        self.frame = image

    """
    Display the passed image or the frame itself
    if image is None.
    Updates exit if there is an error or user exit.
    """
    def display(self, image=None):
        if image is None:
            image = self.frame

        # Add fps to image
        image = cv2.putText(image, "Fps: " + str(self.fps),
            (50,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (20,255,20),
            2,
            cv2.LINE_AA
            )

        # Show image
        cv2.imshow('MediaPipe Hands', image)

        # handle user input
        if cv2.waitKey(1) & 0xFF == 27:
            self.user_exit = True

    """
    Returns whether this class found that the program should end.
    """
    @property
    def state_exit(self):
        return (self.user_exit or self.cap_fail_exit)

    """
    Deconstructor that handles cv2 cleanup.
    """
    def __del__(self):
        self.cap.release()