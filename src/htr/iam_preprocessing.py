# Preprocess images loaded from the IAM HTR dataset
from typing import Tuple

import numpy as np

from htr_loaddata import Batch
import random
import cv2


class Preprocessor:
    def __init__(self, img_size: Tuple[int, int], padding: int = 0, dynamic_width: bool = False,
                 data_augment: bool = False, line_mode: bool = False) -> None:

        # only support dynamic width if there is NO data augmentation
        assert not (dynamic_width and data_augment)

        # padding requires dynamic width
        assert not (padding > 0 and not dynamic_width)

        self.img_size = img_size
        self.padding = padding
        self.dynamic_width = dynamic_width
        self.data_augmentation = data_augment
        self.line_mode = line_mode

    '''
        ctc loss must be able to map text labels to input labels.
        Repeated letters cost double (because of blank symbols). If a label is too long ctc loss
        returns an infinite gradient.
    '''
    ''' Calculate the cost (including doubles) and truncate labels that are too long '''
    @staticmethod
    def truncate_label(text: str, max_len: int) -> str:
        cost = 0

        # for letter in text
        for i in range(len(text)):
            # account for double letters equalling double cost
            if i != 0 and text[i] == text[i - 1]:
                cost += 2
            else:
                cost += 1

            # if cost exceeds label max -> truncate the label
            if cost > max_len:
                return text[:i]

        return text  # return label

    ''' Generates an image of an IAM sentence by pasting several IAM word images into a single image '''
    def sim_textline(self, batch: Batch) -> Batch:

        # default values
        default_word_sep = 30
        default_num_words = 5

        # store resulting images and ground texts
        res_imgs = []
        res_gt_texts = []

        # loop over all batch elements
        for i in range(batch.batchsize):
            # number of words used in the current line
            # if data augmentation = True set number of words to a random integer 1-8 else revert to default
            num_words = random.randint(1, 8) if self.data_augmentation else default_num_words

            # combine the ground texts of each word image to make up the gt of the line
            # and append to the list of ground texts
            curr_gt = ' '.join([batch.gt_texts[(i + j) % batch.batchsize] for j in range(num_words)])
            res_gt_texts.append(curr_gt)

            # store word images in list + calculate the target image size
            select_imgs = []
            word_seps = [0]

            h = 0
            w = 0
            for j in range(num_words):
                curr_img = batch.imgs[(i + j) % batch.batchsize]
                curr_word_sep = random.randint(20, 50) if self.data_augmentation else default_word_sep

                # set h, w
                h = max(h, curr_img.shape[0])
                w += curr_img.shape[1]

                select_imgs.append(curr_img)
                if j + 1 < num_words:
                    w += curr_word_sep
                    word_seps.append(curr_word_sep)

            # place all selected word images in target img
            target = np.ones([h, w], np.uint8) * 255
            x = 0
            for curr_img, curr_word_sep in zip(select_imgs, word_seps):
                x += curr_word_sep
                y = (h - curr_img.shape[0]) // 2
                target[y:y + curr_img.shape[0]:, x:x + curr_img.shape[1]] = curr_img

            res_imgs.append(target)

        return Batch(res_imgs, res_gt_texts, batch.batchsize)

    ''' Resize image to target size, and optionally apply data augmentation '''
    def process_img(self, img: np.ndarray) -> np.ndarray:

        # replace damage IAM image files with a blank black image
        if img is None:
            img = np.zeros(self.img_size[::-1])

        # data augmentation
        img = img.astype(np.float64)
        if self.data_augmentation:

            # photometric data augmentation
            if random.random() < 0.25:
                def rand_odd():
                    return random.randint(1, 3) * 2 + 1

                img = cv2.GaussianBlur(img, (rand_odd(), rand_odd()), 0)

            if random.random() < 0.25:
                img = cv2.dilate(img, np.ones((3, 3)))
            if random.random() < 0.25:
                img = cv2.erode(img, np.ones((3, 3)))

            # geometric data augmentation
            wt, ht = self.img_size
            h, w = img.shape

            f = min(wt / w, ht / h)
            fx = f * np.random.uniform(0.75, 1.05)
            fy = f * np.random.uniform(0.75, 1.05)

            # random position around center
            txc = (wt - w * fx) / 2
            tyc = (ht - h * fy) / 2
            freedom_x = max((wt - fx * w) / 2, 0)
            freedom_y = max((ht - fy * h) / 2, 0)
            tx = txc + np.random.uniform(-freedom_x, freedom_x)
            ty = tyc + np.random.uniform(-freedom_y, freedom_y)

            # map image into target image
            m = np.float32([[fx, 0, tx], [0, fy, ty]])
            target = np.ones(self.img_size[::-1]) * 255
            img = cv2.warpAffine(img, m, dsize=self.img_size, dst=target, borderMode=cv2.BORDER_TRANSPARENT)

            # photometric data augmentation
            if random.random() < 0.5:
                img = img * (0.25 + random.random() * 0.75)
            if random.random() < 0.25:
                img = np.clip(img + (np.random.random(img.shape) - 0.5) * random.randint(1, 25), 0, 255)
            if random.random() < 0.1:
                img = 255 - img

            # no data augmentation
        else:
            if self.dynamic_width:
                ht = self.img_size[1]
                h, w = img.shape
                f = ht / h

                wt = int(f * w + self.padding)
                wt = wt + (4 - wt) % 4

                tx = (wt - w * f) / 2
                ty = 0
            else:
                wt, ht = self.img_size
                h, w = img.shape
                f = min(wt / w, ht / h)

                tx = (wt - w * f) / 2
                ty = (ht - h * f) / 2

            # map image onto target image
            m = np.float32([[f, 0, tx], [0, f, ty]])
            target = np.ones([ht, wt]) * 255
            img = cv2.warpAffine(img, m, dsize=(wt, ht), dst=target, borderMode=cv2.BORDER_TRANSPARENT)

        img = cv2.transpose(img)  # get transpose for tensorflow

        # convert image to range [-1, 1]
        img = img / 255 - 0.5
        return img

    def process_batch(self, batch: Batch) -> Batch:
        # generates batch of sentences for line mode instead of using singular words
        if self.line_mode:
            batch = self.sim_textline(batch)

        res_imgs = [self.process_img(img) for img in batch.imgs]  # all processed images in the batch
        max_len = res_imgs[0].shape[0] // 4
        res_gt = [self.truncate_label(gt, max_len) for gt in batch.gt_texts]

        return Batch(res_imgs, res_gt, batch.batchsize)
