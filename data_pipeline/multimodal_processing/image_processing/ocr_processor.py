import pytesseract
import cv2
import logging
from PIL import Image
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('ocr_processor.log'), logging.StreamHandler()]
)

class OCRProcessor:
    def __init__(self, tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        logging.info("Initialized OCRProcessor.")

    def preprocess_image(self, image_path):
        logging.info(f"Preprocessing image: {image_path}")
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        logging.info("Image preprocessing complete.")
        return thresh

    def extract_text(self, image_path):
        preprocessed_image = self.preprocess_image(image_path)
        text = pytesseract.image_to_string(preprocessed_image)
        logging.info(f"Extracted text: {text[:50]}...")
        return text

if __name__ == "__main__":
    ocr = OCRProcessor()
    extracted_text = ocr.extract_text('path_to_image.jpg')
    print(extracted_text)
