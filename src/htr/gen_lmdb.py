import argparse
import pickle

import cv2
import lmdb
from path import Path

# handle cmd argument for directory of IAM database
parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', type=Path, required=True)
args = parser.parse_args()

assert not (args.data_dir / 'lmdb').exists()  # check lmdb does not exist

# map size controls the size of the lmdb database. 2GB covers the IAM dataset (so it can work on 64-bit and 32-bit
env = lmdb.open(str(args.data_dir / 'lmdb'), map_size=1024 * 1024 * 1024 * 2)  # new lmdb environment

# walk over all png files
input_imgs = list((args.data_dir / 'img').walkfiles('*.png'))

# convert into lmdb as pickled greyscale images - new write transaction
with env.begin(write=True) as txn:
    for i, input_img in enumerate(input_imgs):
        print(i, len(input_imgs))
        img = cv2.imread(input_img, cv2.IMREAD_GRAYSCALE)  # read image in OpenCV and convert to greyscale
        basename = input_img.basename()
        txn.put(basename.encode("ascii"), pickle.dumps(img))  # represents data as a byte object

env.close()  # close lmdb environ
