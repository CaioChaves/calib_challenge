from cv2 import bilateralFilter
import numpy as np
import cv2
import argparse

input_video = "./labeled/0.mp4"

cap = cv2.VideoCapture(input_video)

# Corner Detection - parameters for ShiTomasi method
features_params = dict(maxCorners=400,
                       qualityLevel=0.3,
                       minDistance=7,
                       blockSize=7)

# Optical Flow - parameters for Lucas Kanade method
lk_params = dict(winSize=(15,15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,0.03))

# Create some randon colors
color = np.random.randint(0,255,(400,3))

# Take image and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame,cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray,mask=None,**features_params)

# Create mask image for drawing purposes
mask = np.zeros_like(old_frame)

while(True):
    ret, frame = cap.read()
    if not ret:
        print("No frames grabbed!")
        break

    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # Calculate optical flow
    p1,st,err = cv2.calcOpticalFlowPyrLK(old_gray,frame_gray,p0,None,**lk_params)

    # Select good points
    if p1 is not None:
        good_new = p1[st==1]
        good_old = p0[st==1]

    # Draw the tracks
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
        frame = cv2.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)
    img = cv2.add(frame, mask) 

    # Display image
    cv2.imshow("frame",img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    # Update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)

cv2.destroyAllWindows()



