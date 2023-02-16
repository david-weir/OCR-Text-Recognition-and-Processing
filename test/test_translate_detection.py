import unittest
import os
from src.detection import detection_text, detection_file
from src.googletranslation import translate
import jellyfish
import time

class TestDetectionTranslationIntegration(unittest.TestCase):

    def normalise_levenshtein(self, str1, str2):
        score = jellyfish.levenshtein_distance(str1, str2)
        length = max(len(str1), len(str2))

        normalised_score = 1 - (score / length)

        return normalised_score
    
    def test_detect_translate(self):
        french_file = "frenchtext.txt"
        english_file = "englishtext.txt"
        fr_filepath = os.path.dirname(__file__) + "/" + french_file
        en_filepath = os.path.dirname(__file__) + "/" + english_file

        detected_lang = detection_file(fr_filepath)
        with open(fr_filepath, "r") as language_file:
            translated = translate(detected_lang, "en", language_file.read())
        new_detected_lang = detection_text(translated)
        self.assertEqual(detected_lang, "fr")
        self.assertEqual(new_detected_lang, "en")
        with open(en_filepath, "r") as en_file:
            self.assertGreaterEqual(self.normalise_levenshtein(translated, en_file.read()), 0.85)


if __name__ == '__main__':
    unittest.main()