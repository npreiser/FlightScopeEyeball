from collections import deque
import numpy as np
import argparse

from numpy.core.numeric import True_
import imutils
import cv2
import requests
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from stepper import stepforward,stepreverse,ismanualmode,manualpositionleft,initIO,cleanupIO

current_tray_position = 0 

TX_DATA = False  # set to enable/disable tranmsion of data.
TARGET_IP_ADDR = '192.168.1.73'

MANUAL_MODE = True #  determined by gpio 2 (pin 3) , if true manual, if false,= auto mode 
MANUAL_POSITION = True  # true = left  false == right,, 
# flag to reload config
reload_config = True

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))


# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])


# setup file watcher
class MyHandler(FileSystemEventHandler):
    
    def __init__(self, callback):
        self.callback = callback
        
    def on_modified(self, event):
        self.callback()
        print(f'event type: {event.event_type}  path : {event.src_path}')




if __name__ == "__main__":
    
    

    def callback():
        global reload_config
        reload_config = True
        print("File was modified")
        
        
    event_handler = MyHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

   

initIO()
# main loop

xstart=0
xend=600
ystart=120
yend=280

while True:
    
    # update local manual or auto mode 
    temp = ismanualmode()
    if temp != MANUAL_MODE: # if its changed... 
        MANUAL_MODE = temp
        print("manual auto mode switched:  %s " % MANUAL_MODE)
        
   
    if MANUAL_MODE == True:  # if you are in manual mode, check position, 
        temppos = manualpositionleft()
        if temppos != MANUAL_POSITION:
            MANUAL_POSITION = temppos
            print("Manul Position switched: %s " % MANUAL_POSITION)

            # move to the other side.. # true left,  false right, 
            if MANUAL_POSITION == True:
                stepreverse(1000)
                print("Moved manual left position")
            else:
                stepforward(1000)
                print("Moved manual right position")
    else:
        mycfg = ""
        if reload_config == True:
            print("loading config")
            reload_config = False
            f = open('config.json')
            mycfg = json.load(f)
            f.close()
            xstart=mycfg['crop_x_start']
            xend=mycfg['crop_x_end']
            ystart=mycfg['crop_y_start']
            yend=mycfg['crop_y_end']

        # grab the current frame
        (grabbed, frame) = camera.read()
        frame = imutils.rotate(frame, angle=180)
        orig = frame

        width = 640
        height = 480
        dim = (width, height)
        resized = cv2.resize(orig, dim, interpolation = cv2.INTER_AREA)

        cropped = resized[ystart:yend, xstart:xend]
        
        # orig = cv2.imread("gball2.jpg", cv2.IMREAD_COLOR)
        (B, G, R) = cv2.split(cropped)

        # Set up the detector with default parameters.
        params = cv2.SimpleBlobDetector_Params()

        params.filterByColor = True
        params.blobColor = 255
        params.minThreshold = 160
        params.maxThreshold = 255

        params.filterByArea = True
        params.maxArea = 40
        params.minArea = 10

        params.filterByCircularity = True
        params.minCircularity = .5

        params.filterByConvexity = False
        params.minConvexity = 0.2
        params.maxConvexity = 0.9
        
        params.filterByInertia = False
        params.minInertiaRatio = 0.9

    # dump(params) 

        detector = cv2.SimpleBlobDetector_create(params)
        
        # Detect blobs.
        keypoints = detector.detect(B)
        
        
        if len(keypoints) > 0:
            
        
            
            # data = {}
            
            holder = []  # array of objects 

            for i in keypoints:
                obj = {};
                obj['x'] = format(i.pt[0],".2f")
                obj['y'] = format(i.pt[1],".2f")
                obj['size'] = format(i.size,".2f")
                holder.append(obj)
                # print(format(i.pt[0],".2f"))
                
            #print(data)
            # print(len(keypoints))
            
            
            # send over data
            if TX_DATA == True:
                try:
                    api_url = "http://"+TARGET_IP_ADDR+":3000/setkeypoints"
                    response = requests.post(api_url, json=holder, timeout=1)      
                except requests.exceptions.RequestException as e: 
                    print("http error" ) 
            
        
            #  office cord .  535  ... 345 .... 175
            # 300 is dead center... +- 200 to each side. range = 100 : 300: 500
            # 
            # forward() # step forward... fixed ammount for now. 
        #  move = False
            """
            STEP_FACTOR = 100  # how many steps per pixel... 
            delta = 0
            # its inverted..  increase in pixel position.. move revers(ccw) .. 
            # map home(step = 0) to 535 x ball position.. 
            # take position and sub 535. 
            offset = 37
            temp = int(500+offset - i.pt[0])   # calc target position 
            direction = "R"
            
            if current_tray_position != temp:
                print("target position %d" % temp) 
            
            if temp > current_tray_position:
                delta = int(temp - current_tray_position)
                direction = "F"
            elif temp < current_tray_position:   
                delta = int(current_tray_position - temp)
                direction = "R"
            else:
                print("No need to move")
            
            
            if delta > 0:
                print("delta: "+format(delta,".2f") + "   dir: " + direction) 
                if direction == "R":
                    stepreverse(delta*STEP_FACTOR)
                    print("moved backward: ")
                    current_tray_position -= delta
                    print("current tray pos: %d" % (current_tray_position))
                elif direction == "F":
                    stepforward(delta*STEP_FACTOR)
                    print("moved forward: ")
                    current_tray_position += delta
                    print("current tray pos: %d" % (current_tray_position))
            """               

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv2.drawKeypoints(cropped, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        # Show keypoints
        cv2.imshow("Keypoints", im_with_keypoints)
        # cv2.waitKey(0)
        
        
        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
 
        
    
# cleanup the camera and close any open windows
# observer.join()
cleanupIO()
observer.stop()
camera.release()
cv2.destroyAllWindows()
