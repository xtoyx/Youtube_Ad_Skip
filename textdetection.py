import cv2 as cv
import easyocr


class TextDetection:
    # properties
    target_image_path=""
    reader=""
    target_img=""

    def __init__(self, target_image_path):
        self.target_image_path = target_image_path
        self.reader = easyocr.Reader(['en'], gpu=False)
        self.target_img = cv.imread(target_image_path)

    def detect_and_return_sponsored_bounding_boxes(self,confidence_threshold=0.7):
        
        result = self.reader.readtext(self.target_img)
        sponsored_bounding_boxes = self._draw_unique_rectangles(result, confidence_threshold)
        return sponsored_bounding_boxes

    def _draw_unique_rectangles(self, text_detections, confidence_threshold):
        sponsored_bounding_boxes = []

        for detection in text_detections:
            text, confidence = detection[1], detection[2]

            if "skip" in text.lower() and confidence >= confidence_threshold:
                bounding_box = tuple(map(tuple, detection[0]))
                sponsored_bounding_boxes.append(bounding_box)
                # Draw rectangle around the text region
                top_left = bounding_box[0]
                bottom_right = bounding_box[2]
                cv.rectangle(self.target_img, top_left, bottom_right, (0, 255, 0), 2)
                cv.imwrite('result_image.jpg', self.target_img)
                # Print bounding box coordinates and text
                print(f"Bounding Box: {top_left}, {bottom_right}")
                print(f"Text: {text}, Confidence: {confidence}")

        return sponsored_bounding_boxes      
