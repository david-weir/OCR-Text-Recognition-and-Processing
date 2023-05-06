import unittest
import os
from src.detection import detection_file
from src.translation import translate
import jellyfish
import time

class TestDetectionTranslationIntegration(unittest.TestCase):

    # find the levenshtein distance between two strings to find the dissimilarity
    def normalise_levenshtein(self, str1, str2):
        score = jellyfish.levenshtein_distance(str1, str2)
        length = max(len(str1), len(str2)) # find the longest of the two strings

        normalised_score = 1 - (score / length) # normalise the score to get a percentage

        return normalised_score
    
    # test how language detection and translation work together
    def test_detect_translate(self):
        french_file = "frenchtext.txt"
        english_file = "englishtext.txt"
        translated_file = "translated.txt"
        fr_filepath = os.path.dirname(__file__) + "/" + french_file
        en_filepath = os.path.dirname(__file__) + "/" + english_file
        translated = os.path.dirname(__file__) + "/" + translated_file

        detected_lang = detection_file(fr_filepath) # detect lang of file
        with open(fr_filepath, "r") as language_file:
            with open(translated, 'w') as f: # translate from detected lang to english
                f.write(translate(detected_lang, "en", language_file.read()))
            
        new_detected_lang = detection_file(translated)
        
        translated_txt = open(translated, 'r')
        self.assertEqual(detected_lang, "fr") # check it has detected correctly
        self.assertEqual(new_detected_lang, "en")
        with open(en_filepath, "r") as en_file:  # check the translation is accurate
            self.assertGreaterEqual(self.normalise_levenshtein(translated_txt.read(), en_file.read()), 0.85)

        translated_txt.close()
        os.remove(translated)

    # test what happens when detected lang is not supported
    def test_unsupported_lang(self):
        italian_file = 'italiantext.txt'
        it_filepath = os.path.dirname(__file__) + "/" + italian_file

        detected_lang = detection_file(it_filepath) # detected italian is not supported
        with open(it_filepath, "r") as language_file:
            self.assertRaises(ValueError, translate, detected_lang, 'en', language_file.read())
            
            with self.assertRaises(ValueError) as cm: # will return error when translating
                translate(detected_lang, 'en', language_file.read())
                self.assertEqual(str(cm.exception), 'Language is not supported.')
        
        self.assertEqual(detected_lang, "it")


if __name__ == '__main__':
    unittest.main()