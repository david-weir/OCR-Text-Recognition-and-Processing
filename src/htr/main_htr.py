import json
from typing import List, Tuple

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
