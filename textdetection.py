import cv2 as cv
import win32api

class TextDetection:
    # properties
    target_image_path=""
    reader=""
    target_img=""

    def __init__(self, target_image_path,reader):
        self.target_image_path = target_image_path
        self.reader=reader
        self.target_img = cv.imread(target_image_path)

    def detect_and_return_sponsored_bounding_boxes(self,confidence_threshold):     
        result = self.reader.readtext(self.target_img,batch_size=5)
        sponsored_bounding_boxes = self._draw_unique_rectangles(result, confidence_threshold)
        return sponsored_bounding_boxes

    def _draw_unique_rectangles(self, text_detections, confidence_threshold):
        sponsored_bounding_boxes = []

        for detection in text_detections:
            text, confidence = detection[1], detection[2]
            #incudle you can skip and it will be too fast or perfect 
            if ("skip" in text.lower()) and confidence >= confidence_threshold:
                bounding_box = tuple(map(tuple, detection[0]))
                sponsored_bounding_boxes.append(bounding_box)
                break
                # # Draw rectangle around the text region
                # try:
                #     top_left = bounding_box[0]
                #     bottom_right = bounding_box[2]
                #     # Resize the image
                #     # resized_img = cv.resize(self.target_img, None, fx=0.8, fy=0.8, interpolation=cv.INTER_CUBIC)

                #     # # Convert the resized image to grayscale
                #     # gray_img = cv.cvtColor(resized_img, cv.COLOR_BGR2GRAY)
                #     # cv.rectangle(gray_img, top_left, bottom_right, (0, 255, 0), 2)
                #     # cv.imwrite('result_image.png', gray_img)
                #     # Print bounding box coordinates and text
                #     print(f"Bounding Box: {top_left}, {bottom_right}")
                #     print(f"Text: {text}, Confidence: {confidence}")
                    
                #     # Get dimensions of the application window image
                #     # window_height, window_width, _ = self.target_img.shape

                #     # print("Window width:", window_width)
                #     # print("Window height:", window_height)
                    
                #     # # Get the dimensions of the screen (screenshot)
                #     # screenshot_width = win32api.GetSystemMetrics(0)
                #     # screenshot_height = win32api.GetSystemMetrics(1)

                #     # print("Screenshot width:", screenshot_width)
                #     # print("Screenshot height:", screenshot_height)
                    
                #     # click_position = self.convert_to_click_position(bounding_box, window_height, window_width, screenshot_width, screenshot_height)
                #     # print(f"click : {click_position}")
                    
                # except Exception as e:
                #     print("An exception occurred" ,e) 
                
                

        return sponsored_bounding_boxes  
    
    def convert_to_click_position(self, bounding_box, window_height, window_width, screenshot_width, screenshot_height):
        # Calculate center of the bounding box
        center_x = (bounding_box[0][0] + bounding_box[2][0]) / 2
        center_y = (bounding_box[0][1] + bounding_box[2][1]) / 2

        # Get the offset between the window and the screen
        border_pixels = 8
        titlebar_pixels = 30
        offset_x = border_pixels
        offset_y = titlebar_pixels + border_pixels

        # Adjust center coordinates based on the offset
        center_x += offset_x
        center_y += offset_y

        # Convert center coordinates to click position
        click_position_x = (center_x / window_width) * screenshot_width 
        click_position_y = (center_y / window_height) * screenshot_height
        win32api.SetCursorPos(((int)(click_position_x.item()), (int)(click_position_y.item())))
        return click_position_x, click_position_y