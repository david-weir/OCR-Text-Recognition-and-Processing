# developed for running tests as part of the CI/CD pipeline
# extracts text from all images in a folder and outputs a text file of the extracted text
from PIL import Image
import pytesseract
import os


def main():

    # path to the folder of images
    folderpath = "./test/print text testing/data/"

    for folder in os.listdir(folderpath):
        # link to the file in which output needs to be stored
        resultpath = "./test/print text testing/ocr/" + (folder + ".txt")

        # iterate through and OCR images in folder
        for image in os.listdir(os.path.join(folderpath, folder)):
            img = Image.open(os.path.join(os.path.join(folderpath, folder), image))  # access the image

            # convert image to text (PLACEHOLDER eng for tests)
            text = pytesseract.image_to_string(img, lang="eng")

            # append text to the new text file (creating a file if it does not already exist)
            file1 = open(resultpath, "a+")

            # write to text file + close
            file1.write(text + "/n")
            file1.close()


if __name__ == '__main__':
    main()
