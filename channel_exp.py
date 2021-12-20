from collections import deque
import numpy as np
import argparse
import imutils
import cv2


def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

orig = cv2.imread("sample_images/gball2.jpg", cv2.IMREAD_COLOR)

width = 640
height = 480
dim = (width, height)

resized = cv2.resize(orig, dim, interpolation = cv2.INTER_AREA)

cropped = resized[150:330, 0:640]

(B, G, R) = cv2.split(cropped)

# Set up the detector with default parameters.
params = cv2.SimpleBlobDetector_Params()

params.filterByColor = True
params.blobColor = 255
params.minThreshold = 120
params.maxThreshold = 255

params.filterByArea = True
params.maxArea = 25
params.minArea = 5

params.filterByCircularity = False
params.minCircularity = .9

params.filterByConvexity = False
params.filterByInertia = False

#dump(params) 

detector = cv2.SimpleBlobDetector_create(params)
 
# Detect blobs.
keypoints = detector.detect(B)
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(cropped, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
