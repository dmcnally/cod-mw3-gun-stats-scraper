import cv2
import pytesseract
from PIL import Image
import numpy as np

def find_and_draw_text(image_path, text_to_find):
    # Load the image file
    image = Image.open(image_path)

    # Convert image to OpenCV format
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Perform OCR to detect text
    text_data = pytesseract.image_to_data(image_cv, output_type=pytesseract.Output.DICT)

    # Loop through detected text regions
    for i in range(len(text_data['text'])):
        # Check if the detected text matches the specified text to find
        if text_data['text'][i].strip() == text_to_find.strip():
            x, y, w, h = text_data['left'][i], text_data['top'][i], text_data['width'][i], text_data['height'][i]
            cv2.rectangle(image_cv, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw blue box around text

    # Display modified image
    cv2.imshow('Highlighted Text', image_cv)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    image_path = input("/Users/amcnally/Desktop/Python Text Rec/image.jpeg")
    text_to_find = input("RAM-7")
    find_and_draw_text(image_path, text_to_find)