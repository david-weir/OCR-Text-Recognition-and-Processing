# CI/CD pipeline tests for print text OCR
import unittest
import jellyfish
import printdata_ocr


class TestPrintOCR(unittest.TestCase):

    # calculate the levenshtein edit distance between 2 strings (in this case 2 text files)
    def normalise_levenshtein(self, ocr, ground):
        score = jellyfish.levenshtein_distance(ocr, ground)
        length = len(ground)  # max length is length of the ground text file

        normalised_score = 1 - (score / length)  # normalise score between 0-1

        return normalised_score

    # edit distance test for Grimm's Fairy Tales
    def test_grimms(self):
        with open("./src/ocr_results/Grimms' Fairy Tales.txt", 'r', encoding="latin-1") as f1:
            ocr = f1.read().strip().replace('/n', '')

        with open("./test/print text testing/ground texts/Grimms' Fairy Tales by Jacob Grimm and Wilhelm Grimm.txt", 'r',
                  encoding="latin-1") as f2:
            ground = f2.read().strip().replace('/n', '')

        edit_dist = self.normalise_levenshtein(ocr, ground)

        f1.close()
        f2.close()

        self.assertGreaterEqual(edit_dist, 0.9, "Grimm's Fairy Tales Test FAILED - edit distance below 0.9")

    # edit distance test for Bram Stoker's Dracula
    def test_drac(self):
        with open("./src/ocr_results/Dracula.txt", 'r', encoding="latin-1") as f1:
            ocr = f1.read().strip().replace('/n', '')

        with open("./test/print text testing/ground texts/Dracula by Bram Stoker.txt", 'r',
                  encoding="latin-1") as f2:
            ground = f2.read().strip().replace('/n', '')

        edit_dist = self.normalise_levenshtein(ocr, ground)

        f1.close()
        f2.close()

        self.assertGreaterEqual(edit_dist, 0.9, "Dracula FAILED - edit distance below 0.9")

    # edit distance test for The Great Gatsby
    def test_gatsby(self):
        with open("./src/ocr_results/Great Gatsby.txt", 'r', encoding="latin-1") as f1:
            ocr = f1.read().strip().replace('/n', '')

        with open("./test/print text testing/ground texts/The Great Gatsby.txt", 'r',
                  encoding="latin-1") as f2:
            ground = f2.read().strip().replace('/n', '')

        edit_dist = self.normalise_levenshtein(ocr, ground)

        f1.close()
        f2.close()

        self.assertGreaterEqual(edit_dist, 0.9, "The Great Gatsby FAILED - edit distance below 0.9")


    def test_randj(self):
        with open("./src/ocr_results/Romeo and Juliet, William Shakespeare.txt", 'r',
                  encoding="latin-1") as f1:
            ocr = f1.read().strip().replace('/n', '')

        with open("./test/print text testing/ground texts/"
                  "The Project Gutenberg of Romeo and Juliet, William Shakespeare.txt", 'r', encoding="latin-1") as f2:
            ground = f2.read().strip().replace('/n', '')

        edit_dist = self.normalise_levenshtein(ocr, ground)

        f1.close()
        f2.close()

        self.assertGreaterEqual(edit_dist, 0.9, "Romeo & Juliet FAILED - edit distance below 0.9")


    def test_oss(self):
        with open("./src/ocr_results/oss handbook.txt", 'r', encoding="latin-1") as f1:
            ocr = f1.read().strip().replace('/n', '')

        with open("./test/print text testing/ground texts/Simple Sabotage Field Manual by United States.txt", 'r',
                  encoding="latin-1") as f2:
            ground = f2.read().strip().replace('/n', '')

        edit_dist = self.normalise_levenshtein(ocr, ground)

        f1.close()
        f2.close()

        self.assertGreaterEqual(edit_dist, 0.9, "Simple Sabotage Field Manual OSS FAILED - edit distance below 0.9")


if __name__ == '__main__':
    unittest.main()
