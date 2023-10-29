# pip install -q git+https://github.com/huggingface/transformers.git
# pip install transformers
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)


def generate_text(input):
    input_ids = tokenizer.encode(input, return_tensors='tf')
    beam_output = model.generate(input_ids, max_length=100, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)
    output = tokenizer.decode(beam_output[0], skip_special=True, clean_up_tokenization_spaces=True)
    return '.'.join(output.split(".")[:-1]) + "."


m = generate_text(" What is Networking")
print(m)
