import unittest
import os
from src.detection import detection_file

class TestDetection(unittest.TestCase):

    # test that the function can detect English
    def test_en_detection(self):
        file = "englishtext.txt"
        filepath = os.path.dirname(__file__) + "/" + file
        
        detected_lang = detection_file(filepath)

        self.assertEqual(detected_lang, "en")

    # test that the function can detect English in short file
    def test_en_detection_short(self):
        file = "short_eng_text.txt"
        filepath = os.path.dirname(__file__) + "/" + file
        
        detected_lang = detection_file(filepath)

        self.assertEqual(detected_lang, "en")

    # test that the function can detect French
    def test_fr_detection(self):
        file = "frenchtext.txt"
        filepath = os.path.dirname(__file__) + "/" + file

        detected_lang = detection_file(filepath)

        self.assertEqual(detected_lang, "fr")

    # test that the function can detect French in short file
    def test_fr_detection_short(self):
        file = "short_fr_text.txt"
        filepath = os.path.dirname(__file__) + "/" + file

        detected_lang = detection_file(filepath)

        self.assertEqual(detected_lang, "fr")

    # test that the function can detect German
    def test_de_detection(self):
        file = "germantext.txt"
        filepath = os.path.dirname(__file__) + "/" + file

        detected_lang = detection_file(filepath)

        self.assertEqual(detected_lang, "de")

    # test that the function can detect German in short file
    def test_de_detection_short(self):
        file = "short_de_text.txt"
        filepath = os.path.dirname(__file__) + "/" + file

        detected_lang = detection_file(filepath)

        self.assertEqual(detected_lang, "de")

    # test that the function will return False if it cannot detect a language
    def test_detection_empty(self):
        file = "empty.txt"
        filepath = os.path.dirname(__file__) + "/" + file

        detected_lang = detection_file(filepath)

        self.assertFalse(detected_lang)

if __name__ == '__main__':
    unittest.main()
