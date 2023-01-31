from langdetect import detect

def detection(file):
    with open(file, "r") as language_file:
        text = language_file.read()
        try:
            return detect(text)
        
        except:
            return False

#print(detection('text.txt'))
    