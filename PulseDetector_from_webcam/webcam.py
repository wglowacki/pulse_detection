import cv2
import time

class Camera:
    def __init__(self):
        vc = cv2.VideoCapture(0)
        if vc.isOpened():
            self.vc = vc
        else:
            self.vc = None
            
        self.frame = None
        self.time = 0
        
    def close(self):
        self.vc.release()
        
    def getFrame(self):
        rval, frame = self.vc.read()
        if rval:
            self.frame = frame
            self.time = time.time()
            
        return rval, self.time, self.frame
        