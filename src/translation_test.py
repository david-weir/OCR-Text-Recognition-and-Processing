import unittest
from translation import *
import jellyfish # need to install w pip
import time

class TestTranslation(unittest.TestCase):

    def normalise_levenshtein(self, str1, str2):
        score = jellyfish.levenshtein_distance(str1, str2)
        length = max(len(str1), len(str2))

        normalised_score = 1 - (score / length)

        return normalised_score

    
    def test_translation_en_de(self):
        self.assertEqual(translate("en", "de", "Hello, world"), "Hallo, Welt")


    def test_translation_eachway(self):
        english_str = "Hello, world"
        german_str = translate("en", "de", english_str)
        new_english_str = translate("de", "en", german_str)

        self.assertEqual(english_str, new_english_str)


    def test_translation_similarity(self):
        self.assertGreaterEqual(self.normalise_levenshtein("hello", "hello"), 0.9)


    def test_translation_time(self):
        start_time = time.time()
        
        english_str = "Hello, world"
        german_str = translate("en", "de", english_str)
        end_time = time.time()

        elapsed_time = end_time - start_time
        self.assertLessEqual(elapsed_time, 10.0)

if __name__ == '__main__':
    unittest.main()
