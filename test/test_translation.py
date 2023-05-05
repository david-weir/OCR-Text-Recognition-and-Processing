import unittest
from src.translation import translate
import jellyfish
import time
import os

class TestTranslation(unittest.TestCase):

    # find the levenshtein distance between two strings to find the dissimilarity
    def normalise_levenshtein(self, str1, str2):
        score = jellyfish.levenshtein_distance(str1, str2)
        length = max(len(str1), len(str2)) # find the longest of the two strings

        normalised_score = 1 - (score / length) # normalise the score to get a percentage

        return normalised_score

    
    def test_translation_en_de_short(self):
        self.assertEqual(translate("en", "de", "Hello, world"), "Hallo, Welt")


    def test_translation_eachway_short(self):
        english_str = "Hello, world"
        german_str = translate("en", "de", english_str)
        new_english_str = translate("de", "en", german_str)

        self.assertEqual(english_str, new_english_str)


    def test_translation_en_fr_long(self):
        eng_filepath = os.path.dirname(__file__) + "/" + 'englishtext.txt'
        fr_filepath = os.path.dirname(__file__) + "/" + 'frenchtext.txt'
        
        english_file  = open(eng_filepath, 'r')
        english_txt = english_file.read()
        french_file = open(fr_filepath, 'r')
        french_txt = french_file.read()

        generated_french = translate('en', 'fr', english_txt)

        self.assertGreaterEqual(self.normalise_levenshtein(french_txt, generated_french), 0.85)

        english_file.close()
        french_file.close()


    def test_translation_time(self):
        eng_filepath = os.path.dirname(__file__) + "/" + 'englishtext.txt'
        english_file  = open(eng_filepath, 'r')
        english_txt = english_file.read()
        
        start_time = time.time()

        translate("en", "fr", english_txt)
        
        end_time = time.time()
        elapsed_time = end_time - start_time

        english_file.close()

        self.assertLessEqual(elapsed_time, 15.0)

if __name__ == '__main__':
    unittest.main()
