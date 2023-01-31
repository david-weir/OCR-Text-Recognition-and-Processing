from langdetect import detect

def detection_file(file):
    with open(file, "r") as language_file:
        text = language_file.read()
        try:
            return detect(text)
        
        except:
            return False

def detection_text(text):
    try:
        return detect(text)
    except:
        return False

#print(detection('text.txt'))
    