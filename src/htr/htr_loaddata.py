# loads in data from the IAM HTR dataset for use in model training
import random
from collections import namedtuple
from path import Path
from typing import Tuple
import numpy as np
import cv2

Sample = namedtuple('Sample', ('gt_text', 'file_path'))
Batch = namedtuple('Batch', ('imgs', 'gt_texts', 'batchsize'))

''' 
Load data from the IAM dataset  
https://fki.tic.heia-fr.ch/databases/iam-handwriting-database
'''


class IAMLoader:
    def __init__(self, data_dir: Path, batchsize: int, data_split: 0.95) -> None:

        assert data_dir.exists()

        self.data_augment = False
        self.curr_id = 0
        self.batchsize = batchsize
        self.samples = []

        words_file = open("../words.txt")  # summary of word data in IAM Dataset
        chars = set()
        broken_words = ['a01-117-05-02', 'r06-022-03-05']  # ids of known broken word images

        for line in words_file:

            # skip empty lines and comments
            line = line.strip()

            if not line or line[0] == '#':
                continue

            # each line consists of 9 space delimited sections
            split_line = line.split(' ')
            assert len(split_line) >= 9  # check each split line contains at least 9 parts

            # split filename into different parts
            # part1/part1-part2/part1-part2-part3.png
            filename_split = split_line[0].split('-')  # split a01-000u-00-00
            subdir1 = filename_split[0]  # a01
            subdir2 = f'{filename_split[0]}-{filename_split[1]}'  # a01-000u
            file_id = split_line[0] + ".png"  # Image in subdirectories: a01-000u-00-00.png
            filename = data_dir / "img" / subdir1 / subdir2 / file_id  # data/img/a01/a01-000u/a01-000u-00-00

            # skip over broken word images
            if split_line[0] in broken_words:
                print("Skipping known broken image: ", filename)
                continue

            gt_text = ' '.join(split_line[8:])  # ground text of an image start at col 9 (can continue if considering
                                                # line/senetnce date)
            chars = chars.union(set(list(gt_text)))

            # append samples to Samples list
            self.samples.append(Sample(gt_text, filename))

        # divide data into training (95%) and validation (5%) sets
        split_id = int(data_split * len(self.samples))
        self.train_samples = self.samples[:split_id]
        self.validation_samples = self.samples[split_id]

        # populate lists with words
        self.train_words = [x.gt_text for x in self.train_samples]
        self.validation_words = [x.gt_text for x in self.validation_samples]

        # start on training set
        self.train_set()

        # lists all characters in dataset
        self.char_list = sorted(list(chars))

    ''' Choose a random subset of the training set '''
    def train_set(self) -> None:
        self.data_augment = True
        self.curr_id = 0

        random.shuffle(self.train_samples)

        self.samples = self.train_samples
        self.curr_set = 'train'

    ''' Switch from training set to validation set'''
    def validation_set(self) -> None:
        self.data_augment = False
        self.curr_id = 0
        self.samples = self.validation_samples
        self.curr_set = 'val'

    ''' Get current batch index & overall batch count '''
    def get_iterator_info(self) -> Tuple[int, int]:
        # grab number of batches
        if self.curr_set == 'train':
            num_batches = int(np.floor(len(self.samples) / self.batchsize))  # train set: only full-sized batches
        else:
            num_batches = int(np.ceil(len(self.samples) / self.batchsize))

        curr_batch = self.curr_id // self.batchsize + 1
        return curr_batch, num_batches

    ''' Checks for next element '''
    def has_next(self) -> bool:
        if self.curr_set == 'train':
            return self.curr_id + self.batchsize <= len(self.samples)  # training set consists of only complete batches
        else:
            return self.curr_id < len(self.samples)  # the final batch in the validation set can be smaller (incomplete)

    ''' Gets image '''
    def get_img(self, i: int) -> np.ndarray:
        img = cv2.imread(self.samples[i].file_path, cv2.IMREAD_GRAYSCALE)

        return img

    ''' Get next element '''
    def get_next(self) -> Batch:
        # get range of batches
        batchrange = range(self.curr_id, min(self.curr_id + self.batchsize, len(self.samples)))

        imgs = [self.get_img(i) for i in batchrange]
        gt_texts = [self.samples[i].gt_text for i in batchrange]

        self.curr_id += self.batchsize
        return Batch(imgs, gt_texts, len(imgs))

