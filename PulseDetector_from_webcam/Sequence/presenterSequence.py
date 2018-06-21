import cv2
import numpy as np
import matplotlib.pyplot as plt
import time


class dataPresenter:
    def __init__(self, _ROI, _buffer_size,  filename = None):
        self.ROI = _ROI
        self.font = cv2.FONT_HERSHEY_SIMPLEX   
        
        self.buffer_size = _buffer_size
        self.BPM = []
        self.start_time = time.time()
        
        self.f_name = None
        
        if filename != None:
            self.f_name = filename
            self.file = open(filename, 'w')
            self.file.write('Timestamp MeasuredBPM SensorBPM\n')
        else:
            self.file = None
        
        
        plt.figure(1)

            
    def close(self):
        cv2.destroyAllWindows()
        if self.f_name!= None:
            self.file.close()
        plt.close()

    
    def show(self, frame, BPM, FPS):
        x, y, w, h = self.ROI
        
        self.BPM.append(BPM)
        
        if len(self.BPM) > self.buffer_size:
            self.BPM = self.BPM[1:]
        
        #If initialized with filname put data to file
        if self.file != None:
            BPM = np.int(BPM)
            self.file.write(str(time.time()-self.start_time) + ' ' + str(BPM) + '\n')
        
        #Plot data
        plt.clf()
        plt.plot(self.BPM)

        plt.xlabel("Sample")
        plt.ylabel("BPM")
        plt.ylim(0, 150)
        plt.legend(['Camera BMP'], loc='lower right')
        plt.pause(0.001)
        
        
        #Draw ROI rectangle
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
        
        #Put Text
        cv2.putText(frame, 'To quit pres ESC', (10,30), self.font, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, 'FPS {:.0f}'.format(FPS), (10,60), self.font, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, 'BPM {:.0f}'.format(BPM), (320,30), self.font, 1, (255,255,255), 2, cv2.LINE_AA)
        
        #Show current frame
        cv2.imshow('Pulse', frame)
        cv2.waitKey(1) 