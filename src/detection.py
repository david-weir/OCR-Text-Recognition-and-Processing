from langdetect import detect, DetectorFactory

# pass in the file and return the detected language
def detection_file(file):
    DetectorFactory.seed = 0 # make the result deterministic
    with open(file, "r") as language_file:
        text = language_file.read()
        try:
            return detect(text)
        
        except: # if it fails to detect the language
            return False