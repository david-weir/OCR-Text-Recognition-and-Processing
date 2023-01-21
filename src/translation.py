import sys
from transformers import *

src, dst, text = sys.argv[1:]

def get_translation_model_and_tokenizer(src_lang, dst_lang):
    # construct our model name
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{dst_lang}"
    # initialize the tokenizer & model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    # return them for use
    return model, tokenizer

model, tokenizer = get_translation_model_and_tokenizer(src, dst)
inputs = tokenizer.encode(text, return_tensors="pt", max_length=512, truncation=True)

"""# generate the translation output using greedy search
greedy_outputs = model.generate(inputs)
# decode the output and ignore special tokens
print(tokenizer.decode(greedy_outputs[0], skip_special_tokens=True))"""


# generate the translation output using beam search
beam_outputs = model.generate(inputs, num_beams=3)
# decode the output and ignore special tokens
print(tokenizer.decode(beam_outputs[0], skip_special_tokens=True))


# beam search or greedy search ?? beam returns more accurate results but may be slower
# need to compare