from googletrans import Translator, constants
from pprint import pprint

# init the Google API translator
def translate(src, dst, text):
    translator = Translator()
    supported = ['en', 'fr', 'de']
    if src not in supported:
        raise ValueError('Language is not supported.')
    # translate a spanish text to english text (by default)
    translation = translator.translate(text)
    # print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
    return translation.text