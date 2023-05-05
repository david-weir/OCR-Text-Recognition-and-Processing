from langdetect import detect

# pass in the file and return the detected language
def detection_file(file):
    with open(file, "r") as language_file:
        text = language_file.read()
        try:
            return detect(text)
        
        except: # if it fails to detect the language
            return False
    