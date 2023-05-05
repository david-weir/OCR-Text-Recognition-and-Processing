import argparse
import json
from typing import List, Tuple

import editdistance

from htr_loaddata import IAMLoader, Batch
from htr_model import Model, DecoderType
from iam_preprocessing import Preprocessor
from path import Path
import cv2
import argparse

class Paths:
    """ Filepaths to data """
    charLst = './model/charList.txt'
    summary = './model/summary.json'
    corpus = './data/corpus.txt'


def get_img_size(line_mode: bool = False) -> Tuple[int, int]:
    """
        Get image size (wxh).
        Height is fixed for NN. Width depends on training mode (single word or text lines)
        as text lines require larger width images
    """
    if line_mode:
        return 256, 32  # w x h

    return 128, 32  # w x h


def write_summary(char_errorrates: List[float], word_accuracy: List[float]) -> None:
    """ Write a summary of the NN training """
    with open(Paths.summary, 'w') as f:
        json.dump({
            'charErrorRates': char_errorrates,
            'wordAccuracy': word_accuracy
        }, f)


def char_lst() -> List[str]:
    """ Extract char list from file """
    with open(Paths.charLst) as f:
        return list(f.read())


def train(model: Model, loader: IAMLoader, line_mode: bool, early_stopping: int = 25) -> None:
    """ Train NN """
    epoch = 0  # count of epochs

    # track summary data
    summ_char_err = []
    summ_word_accr = []

    preprocessor = Preprocessor(get_img_size(line_mode), data_augment=True, line_mode=line_mode)
    best_char_err = float('inf')  # current best validation char error rate (considering all rounds)
    last_improvement = 0  # number of epochs w/out improvement of character error rate

    # loop until number of epochs w/out improvement is >= the early stopping number
    while True:
        epoch += 1
        print('Epoch: ', epoch)

        # training
        print('Train Neural Network')
        loader.train_set()

        # loop while there is a next batch
        while loader.has_next():
            iter_info = loader.get_iterator_info()  # grabs batches completed and total number of batches
            batch = loader.get_next()
            batch = preprocessor.process_batch(batch)
            loss = model.train_batch(batch)

            print(f'Epoch: {epoch} Batch: {iter_info[0]}/{iter_info[1]} Loss: {loss}')

        # validate
        char_err_rate, word_accr = validate(model, loader, line_mode)

        # write summary
        summ_char_err.append(char_err_rate)
        summ_word_accr.append(word_accr)
        write_summary(summ_char_err, summ_word_accr)

        # if validation accr has improved => save new model params
        if char_err_rate < best_char_err:
            print('The Character Error Rate has improved: saving model...')
            best_char_err = char_err_rate  # update best char err rate
            last_improvement = 0  # reset improvement count
            model.save()
        else:
            print(f'The Character Error Rate has not improved. Best so far: {char_err_rate * 100.0}%')
            last_improvement += 1

        # reached early stopping point -> no improvement since x epochs => stop traininf
        if last_improvement >= early_stopping:
            print(f'Limit Reached: No improvement since {early_stopping} epochs. Training stopping...')
            break


def validate(model: Model, loader: IAMLoader, line_mode: bool) -> Tuple[float, float]:
    """ Validate NN """
    print('Validate NN')
    loader.validation_set()
    preprocessor = Preprocessor(get_img_size(line_mode), line_mode=line_mode)

    char_err = 0
    total_char = 0
    corr_words = 0  # a.k.a ok words
    total_words = 0

    while loader.has_next():
        iter_info = loader.get_iterator_info()
        print(f'Batch: {iter_info[0]} / {iter_info[1]}')

        batch = loader.get_next()
        batch = preprocessor.process_batch(batch)
        recognised, _ = model.inference_batch(batch)
        print('Ground Truth -> Recognized')

        # for element in all recognised words
        for i in range(len(recognised)):
            # update ok words and total words
            corr_words += 1 if batch.gt_texts[i] == recognised else 0
            total_words +=1

            # calculate edit distance between recognised text and ground truth text
            dist = editdistance.eval(recognised[i], batch.gt_texts[i])

            # update character error (from edit dist) and total chars seen
            char_err += dist
            total_char += len(batch.gt_texts)

            print('[OK]' if dist == 0 else '[ERR:%d]' % dist, '"' + batch.gt_texts[i] + '"', '->',
                  '"' + recognised[i] + '"')

        # print complete validation results
        char_err_rate = char_err / total_char
        word_accr = corr_words / total_words
        print(f'Character Error Rate: {char_err_rate * 100.0}%. Word accuracy: {word_accr * 100.0}%.')

        return char_err_rate, word_accr


def infer(model: Model, input_img: Path) -> None:
    """ Recognise text from an individual input image """
    img = cv2.imread(input_img, cv2.IMREAD_GRAYSCALE)
    assert img is not None

    preprocessor = Preprocessor(get_img_size(), dynamic_width=True, padding=16)
    img = preprocessor.process_img(img)

    batch = Batch([img], None, 1)
    recognised, prob = model.inference_batch(batch, True)

    print(f'Recognised: {recognised[0]}')


def parser() -> argparse.Namespace:
    """ Parse arguments from command line """
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', help='Choose mode.', choices=['train', 'validate', 'infer'], default='infer')
    parser.add_argument('--decoder', help='Choose a CTC decoder.', choices=['bestpath', 'beamsearch', 'wordbeamsearch'],
                        default='bestpath')
    parser.add_argument('--batch_size', help='Batch size.', type=int, default=100)
    parser.add_argument('--data_dir', help='Directory containing IAM dataset.', type=Path, required=False)
    parser.add_argument('--fast', help='Load samples from LMDB.', action='store_true')
    parser.add_argument('--line_mode', help='Train to read text lines instead of single words.', action='store_true')
    parser.add_argument('--img_file', help='Input image used for inference.', type=Path, default='../data/word.png')
    parser.add_argument('--early_stopping', help='Early stopping epochs.', type=int, default=25)

    return parser.parse_args()


def main():
    args = parser()  # parse cmd arguments
    decoder_map = {
        'bestpath': DecoderType.BestPath,
        'beamsearch': DecoderType.BeamSearch,
        'wordbeamsearch': DecoderType.WordBeamSearch
    }
    decoderType = decoder_map[args.decoder]  # set CTC decoder

    # if training mode
    if args.mode == 'train':
        loader = IAMLoader(args.data_dir, args.batch_size, fast=args.fast)

        char_list = loader.char_list  # load character list

        # ensure whitespace is in char lst if in line mode
        if args.line_mode and ' ' not in char_list:
            char_list = [' '] + char_list

        # save characters and words to corpus text file
        with open(Paths.corpus, 'w') as f:
            f.write(''.join(char_list))

        with open(Paths.corpus, 'w') as f:
            f.write(' '.join(loader.train_words + loader.validation_words))

        model = Model(char_list, decoderType)
        train(model, loader, line_mode=args.line_mode, early_stopping=args.early_stopping)

    # evaluate model on validation set
    elif args.mode == 'validate':
        loader = IAMLoader(args.data_dir, args.batch_size, fast=args.fast)
        model = Model(char_lst(), decoderType, restore=True)
        validate(model, loader, args.line_mode)

    # run inference on inputted image
    elif args.mode == 'infer':
        model = Model(char_lst(), decoderType, restore=True)
        infer(model, args.img_file)


if __name__ == '__main__':
    main()
