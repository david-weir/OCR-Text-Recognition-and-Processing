from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

def get_translation_model_and_tokenizer(src_lang, dst_lang):
    if torch.cuda.is_available():  
        dev = "cuda"
    else:  
        dev = "cpu" 
    device = torch.device(dev)
    # construct our model name
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{dst_lang}"
    # initialize the tokenizer & model
    tokenizer = AutoTokenizer.from_pretrained(model_name) # need PyTorch not Tensorflow !!!
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.to(device)
    # return them for use
    return model, tokenizer

def translate(src, dst, text):
    supported_langs = ['en', 'fr', 'de']
    if src not in supported_langs:
        raise ValueError('Language is not supported.')
    
    model, tokenizer = get_translation_model_and_tokenizer(src, dst)
    inputs = tokenizer.encode(text, return_tensors="pt", max_length=512, truncation=True)

    """# generate the translation output using greedy search
    greedy_outputs = model.generate(inputs)
    # decode the output and ignore special tokens
    print(tokenizer.decode(greedy_outputs[0], skip_special_tokens=True))"""


    # generate the translation output using beam search
    beam_outputs = model.generate(inputs, num_beams=2)
    # decode the output and ignore special tokens
    return tokenizer.decode(beam_outputs[0], skip_special_tokens=True)

def split_text(text):
    paragraphs = text.split('\n\n')
    # print(paragraphs)
    # for paragraph  in paragraphs:
    translate('en', 'fr', paragraphs[0])


def run():
    with open('text.txt', 'r') as f:
        text = f.read()
        split_text(text)

# run()
# beam search or greedy search ?? beam returns more accurate results but may be slower
# need to compare