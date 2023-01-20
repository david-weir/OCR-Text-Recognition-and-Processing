# import the necessary packages
import pytesseract
import cv2
import sys
import preprocessing

# pytesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\admin\AppData\Local\Tesseract-OCR\tesseract.exe'

# OpenCV reads images as BGR not RGB
# load the input image and convert it from BGR to RGB channel
img = cv2.imread(sys.argv[1])  # load the image in the command line
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # conversion to RGB

# image preprocessing methods to improve OCR accuracy
img = preprocessing.deskew(img)  # deskews an image with a tilt
img = preprocessing.adaptive_threshold_binarisation(img)  # binarise the image using gaussian adaptive threshold

# use Tesseract to OCR the image
text = pytesseract.image_to_string(img)

print(text)
