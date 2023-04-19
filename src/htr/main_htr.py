import json
from typing import List, Tuple
from htr_loaddata import IAMLoader, Batch
from htr_model import Model, DecoderType
from iam_preprocessing import Preprocessor
from path import Path

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
    pass

def infer(model: Model, input_img: Path) -> None:
    """ Recognise text from an input image """
    pass

