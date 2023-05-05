from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from nltk.tokenize import sent_tokenize
from nltk.tokenize import LineTokenizer
import math

def get_translation_model_and_tokenizer(src_lang, dst_lang):
    if torch.cuda.is_available():  # use the gpu if it is available
        dev = "cuda"
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
    if src not in supported_langs:
        raise ValueError('Language is not supported.')
    
    # https://stackoverflow.com/questions/68185061/strange-results-with-huggingface-transformermarianmt-translation-of-larger-tex
    model, tokenizer, device = get_translation_model_and_tokenizer(src, dst)
    # lt = LineTokenizer() # split a file into paragraphs on newlines
    batch_size = 8
    paragraphs = text.split('\n\n') #lt.tokenize(text)   
    translated_paragraphs = []

    for paragraph in paragraphs:
        sentences = sent_tokenize(paragraph)
        batches = math.ceil(len(sentences) / batch_size)     
        translated = []
        for i in range(batches):
            sent_batch = sentences[i*batch_size:(i+1)*batch_size]
            model_inputs = tokenizer(sent_batch, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
            with torch.no_grad():
                translated_batch = model.generate(**model_inputs)
            translated += translated_batch
        translated = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
        translated_paragraphs += [" ".join(translated)]

    translated_text = "\n\n".join(translated_paragraphs)
    return translated_text
    # inputs = tokenizer.encode(text, return_tensors="pt", max_length=512, truncation=True)

    # greedy_outputs = model.generate(inputs)
    # print(tokenizer.decode(greedy_outputs[0], skip_special_tokens=True))


    # generate the translation output using beam search
    # beam_outputs = model.generate(inputs, num_beams=2)
    # # decode the output and ignore special tokens
    # return tokenizer.decode(beam_outputs[0], skip_special_tokens=True)
