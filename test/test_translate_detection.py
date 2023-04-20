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

    def test_unsupported_lang(self):
        italian_file = 'italiantext.txt'
        it_filepath = os.path.dirname(__file__) + "/" + italian_file

        detected_lang = detection_file(it_filepath)
        with open(it_filepath, "r") as language_file:
            self.assertRaises(ValueError, translate, detected_lang, 'en', language_file.read())
            
            with self.assertRaises(ValueError) as cm:
                translate(detected_lang, 'en', language_file.read())
                self.assertEqual(str(cm.exception), 'Language is not supported.')
        
        self.assertEqual(detected_lang, "it")

    def test_detect_translate_time(self):
        start_time = time.time()

        german_file = "germantext.txt"
        de_filepath = os.path.dirname(__file__) + "/" + german_file

        detected_lang = detection_file(de_filepath)
        with open(de_filepath, "r") as language_file:
            translated = translate(detected_lang, "en", language_file.read())
        
        end_time = time.time()
        
        new_detected_lang = detection_text(translated)

        self.assertEqual(detected_lang, "de")
        self.assertEqual(new_detected_lang, "en")
        elapsed_time = end_time - start_time
        self.assertLessEqual(elapsed_time, 10.0)

if __name__ == '__main__':
    unittest.main()