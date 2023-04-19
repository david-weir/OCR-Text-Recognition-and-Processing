import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from detection import *
import re

class textModel:
    def __init__(self, src_lang="", dst_lang="", format=""):
        self.src_lang = src_lang
        self.dst_lang = dst_lang
        self.curr_lang = ''
        self.format = format
        self.text = "this is the sample piece of text to show that it is working."
        self.textfile = ""
        self.filename = ""

    def set_src_language(self):
        self.src_lang = detection_text(self.text)
    
    def update_src_language(self, language):
        self.src_lang = language

    def get_src_language(self):
        return self.src_lang

    def set_dst_language(self, language):
        self.dst_lang = language

    def get_dst_language(self):
        return self.dst_lang

    def set_curr_language(self, language):
        self.curr_lang = language

    def get_curr_language(self):
        return self.curr_lang

    def set_format(self, format):
        self.format = format

    def get_format(self):
        return self.format

    def set_text(self):
        with open(self.get_textfile()) as input_file:
            head = [next(input_file).strip() for n in range(5)]
        self.text = " ".join(head)

    def get_text(self):
        return self.text

    def get_textfile(self):
        return self.textfile

    def set_textfile(self, textfile):
        self.textfile = textfile

    def get_output_file(self):
        return self.output_file

    def set_output_file(self, output_file):
        self.output_file = output_file

    def set_filename(self, filename):
        fname = str(filename)
        file = re.findall(r"'([^']*)'", fname)
        f = file[0].split('/')[-1]
        self.filename = f

    def get_filename(self):
        return self.filename

text_model = textModel()