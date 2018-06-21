import numpy as np
from numpy import fft
import matplotlib.pyplot as plt

class pulseDetect():
    def __init__(self, _ROI, _buffer_size):
        self.ROI = _ROI
        
        #Process video @30fps with 1sec buffer
        self.buffer_size = _buffer_size
        self.bpms_buffer = 10
        
        self.fps = 29.3
        self.frame_in = []
        self.time_samples = []
        self.data_buffer = []
        
        self.bpms = []
        self.avg_bpm = 0
 


    
    def getROImeans(self):
        #Get ROI
        x, y, w, h = self.ROI
        ROI = self.frame_in[y:y + h, x:x + w, :]

        #Return average of green pixels in ROI
        return np.mean(ROI[:, :, 1])
    
    
         
    def run(self, frame):
        self.frame_in = frame
        
        L = len(self.time_samples)
        
        #Get average of RGB values for ROI
        vals = self.getROImeans()
        self.data_buffer.append(vals)

        #Keep 30 last ROIs means (1sec buffer)
        if L > self.buffer_size:
            self.data_buffer = self.data_buffer[1:]
            self.time_samples = self.time_samples[1:]
            L = self.buffer_size

        
        #With big enough buffer start processing pulse
        if L > 10:                        
            #Normalize data
            norm_data = self.frame_in - np.mean(self.frame_in)
            norm_data = np.divide(norm_data, np.std(norm_data))
            
            #Get real fft of buffered means
            rawFFT = fft.rfft(norm_data)
            
            #Amplitude
            FFT = np.abs(rawFFT)
            
            #Freqs
            freqs = np.linspace(0.0, 1.0/(2.0*(1/self.fps)), L//2 + 1)#Hz
            freqs = 60. * freqs #BPM

            #Band pass filter (50-180BPM) 
            idxs = np.where((freqs > 50) & (freqs < 180))
            
            freqs = freqs[idxs] #filtered freqs
            FFT = FFT[idxs] #filtered amplitudes

            if FFT != []:
                idx = np.argmax(FFT) #max energy index
    
                bpm = freqs[idx] #freq @ max energy - pulse in BPM
            else:
                bpm = 0
                
            self.bpms.append(bpm)
            if len(self.bpms) > self.bpms_buffer:
                self.bpms = self.bpms[1:]
                
            self.avg_bpm = np.mean(self.bpms[-self.bpms_buffer:])
                
        return self.avg_bpm, self.fps

