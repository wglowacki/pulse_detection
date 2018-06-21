from webcam import Camera
from pulse import pulseDetect
from presenter import dataPresenter
from sensor import sensorReader
import sys
import cv2

#main program loop
if __name__ == "__main__":
    #pulseDetect processor settings
    ROI = [310, 170, 20, 20]
    buffer_size = 50
    presenter_buffer = 200
    filename = "log.txt"
    
    processor = pulseDetect(ROI, buffer_size)
    camera = Camera()
    presenter = dataPresenter(ROI, presenter_buffer, filename=filename)
    sensor = sensorReader('COM3')
    
    if camera == None:
        sys.exit("Unable to connect to Camera")
    
    while True:
        #Get frame from camera
        status, time, frame = camera.getFrame()
        
        if status:
            #Pass frame to pulseDetect processor
            BPM, FPS = processor.run(frame, time)
            refBPM = sensor.read()
            
            #Shoh results
            presenter.show(frame, BPM, FPS, refBPM=refBPM)

        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
    
    camera.close()    
    presenter.close()
    sensor.close()

    