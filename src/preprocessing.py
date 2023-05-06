# Preprocessing methods to improve / allow OCR
import cv2
import numpy as np
from skimage.color import rgb2gray
from skimage.transform import rotate
from deskew import determine_skew


# gaussian adaptive threshold binarisation
def adaptive_threshold_binarisation(img):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert the image to greyscale

    # calculate the local threshold value using Gaussian weighting and a mean value
    thresh = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 4)

    return thresh


# provides image deskewing to improve accuracy on imperfect (tilted) images
def deskew(image):
    grayscale = rgb2gray(image)  # convert the image to grayscale and flip the foreground
    angle = determine_skew(grayscale)  # determine the tilt/skew angle of the text

    rotated = rotate(image, angle, resize=True) * 255  # transforms the image rotating it by the calculated angle to an
    # upright position - set resize to True to avoid cutting off
    # part of the image during rotation

    return rotated.astype(np.uint8)  # returns an unsigned integer (0-255) representing an image with RGB channels


# smooth the image by removing patches of relatively high intensity using non-local means denoising
def denoise(img):
    # denoise the already greyscale/binary image
    dst = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)

    return dst

