from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import requests
import json

TX_DATA = True  # set to enable/disable tranmsion of data.
TARGET_IP_ADDR = '192.168.1.73'

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

# keep looping
while True:
	# grab the current frame
    (grabbed, frame) = camera.read()
    frame = imutils.rotate(frame, angle=180)
    orig = frame

    width = 640
    height = 480
    dim = (width, height)
    resized = cv2.resize(orig, dim, interpolation = cv2.INTER_AREA)
    cropped = resized[120:280, 0:600]
    
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
        data = {}
        
        holder = []  # array of objects 

        for i in keypoints:
            obj = {};
            obj['x'] = format(i.pt[0],".2f")
            obj['y'] = format(i.pt[1],".2f")
            obj['size'] = format(i.size,".2f")
            holder.append(obj)
            
        #print(data)
        print(len(keypoints))
        
        # send over data
        if TX_DATA == True:
            try:
                api_url = "http://"+TARGET_IP_ADDR+":3000/setkeypoints"
                response = requests.post(api_url, json=holder, timeout=1)      
            except requests.exceptions.RequestException as e: 
                 print("http error" ) 
        
    
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
camera.release()
cv2.destroyAllWindows()
