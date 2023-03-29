class textModel:
    def __init__(self, src_lang="", dst_lang="", format=""):
        self.src_lang = src_lang
        self.dst_lang = dst_lang
        self.format = format
        self.text = "this is the sample piece of text to show that it is working."
        self.textfile = ""

    def set_src_language(self, language):
        self.src_lang = language

    def get_src_language(self):
        return self.src_lang

    def set_dst_language(self, language):
        self.dst_lang = language

    def get_dst_language(self):
        return self.dst_lang

    def set_format(self, format):
        self.format = format

    def get_format(self):
        return self.format

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text

    def get_textfile(self):
        return self.textfile

    def set_textfile(self, textfile):
        self.textfile = textfile

text_model = textModel()