import unittest
import os
import src.convert as convert
import pathlib
from mutagen.mp3 import MP3

class TestAudio(unittest.TestCase):
    
    def test_audio_created(self):
        text = 'englishtext.txt'
        path = pathlib.Path(__file__).parent.resolve()

        text_path = os.path.join(path, text)
        convert.download_mp3("en", text_path)
        new_path = os.path.join(path, 'englishtext.mp3')
        audio = MP3(new_path)
        
        self.assertTrue(os.path.exists(new_path))
        self.assertGreater(audio.info.length, 0)


if __name__ == '__main__':
    unittest.main()
