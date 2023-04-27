import shutil
import unittest
import os
from src.convert import download_mp3, split_txtfile
import pathlib
from mutagen.mp3 import MP3

class TestAudio(unittest.TestCase):
    
    def test_audio_created(self):
        text = 'englishtext.txt'
        path = pathlib.Path(__file__).parent.resolve()

        text_path = os.path.join(path, text)
        download_mp3("en", text_path)
        new_path = os.path.join(path, 'englishtext.mp3')
        audio = MP3(new_path)
        
        self.assertTrue(os.path.exists(new_path))
        self.assertGreater(audio.info.length, 0)

    def test_empty_audio_created(self):
        text = 'empty.txt'
        path = pathlib.Path(__file__).parent.resolve()

        text_path = os.path.join(path, text)
        with self.assertRaises(AssertionError) as cm:
            download_mp3("en", text_path)
            self.assertEqual(str(cm.exception), 'No text to speak')

        new_path = os.path.join(path, 'empty.mp3')        
        self.assertFalse(os.path.exists(new_path))

    def test_split_audios(self):
        text = 'englishtext.txt'
        path = pathlib.Path(__file__).parent.resolve()

        text_path = os.path.join(path, text)
        os.mkdir('{}/mp3_segments'.format(path))
        txt_files = split_txtfile(text_path, 'mp3_segments')
        audio_files = []
        
        for file in txt_files:
            if file is not txt_files[-1]:
                with open(file, 'r') as f:
                    words = f.read().split()
                    self.assertEqual(len(words), 100)

            rec = download_mp3('en', file)
            audio_files.append(rec)
        
        for file in audio_files:
            if file is not audio_files[-1]:
                audio = MP3(file)
                self.assertTrue(35 <= audio.info.length <= 50)

        shutil.rmtree('{}/mp3_segments'.format(path))


if __name__ == '__main__':
    unittest.main()
