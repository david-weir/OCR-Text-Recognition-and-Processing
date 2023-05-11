""" Extract htr images from training data and perform HTR and check quality """
import os

import unittest
import jellyfish
import subprocess


class TestHTR(unittest.TestCase):

    # calculate the levenshtein edit distance between 2 strings (in this case 2 text files)
    def normalise_levenshtein(self, ocr, ground):
        score = jellyfish.levenshtein_distance(ocr, ground)
        length = len(ground)  # max length is length of the ground text file

        normalised_score = 1 - (score / length)  # normalise score between 0-1

        return normalised_score

    def run_write_htr(self):
        for img in os.listdir("./test/htr_tests/data/"):
            resultpath = "./test/htr_tests/htr_results/"

            img_file = "../../test/htr_tests/data/" + str(img)
            img_name_txt = img.strip().split(".")[0] + ".txt"

            htr = subprocess.check_output(["python", "main_htr.py", "--img_file", img_file],
                                          cwd="../src/htr")

            htr_out = htr.decode("utf-8").strip().split()
            recog_idx = htr_out.index("Recognised:")
            recog_txt = ' '.join(htr_out[recog_idx + 1:])

            file = open(resultpath + img_name_txt, "w")
            file.write(recog_txt)
            file.close()

    def test_htr(self):

        self.run_write_htr()

        for text_file in os.listdir("./test/htr_tests/htr_results/"):
            text_file_path = "./test/htr_tests/htr_results/" + str(text_file)
            gt_file_path = "./test/htr_tests/ground_truth/" + str(text_file)

            with open(text_file_path, "r") as f1:
                htr_text = f1.read().strip().split()

            with open(gt_file_path, "r") as f2:
                gt = f2.read().strip().split()

            edit_dist = self.normalise_levenshtein(str(htr_text), str(gt))

            f1.close()
            f2.close()

            self.assertGreaterEqual(edit_dist, 0.9, "Edit distance below 0.9")


if __name__ == '__main__':
    unittest.main()
