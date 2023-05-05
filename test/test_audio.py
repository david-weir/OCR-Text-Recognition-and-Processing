import unittest
import os
from src.convert import download_mp3
import pathlib
from mutagen.mp3 import MP3

class TestAudio(unittest.TestCase):
    
    # test if the audio file has been created
    def test_audio_created(self):
        text = 'englishtext.txt'
        path = pathlib.Path(__file__).parent.resolve()

        text_path = os.path.join(path, text)
        download_mp3("en", text_path) # convert text to mp3
        new_path = os.path.join(path, 'englishtext.mp3')
        audio = MP3(new_path)
        
        self.assertTrue(os.path.exists(new_path)) # check there is a path to the new file
        self.assertGreater(audio.info.length, 0) # check that the length of the audio is greater than 0 seconds

        os.remove(new_path)

    # test to see if function will create empty mp3
    def test_empty_audio_created(self):
        text = 'empty.txt' # an empty file with no text
        path = pathlib.Path(__file__).parent.resolve()

        text_path = os.path.join(path, text)
        with self.assertRaises(AssertionError) as cm:
            download_mp3("en", text_path)
            self.assertEqual(str(cm.exception), 'No text to speak')

        new_path = os.path.join(path, 'empty.mp3')        
        self.assertFalse(os.path.exists(new_path)) # path has not been created


if __name__ == '__main__':
    unittest.main()
