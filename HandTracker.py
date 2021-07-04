import cv2
from matplotlib import scale
import mediapipe as mp
import math
import matplotlib.pyplot as plt

class Line:
    def __init__(self):
        self.pxs = []
        self.pys = []
        self.pzs = []

class Graph:
    def __init__(self, title):
        plt.ion()
        self.title = title
        self.figure = plt.figure()
        self.figure.suptitle(title)
        self.ax = self.figure.gca(projection="3d")
        self.ax.axes.set_xlim([-10, 10])
        self.ax.axes.set_zlim([-10, 10])
        self.ax.axes.set_ylim([-10,10])
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')
        self.figure.show()
        self.lines = []
        self.pastScaleFactor = 1

    """
    Add a line between multiple points in a sequence.
    """
    def addLine(self, points, scaleFactor):
        line = Line()
        for p in points:
            line.pxs.append(p.x * 640 / (scaleFactor * 10))
            line.pys.append((1-p.y) * 480 / (scaleFactor * 10))
            line.pzs.append((p.z + 1) * 300 + scaleFactor * 300)
        self.lines.append(line)
        self.pastScaleFactor = scaleFactor

    def update(self):
        if len(self.lines) != 0:
            for line in self.lines:
                self.ax.plot(
                line.pxs,
                line.pzs,
                line.pys,
                color="r",
                )
                self.ax.scatter(
                    line.pxs,
                    line.pzs,
                    line.pys,
                    c='b',
                    s=25
                )
            
            self.lines.clear()
            #self.figure.canvas.draw()
        else:
            self.ax.plot([],[],[])
        self.ax.axes.set_xlim([-50, 650])
        self.ax.axes.set_zlim([-50, 450])
        self.ax.axes.set_ylim([-50,550])
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')
        plt.pause(0.001)
        self.ax.cla()


class Gestures:
    def __init__(self):
        self.isDetected = False
        self.LMouseDown = False
        self.RMouseDown = False
        self.ScrollDown = False
        self.pointerX = 0
        self.pointerY = 0


"""
Class for tracking hands to be used for tracking and gesture recognition.
Lets define some useful parts of mediapipe Hands library to use:

"""
class HandTracker:
    
    def __init__(self, width, height):
        print("Creating HandTracker:\n\tFrameSize=(", width,",", height, ")")
        self.vidWidth = width
        self.vidHeight = height
        self.hasGraph = True
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.3
        )
        self.leftHand = None
        self.rightHand = None
        self.scaleFactor = 1
        self.gestures = Gestures()
        if self.hasGraph:
            self.graph = Graph("test 3d hand")
    
    """
    Chooses how to define the pointer ex below is center of mass of points around palm.
    """
    def getPointer(self, hand):
        cx, cy = 0,0
        points = []
        points.append(hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP])
        #points.append(hand.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP])
        #points.append(hand.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP])
        #points.append(hand.landmark[self.mp_hands.HandLandmark.PINKY_MCP])
        #points.append(hand.landmark[self.mp_hands.HandLandmark.WRIST])
        #points.append(hand.landmark[self.mp_hands.HandLandmark.THUMB_CMC])

        for p in points:
            cx += p.x
            cy += p.y

        numpoints = len(points)
        return cx / numpoints, cy / numpoints

    def getLMouseDown(self, hand):

        return False

    # Get a scale factor from the average pixel distances between landmarks
    def getUnscaledDepth(self, hand):
        sum = 0
        wrist = hand.landmark[self.mp_hands.HandLandmark.WRIST]
        indexmcp = hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        pinkymcp = hand.landmark[self.mp_hands.HandLandmark.PINKY_MCP]
        thumbcmc = hand.landmark[self.mp_hands.HandLandmark.THUMB_CMC]
        middlemcp = hand.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        ringmcp = hand.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP]
        pinkypip = hand.landmark[self.mp_hands.HandLandmark.PINKY_PIP]
        points = [wrist, indexmcp, pinkymcp, thumbcmc, middlemcp, ringmcp, pinkymcp, pinkypip]

        # sum each possible pair 
        for x in points:
            for y in points:
                if x != y:
                    sum += math.dist([x.x, x.y, x.z], [y.x, y.y, y.z])
        scaleFactor = sum / (len(points)**2)
        return scaleFactor
    
    def create3dGraph(self, hand):
        scaleFactor = self.getUnscaledDepth(hand)
        print("Scale Factor: ", scaleFactor)

        # Thumb
        points = []
        points.append(hand.landmark[self.mp_hands.HandLandmark.WRIST])
        points.append(hand.landmark[self.mp_hands.HandLandmark.THUMB_CMC])
        points.append(hand.landmark[self.mp_hands.HandLandmark.THUMB_MCP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.THUMB_IP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.THUMB_TIP])
        self.graph.addLine(points, scaleFactor)

        # Index
        points.clear()
        points.append(hand.landmark[self.mp_hands.HandLandmark.WRIST])
        points.append(hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_DIP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP])
        self.graph.addLine(points, scaleFactor)

        # Middle
        points.clear()
        points.append(hand.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_DIP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP])
        self.graph.addLine(points, scaleFactor)

        # Ring
        points.clear()
        points.append(hand.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.RING_FINGER_DIP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP])
        self.graph.addLine(points, scaleFactor)

        # Pinky
        points.clear()
        points.append(hand.landmark[self.mp_hands.HandLandmark.WRIST])
        points.append(hand.landmark[self.mp_hands.HandLandmark.PINKY_MCP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.PINKY_PIP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.PINKY_DIP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.PINKY_TIP])
        self.graph.addLine(points, scaleFactor)

        # Connectors
        points.clear()
        points.append(hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP])
        points.append(hand.landmark[self.mp_hands.HandLandmark.PINKY_MCP])
        self.graph.addLine(points, scaleFactor)




    """
    Sets the Gestures object's properties to indicate
    certain actions and movements.
    """
    def setGestures(self, hand):
        # DO NOT FORGET THIS WHEN TESTING OR YOU WILL NEED TO SHUT OFF YOUR PC!!!!!!!
        self.gestures.LMouseDown = False

        self.gestures.isDetected = True

        # Set gesture for pointer
        
        self.gestures.pointerX, self.gestures.pointerY = self.getPointer(hand)

        # Get depth
        
        self.scaleFactor = self.getUnscaledDepth(hand)

        # set gesture for clicking

        self.gestures.LMouseDown = self.getLMouseDown(hand)

    """
    Returns "left" if the hand index of the hand passed was the left hand.
    Returns None otherwise.
    """
    def getLabel(self, index, hands, results):
        for idx, classification in enumerate(results.multi_handedness):
            if classification.classification[0].index == index:
                return classification.classification[0].label
        return None
    
    """
    Call this for each frame of your video or camera feed.
    handles mediapipe calls internally and sets the gestures
    for the current frame.
    """
    def processFrame(self, frame):
        # Flip image so that the user sees their hands correctly
        # And convert to RGB so that hands can use it.
        image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

        # set this to false such that if the frame doesn't encounter a hand, we know.
        self.gestures.isDetected = False

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = self.hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            # Just get the first index finger shown
            for num, hand_landmarks in enumerate(results.multi_hand_landmarks):
                #print(self.getLabel(num, hand_landmarks, results))
                if self.getLabel(num, hand_landmarks, results) != "Left":
                    # set the gestures used during frame
                    self.rightHand = hand_landmarks
                    self.setGestures(hand_landmarks)
                    if self.hasGraph:
                        self.create3dGraph(hand_landmarks)
                    # draw based on gestures
                    self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                    self.mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2),
                    )
                    

            if self.gestures.LMouseDown:
                cv2.circle(
                    image,
                    (int(self.gestures.pointerX * self.vidWidth),
                    int(self.gestures.pointerY * self.vidHeight)),
                    5,
                    (0,255,0),
                    2
                    )
            else:
                cv2.circle(
                    image,
                    (int(self.gestures.pointerX * self.vidWidth),
                    int(self.gestures.pointerY * self.vidHeight)),
                    5,
                    (255,0,0),
                    2
                    )
            if self.hasGraph:
                self.graph.update()

        return image
                

