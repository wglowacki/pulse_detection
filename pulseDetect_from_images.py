import numpy as np
from numpy import fft
import cv2
import matplotlib.pyplot as plt
import time

class pulseDetect():
    def __init__(self, coord, filename):
        self.coord = coord
        
        #Process video @30fps with 1sec buffer
        self.buffer_size = 50
        self.fps = 29.3

        self.data_buffer = []
        self.samples = []
        self.freqs = []
        self.fft = []
        self.bpm = 0
        
        self.start_time = time.time()
        
        self.f_name = filename
        self.file = open(self.f_name, 'w')
        
        self.frame_in = 0
        self.idx = 1
        
        if self.f_name != None:
            self.file.write('Timestamp MeasuredBPM SensorBPM\n')
            
    
    def getROImeans(self):
        x, y, w, h = self.coord
        ROI = self.frame_in[y:y + h, x:x + w, :]
        ##v1 = np.mean(ROI[:, :, 0])
        v2 = np.mean(ROI[:, :, 1])
        #v3 = np.mean(ROI[:, :, 2])

        #return (v1 + v2 + v3) / 3.
        return v2

    def show(self):
        cv2.rectangle(self.frame_in,(self.coord[0],self.coord[1]),(self.coord[0]+self.coord[2],self.coord[1]+self.coord[3]),(0,255,0),3)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.frame_in,'BPM {}'.format(self.bpm),(self.coord[0],self.coord[1]), font, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow('Pulse',self.frame_in)
        cv2.waitKey(1)

         
    def run(self, frame):
        self.frame_in = frame

        #Get average of RGB values for ROI
        vals = self.getROImeans()
        self.data_buffer.append(vals)

        #Keep 30 last ROIs means (1sec buffer)
        L = len(self.data_buffer)
        if L > self.buffer_size:
            self.data_buffer = self.data_buffer[1:]
            L = self.buffer_size

        
        #With big enough buffer start processing pulse
        if L > 10:                        
            #We process images from 29.3fps sequence
            data = self.data_buffer
            data = data - np.mean(data)
            data = np.divide(data, np.std(data))
            
            #Get fft of buffered means
            raw = fft.rfft(data)
          
            #Amplitude
            self.fft = np.abs(raw)
            
            #Freqs
            self.freqs = np.linspace(0.0, 1.0/(2.0*(1/self.fps)), L//2 + 1)#Hz
            freqs = 60. * self.freqs #BPM

            idx = np.where((freqs > 50) & (freqs < 180))#Band pass filter (50-180BPM) 
            
            self.freqs = freqs[idx] #filtered freqs
            self.fft = self.fft[idx] #filtered amplitudes
            
            idx2 = np.argmax(self.fft) #max energy index

            self.bpm = self.freqs[idx2] #freq @max energy - pulse in BPM
        
        
        if self.f_name != None:
            if self.bpm != None:
                BPM = np.int(self.bpm)
                self.file.write(str(time.time()-self.start_time) + ' ' + str(BPM) + '\n')
            else:
                print(str(time.time()-self.start_time) + ' ' + str(BPM) + '\n')


if __name__ == "__main__":
    
    ROI = [[920, 300, 60, 60],[920, 240, 60, 60],[920, 300, 60, 60],[920, 270, 60, 60]]
    filename = 'log.txt'
    path = ['.\Test_data\Viedeo_data\emil_spoczynek_swiatlo_dzienne\emil_spoczynek_swiatlo_dzienne {:04}.jpg',
           '.\Test_data\Viedeo_data\emil_wysilek_swiatlo_dzienne\emil_wysilek_swiatlo_dzienne {:04}.jpg',
           '.\Test_data\Viedeo_data\wojtek_spoczynek_swiatlo_dzienne\wojtek_spoczynek_swiatlo_dzienne {:04}.jpg',
           '.\Test_data\Viedeo_data\wojtek_wysilek_swiatlo_dzienne\wojtek_wysilek_swiatlo_dzienne {:04}.jpg']
    
    number_of_images = [2264,2003,2100,2041]

    series = 1
    
#    I = cv2.imread(path[series].format(1))
#
#    cv2.rectangle(I,(ROI[series][0],ROI[series][1]),(ROI[series][0] + ROI[series][2], ROI[series][1] + ROI[series][3]),(0,255,0),3)
#    cv2.imshow('img',I)
    
    processor = pulseDetect(ROI[series],filename)

    for i in range(1,number_of_images[series]):
        img = path[series].format(i)

        I = cv2.imread(img)
        processor.run(I)
        
        processor.show()

        
    cv2.waitKey(0)
    cv2.destroyAllWindows()
