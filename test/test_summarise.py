import unittest
from src.summarise import summarisation
import os


class TestSummarisation(unittest.TestCase):

    # test the english text has been summarised
    def test_summarisation_en(self):
        eng_filepath = os.path.dirname(__file__) + "/" + 'englishtext.txt'
        
        summarised_en = summarisation(eng_filepath) # summarise the file
        english_file  = open(eng_filepath, 'r')
        english_txt = english_file.read()

        # assert length of summary is less than original file length
        self.assertLess(len(summarised_en), len(english_txt))

        english_file.close()

    # test the french text has been summarised
    def test_summarisation_fr(self):
        fr_filepath = os.path.dirname(__file__) + "/" + 'frenchtext.txt'
        
        summarised_fr = summarisation(fr_filepath) # summarise the file
        french_file  = open(fr_filepath, 'r')
        french_txt = french_file.read()

        # assert length of summary is less than original file length
        self.assertLess(len(summarised_fr), len(french_txt))

        french_file.close()

    # test the german text has been summarised
    def test_summarisation_de(self):
        de_filepath = os.path.dirname(__file__) + "/" + 'germantext.txt'
        
        summarised_de = summarisation(de_filepath) # summarise the file
        german_file  = open(de_filepath, 'r')
        german_txt = german_file.read()

        # assert length of summary is less than original file length
        self.assertLess(len(summarised_de), len(german_txt))

        german_file.close()
    
        