import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowcapture import WindowCapture
from textdetection import TextDetection

DEBUG = False

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize the WindowCapture class
wincap = WindowCapture('Youtube Music')
# Create an instance of TextDetection
text_detector = TextDetection('target_image.png')

wincap.start()

last_check_time = time()
loop_time = time()

while True:


    # Get an updated image of the window
    if wincap.screenshot is None:
        continue

    # Calculate time elapsed since the last check

    time_elapsed = time() - last_check_time
    # Perform text detection on the screenshot every 5 seconds
    if time_elapsed >= 2:
        grayscale= cv.cvtColor(wincap.screenshot, cv.COLOR_BGR2GRAY)
        cv.imwrite('target_image.png', grayscale)
        # Detect and return bounding boxes of texts containing "sponsored"
        text_detector.target_img=cv.imread('target_image.png')
        Skip_bounding_box = text_detector.detect_and_return_sponsored_bounding_boxes(confidence_threshold=0.5)
        last_check_time = time()
        # Make the click function if sponsored
        if Skip_bounding_box:
            print("Bounding Boxes of Skip Texts:", Skip_bounding_box)
            x,y=wincap.get_screen_position((0,0))
            def calcdistance(x,y,top_left_x,top_right_x,bottom_left_y,top_left_y):
                top_left_x=top_left_x.item()
                bottom_left_y=bottom_left_y.item()
                top_right_x=top_right_x.item()
                x_click=x+(top_right_x-top_left_x)*4+top_right_x/2
                y_click=y+(top_right_x-top_left_x)*3.5+bottom_left_y/2 
                wincap.click(x_click,y_click)
            for i in Skip_bounding_box:
                top_left=i[0]
                top_right=i[1]
                bottom_left=i[3]
                top_left_x,top_left_y=top_left
                top_right_x,dropit=top_right
                dropit2,bottom_left_y=bottom_left
                calcdistance(x,y,top_left_x,top_right_x,bottom_left_y,top_left_y)
    # Skip_bounding_box = text_detector.detect_and_return_sponsored_bounding_boxes(wincap.screenshot,confidence_threshold=0.5)
    # # Make the click function if sponsored
    # if Skip_bounding_box:
    #     print("Bounding Boxes of Skip Texts:", Skip_bounding_box)
    #     x,y=wincap.get_screen_position((0,0))
    #     def calcdistance(x,y,top_left_x,top_right_x,bottom_left_y,top_left_y):
    #         top_left_x=top_left_x.item()
    #         bottom_left_y=bottom_left_y.item()
    #         top_right_x=top_right_x.item()
    #         x_click=x+(top_right_x-top_left_x)*4+top_right_x/2
    #         y_click=y+(top_right_x-top_left_x)*3.5+bottom_left_y/2 
    #         wincap.click(x_click,y_click)
    #         text_detector.sleepfor()
    #     for i in Skip_bounding_box:
    #         top_left=i[0]
    #         top_right=i[1]
    #         bottom_left=i[3]
    #         top_left_x,top_left_y=top_left
    #         top_right_x,dropit=top_right
    #         dropit2,bottom_left_y=bottom_left
    #         calcdistance(x,y,top_left_x,top_right_x,bottom_left_y,top_left_y)

        

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
