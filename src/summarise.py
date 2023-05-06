from transformers import pipeline
from nltk.tokenize import sent_tokenize
import torch
import re

def summarisation(file):
    f = open(file, "r", encoding="utf8")
    text = f.read()

    if len(re.findall(r'\w+', text)) < 100:
        f.close()
        return text

    if torch.cuda.is_available():  # use the gpu if it is available
        dev = 0 # gpu
    else:  
        dev = -1 # cpu 

    sentences = sent_tokenize(text)
    sections = []
    chunk = []
    for sentence in sentences:
        chunk_size = " ".join(chunk) + sentence
        if len(re.findall(r'\w+', chunk_size)) < 300:
            chunk.append(sentence)
        else:
            sections.append(" ".join(chunk))
            chunk = []

    summariser = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=dev)
    summarised = summariser(sections, min_length=75, max_length=150, truncation=True)

    joined_summ = " ".join([summary['summary_text'] for summary in summarised])
    complete_summ = re.sub(r'\s\.', r'.', joined_summ)

    f.close()
    return complete_summ