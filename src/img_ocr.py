# import the necessary packages
import pytesseract
import cv2
import sys
import preprocessing
from textModel import *

sys.path.insert(0, './src/gui')


def single_ocr(img_path):
    # OpenCV reads images as BGR not RGB
    # load the input image and convert it from BGR to RGB channel
    img = cv2.imread(img_path)  # load the image from given path
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # conversion to RGB

    # image preprocessing methods to improve OCR accuracy
    img = preprocessing.deskew(img)  # deskews an image with a tilt
    img = preprocessing.adaptive_threshold_binarisation(img)  # binarise the image using gaussian adaptive threshold
    img = preprocessing.denoise(img)  # image denoising

    # use Tesseract to OCR the image
    text = pytesseract.image_to_string(img)

    # open file to write OCR text to text file
    file1 = open("output.txt", "w")

    # write to text file + close
    file1.write(text + "/n")
    file1.close()

    # set new files to pass through to next steps (translation etc.)
    text_model.set_textfile("output.txt")
    text_model.set_output_file("output.txt")
    text_model.set_text()
    text_model.set_src_language()
    text_model.set_curr_language(text_model.get_src_language)
    text_model.set_filename(img_path)
