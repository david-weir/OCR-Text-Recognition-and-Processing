# extracts text from all images in a folder and outputs a text file of the extracted text
from PIL import Image
import pytesseract
import os
import sys
from textModel import *

sys.path.insert(0, './src/gui')


def folders_ocr(folder_path):

    file1 = open("output.txt", "w")
    # iterate through and OCR images in folder
    for image in os.listdir(os.path.join(folder_path)):
        img = Image.open(os.path.join(os.path.join(folder_path), image))  # access the image

        # convert image to text (PLACEHOLDER eng for tests)
        text = pytesseract.image_to_string(img, lang="eng")

        # append text to the new text file (creating a file if it does not already exist)
        file1 = open("output.txt", "+a")  # output.txt should be deleted after user downloads pdfs etc

        # write to text file + close
        file1.write(text + "\n")
        file1.close()

        # set new files to pass through to next steps (translation etc.)
        text_model.set_textfile("output.txt")
        text_model.set_output_file("output.txt")
        text_model.set_src_language()
        text_model.set_curr_language(text_model.get_src_language())
        text_model.set_filename(folder_path)
