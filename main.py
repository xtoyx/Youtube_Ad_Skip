import cv2 as cv
import numpy as np
import os
import win32api
import easyocr

from time import time, sleep
from windowcapture import WindowCapture
from textdetection import TextDetection
from windowpositioncheck import WindowPositionChecker
DEBUG = False
SETPOS = True
SetX=0
SetY=0

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize the WindowCapture class
wincap = WindowCapture('Youtube Music')
# Create an instance of TextDetection
reader = easyocr.Reader(['en'], detector='dbnet18' ,gpu=False)
text_detector = TextDetection('target_image.png',reader)

wincap.start()

last_check_time = time()
loop_time = time()

while True:


    # Get an updated image of the window
    if wincap.screenshot is None:
        continue
    
    if SETPOS:
        WindowPos=WindowPositionChecker()
        bb,num=WindowPos.get_window_position(wincap.hwnd)
        count=0
        for i in num:
            if count==0 :
                SetX=i
                count+=1
            else :
                SetY=i
        print(f"x:{SetX} y:{SetY}")
        if WindowPos == None:
            me=input("Please Set A Position of skip button click 1 when u Ready \n")
            if me == "1":
                SETPOS=False
                count=0
                for i in win32api.GetCursorPos():
                    if count==0 :
                        SetX=i
                        count+=1
                    else :
                        SetY=i
                print(f"x:{SetX} y:{SetY}")
            #List of poistions One Screen:-
            #the window is in the right side :- x:1826 y:508
            #full window :- x:1100 y:807
            #50% window :- x:1808 y:610
            #Second Screen :-
            #the window is in the right side :- x:4510 y:728
            #full window :- x:3653 y:984
            #50% window :- x:4499 y:709
        else :
            SETPOS=False

    # Calculate time elapsed since the last check
    time_elapsed = time() - last_check_time
    # Perform text detection on the screenshot every 5 seconds
    if time_elapsed >= 4:
        start_timer=time()
        def runthisfunc():
            #crop then rescale it down so it faster to read duh
            grayscale = cv.cvtColor(wincap.screenshot, cv.COLOR_BGR2GRAY)
            # Define the coordinates of the region of interest (ROI) to crop
            x1, y1 = (int)(wincap.h/3), (int)(wincap.h/3)  # Top-left corner coordinates
            x2, y2 = wincap.w, wincap.w  # Bottom-right corner coordinates

            # Crop the ROI from the image
            cropped_image = grayscale[y1:y2, x1:x2]
            resized_cropped = cv.resize(cropped_image, None,fx=0.68, fy=0.68, interpolation=cv.INTER_CUBIC)

            #cv.imwrite('target_image.png', resized)
            cv.imwrite('target_image.png',resized_cropped)
            text_detector.target_img=resized_cropped
            #text_detector.target_img=resized
            # Detect and return bounding boxes of texts containing "skip"
            Skip_bounding_box = text_detector.detect_and_return_sponsored_bounding_boxes(confidence_threshold=0.5)
            # Make the click function if skip
            if Skip_bounding_box:
                print("Bounding Boxes of Skip Texts:", Skip_bounding_box)
                # x,y=wincap.get_screen_position((0,0))
                wincap.click(SetX,SetY)
       
        runthisfunc()
        print(f"{round(time()-start_timer,2)}")
        last_check_time = time()
    if DEBUG:
        # Display the screenshot with text detection and skip rectangles
        cv.imshow('Youtube Capture', wincap.screenshot)

        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()    

    # Press 'q' with the output window focused to exit
    # waits 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord('q'):
        wincap.stop()
        cv.destroyAllWindows()
        break

print('Done.')
