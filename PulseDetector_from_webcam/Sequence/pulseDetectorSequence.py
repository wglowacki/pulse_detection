from pulseSequence import pulseDetect
from presenterSequence import dataPresenter
import cv2

#main program loop
if __name__ == "__main__":
    #pulseDetect processor settings
    ROI = [310, 170, 20, 20]
    buffer_size = 50
    presenter_buffer = 200
    filename = "log.txt"
    
    processor = pulseDetect(ROI, buffer_size)
    presenter = dataPresenter(ROI, presenter_buffer, filename=filename)

    while True:
        #Get frame from camera
        status, time, frame = camera.getFrame()

        #Pass frame to pulseDetect processor
        BPM, FPS = processor.run(frame)
        
        #Shoh results
        presenter.show(frame, BPM, FPS)

        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
       
    presenter.close()

