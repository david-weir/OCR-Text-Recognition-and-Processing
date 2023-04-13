from transformers import pipeline
import re

def summarisation():
    f = open("text.txt", "r", encoding="utf8")
    to_tokenize = f.read()

    summariser = pipeline("summarization")
    summarized = summariser(to_tokenize, min_length=75, max_length=300)
    complete = re.sub(r'\s([?.!"](?:\s|$))', r'\1', summarized[0]['summary_text'])

    print(complete)