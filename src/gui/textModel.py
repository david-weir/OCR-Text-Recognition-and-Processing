import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from detection import *
import re

class textModel:
    def __init__(self):
        self.reset()

    def reset(self):
        self.src_lang = ''
        self.dst_lang = ''
        self.curr_lang = ''
        self.format = ''
        self.textfile = ''
        self.output_file = ''
        self.filename = ''
        self.dir_path = ''

    def set_src_language(self):
        self.src_lang = detection_file(self.textfile)
    
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

    def get_textfile(self):
        return self.textfile

    def set_textfile(self, textfile):
        self.textfile = textfile

    def get_output_file(self):
        return self.output_file

    def set_output_file(self, output_file):
        self.output_file = output_file

    def set_filename(self, file_path):
        # fname = str(file_path)
        # file = re.findall(r"'([^']*)'", fname)
        filename = file_path.split('/')[-1]
        self.filename = filename

    def get_filename(self):
        return self.filename

    def get_dir_path(self):
        return self.dir_path

    def set_dir_path(self, dir_path):
        self.dir_path = dir_path

    def get_language_dict(self):
        self.lang_codes = {
            "English": "en",
            "French": "fr",
            "German": "de",
            "en": "English",
            "fr": "French",
            "de": "German"
        }

        return self.lang_codes

text_model = textModel()