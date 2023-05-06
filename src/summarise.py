from transformers import pipeline
from nltk.tokenize import sent_tokenize
import torch
import re

def summarisation(file):
    f = open(file, "r", encoding="utf8")
    text = f.read()

    if len(re.findall(r'\w+', text)) < 100: # if the text is less than 100 words, no need to summarise
        f.close()
        return text

    if torch.cuda.is_available():  # use the gpu if it is available
        dev = 0 # gpu
    else:  
        dev = -1 # cpu 

    sentences = sent_tokenize(text) # split the text into sentences
    sections = []
    chunk = []
    if len(text.split()) > 300:
        for sentence in sentences:
            chunk_size = " ".join(chunk) + sentence # length of chunk of text with the current sentence
            if len(re.findall(r'\w+', chunk_size)) < 300: # if it is less than 300 words
                chunk.append(sentence)
            else: # add completed chunk to the sections array and restart the chunk array with current sentnce
                sections.append(" ".join(chunk))
                chunk = []
                chunk.append(sentence)
    else: 
        sections.append(text)
   
    # initialise the summariser
    summariser = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=dev) #, device=dev
    # pass the array of sections to the summariser
    summarised = []
    for section in sections:
        summary = summariser(section, min_length=75, max_length=150, truncation=True)
        summarised.append(summary[0])

    joined_summ = "\n\n".join([summary['summary_text'] for summary in summarised]) # join all the sections
    complete_summ = re.sub(r'\s\.', r'.', joined_summ) # replace " ." with "."

    f.close()
    return complete_summ