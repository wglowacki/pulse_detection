import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time


class dataPresenter:
    def __init__(self, _ROI, _buffer_size,  filename = None):
        self.ROI = _ROI
        self.font = cv2.FONT_HERSHEY_SIMPLEX   
        
        self.buffer_size = _buffer_size
        self.BPM = []
        self.refBPM = []
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

    
    def show(self, frame, BPM, FPS, refBPM = None):
        x, y, w, h = self.ROI
        
        self.BPM.append(BPM)
        if refBPM != None:
            self.refBPM.append(refBPM)
            
            if len(self.refBPM) > self.buffer_size:
                self.refBPM = self.refBPM[1:]
        
        if len(self.BPM) > self.buffer_size:
            self.BPM = self.BPM[1:]
        
        #If initialized with filename put data to file
        if self.file != None:
            if refBPM != None:
                BPM = np.int(BPM)
                refBPM = np.int(refBPM)
                self.file.write(str(time.time()-self.start_time) + ' ' + str(BPM) + ' ' + str(refBPM) + '\n')
            else:
                BPM = np.int(BPM)
                self.file.write(str(time.time()-self.start_time) + ' ' + str(BPM) + '\n')
        
        #Plot data
        plt.clf()
        plt.plot(self.BPM)
        
        if refBPM != None:
            plt.plot(self.refBPM)
        
        plt.xlabel("Sample")
        plt.ylabel("BPM")
        plt.ylim(0, 150)
        plt.legend(['Camera BMP','Sensor BMP'], loc='lower right')
        plt.pause(0.001)
        
        
        
        #Draw ROI rectangle
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
        
        #Put Text
        cv2.putText(frame, 'To quit pres ESC', (10,30), self.font, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, 'FPS {:.0f}'.format(FPS), (10,60), self.font, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, 'BPM {:.0f}'.format(BPM), (320,30), self.font, 1, (255,255,255), 2, cv2.LINE_AA)
        if refBPM != None:
            cv2.putText(frame, 'Sensor BPM {:.0f}'.format(refBPM), (320,60), self.font, 1, (255,255,255), 2, cv2.LINE_AA)
        
        #Show current frame
        cv2.imshow('Pulse', frame)
        cv2.waitKey(1) 