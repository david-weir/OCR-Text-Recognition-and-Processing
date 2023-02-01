import unittest
from src.detection import detection_text, detection_file

class TestDetection(unittest.TestCase):

    def test_en_detection_text(self):
        text = "This text is written in English."
        detected_lang = detection_text(text)

        self.assertEquals(detected_lang, "en")

    def test_en_detection_file(self):
        file = "englishtext.txt"
        detected_lang = detection_file(file)

        self.assertEquals(detected_lang, "en")
    
    def test_fr_detection_text(self):
        text = "Ce texte est écrit en français."
        detected_lang = detection_text(text)

        self.assertEquals(detected_lang, "fr")

    def test_fr_detection_file(self):
        file = "frenchtext.txt"
        detected_lang = detection_file(file)

        self.assertEquals(detected_lang, "fr")

    def test_de_detection_text(self):
        text = "Dieser Text ist in deutscher Sprache verfasst."
        detected_lang = detection_text(text)

        self.assertEquals(detected_lang, "de")

    def test_de_detection_file(self):
        file = "germantext.txt"
        detected_lang = detection_file(file)

        self.assertEquals(detected_lang, "de")

if __name__ == '__main__':
    unittest.main()
