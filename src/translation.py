from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from nltk.tokenize import sent_tokenize
import math

# pass the source and target languages to return necessary components
def get_translation_model_and_tokenizer(src_lang, dst_lang):
    if torch.cuda.is_available():  # use the gpu if it is available
        dev = "cuda" # gpu
    else:  
        dev = "cpu" 
    device = torch.device(dev) # set the device as gpu or cpu

    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{dst_lang}" # translation model
    # get the tokenizer and model for the language pair
    tokenizer = AutoTokenizer.from_pretrained(model_name) 
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.to(device)

    return model, tokenizer, device

def translate(src, dst, text):
    supported_langs = ['en', 'fr', 'de']
    if src not in supported_langs: # return an error
        raise ValueError('Language is not supported.')
    
    model, tokenizer, device = get_translation_model_and_tokenizer(src, dst)

    # code from https://stackoverflow.com/questions/68185061/strange-results-with-huggingface-transformermarianmt-translation-of-larger-tex
    batch_size = 8  # code will be processing 8 sentences at a time
    paragraphs = text.split('\n\n')  # split the text by paragraphs
    translated_paragraphs = []

    for paragraph in paragraphs:
        sentences = sent_tokenize(paragraph) # tokenise the sentences in the paragraph
        batches = math.ceil(len(sentences) / batch_size) # find how many batches there will be    
        translated = []
        for i in range(batches):
            sent_batch = sentences[i*batch_size:(i+1)*batch_size] # get batch of sentences 
            model_inputs = tokenizer(sent_batch, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
            with torch.no_grad(): # disables gradient calc
                translated_batch = model.generate(**model_inputs)
            translated += translated_batch
        translated = [tokenizer.decode(sentence, skip_special_tokens=True) for sentence in translated]
        translated_paragraphs += [" ".join(translated)]

    translated_text = "\n\n".join(translated_paragraphs) # rejoin the paragraphs for final text
    return translated_text
