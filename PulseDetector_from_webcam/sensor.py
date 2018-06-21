import serial

class sensorReader:
    def __init__(self, comName, baudRate = 9600, timeout = 0.1):
        self.serialport = serial.Serial('COM3', baudRate, timeout = timeout)
        
        self.BPM = 0
        


    def close(self):
        #print(self.serialport)
        #if self.serialport != None:
        self.serialport.close()


    def read(self):
        val = str(self.serialport.readline())
        
        if len(val) > 1:
            val = str(val)
            val = val.strip()
            try:
                self.BPM = int(val)
            except:
                pass
        
        return self.BPM
                 
