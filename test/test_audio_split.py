import shutil
import unittest
import os
from src.convert import download_mp3
from src.split_text import split_txtfile
import pathlib
from mutagen.mp3 import MP3

class TestAudioSplitTextIntegration(unittest.TestCase):
    
    # integration test of mp3 and split text function
    def test_split_audios(self):
        text = 'englishtext.txt'
        path = pathlib.Path(__file__).parent.resolve()

        text_path = os.path.join(path, text)
        os.mkdir('{}/mp3_segments'.format(path)) # create the temp directory
        txt_files = split_txtfile(text_path, 'mp3_segments') # split the text file and add to dir
        audio_files = []
        
        for file in txt_files:
            if file is not txt_files[-1]:
                with open(file, 'r') as f:
                    words = f.read().split()
                    self.assertEqual(len(words), 100) # assert each chunk is the correct length

            rec = download_mp3('en', file) # convert chunk to mp3
            audio_files.append(rec)
        
        for file in audio_files:
            if file is not audio_files[-1]:
                audio = MP3(file)
                self.assertTrue(35 <= audio.info.length <= 50) # assert each track is not too long or short

        shutil.rmtree('{}/mp3_segments'.format(path)) # delete temp folder


if __name__ == '__main__':
    unittest.main()
