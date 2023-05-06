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

    # translate from english to french and back again
    def test_translation_eachway_fr(self):
        eng_filepath = os.path.dirname(__file__) + "/" + 'englishtext.txt'
        
        english_file  = open(eng_filepath, 'r')
        english_txt = english_file.read()

        # translate in both directions
        generated_french = translate('en', 'fr', english_txt)
        new_english = translate('fr', 'en', generated_french)

        # get the similarity of the original english and the generated english
        self.assertGreaterEqual(self.normalise_levenshtein(english_txt, new_english), 0.80)
        english_file.close()

    # translate from english to german and back again
    def test_translation_eachway_de(self):
        eng_filepath = os.path.dirname(__file__) + "/" + 'englishtext.txt'
        
        english_file  = open(eng_filepath, 'r')
        english_txt = english_file.read()

        # translate in both directions
        generated_german = translate('en', 'de', english_txt)
        new_english = translate('de', 'en', generated_german)

        # get the similarity of the original english and the generated english
        self.assertGreaterEqual(self.normalise_levenshtein(english_txt, new_english), 0.80)
        english_file.close()

    # test of accuracy of english to french against french text
    def test_translation_en_fr(self):
        eng_filepath = os.path.dirname(__file__) + "/" + 'englishtext.txt'
        fr_filepath = os.path.dirname(__file__) + "/" + 'frenchtext.txt'
        
        english_file  = open(eng_filepath, 'r')
        english_txt = english_file.read()
        french_file = open(fr_filepath, 'r')
        french_txt = french_file.read()

        generated_french = translate('en', 'fr', english_txt)

        # compare the generated french with the reference french
        self.assertGreaterEqual(self.normalise_levenshtein(french_txt, generated_french), 0.80)

        english_file.close()
        french_file.close()

    # test of accuracy of english to french against french text
    def test_translation_en_de(self):
        eng_filepath = os.path.dirname(__file__) + "/" + 'englishtext.txt'
        de_filepath = os.path.dirname(__file__) + "/" + 'germantext.txt'
        
        english_file  = open(eng_filepath, 'r')
        english_txt = english_file.read()
        german_file = open(de_filepath, 'r')
        german_txt = german_file.read()

        generated_german = translate('en', 'de', english_txt)

        # compare the generated german with the reference german
        self.assertGreaterEqual(self.normalise_levenshtein(german_txt, generated_german), 0.80)

        english_file.close()
        german_file.close()

    # performance test of the translation time
    @unittest.skip("Will fail on CI/CD")
    def test_translation_time(self):
        eng_filepath = os.path.dirname(__file__) + "/" + 'englishtext.txt'
        english_file  = open(eng_filepath, 'r')
        english_txt = english_file.read()
        times = []
        while len(times) < 10: # translate the text 10 times
            start_time = time.time()

            translate("en", "fr", english_txt)
            
            end_time = time.time()
            elapsed_time = end_time - start_time # find how long each attempt took
            times.append(elapsed_time)

        english_file.close()
        avg_time = sum(times) / 10.0 # get average time taken for the translation
        print(avg_time)
        self.assertLessEqual(avg_time, 15.0)


if __name__ == '__main__':
    unittest.main()
