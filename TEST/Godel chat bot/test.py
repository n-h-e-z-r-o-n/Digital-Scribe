# pip install transformers

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/GODEL-v1_1-base-seq2seq")
model = AutoModelForSeq2SeqLM.from_pretrained("microsoft/GODEL-v1_1-base-seq2seq")


def predict(input, history=[]):
    instruction = 'Instruction: given a dialog context, you need to respond as therapist'

    knowledge = '  '
    # knowledge  = "[KNOWLEDGE]" +

    s = list(sum(history, ()))

    s.append(input)

    #print(s)

    dialog = ' EOS '.join(s)

    # print(dialog)

    query = f"{instruction} [CONTEXT] {dialog} {knowledge}"

    top_p = 0.9
    min_length = 8
    max_length = 64

    # tokenize the new input sentence
    new_user_input_ids = tokenizer.encode(f"{query}", return_tensors='pt')

    output = model.generate(new_user_input_ids, min_length=int(min_length), max_length=int(max_length), top_p=top_p, do_sample=True).tolist()

    response = tokenizer.decode(output[0], skip_special_tokens=True)

    history.append((input, response))

    return response, history



print("Chatbot: Hello! I'm your chatbot therapist. Type 'exit' to end the RAG_page.")
history = []

while True:
    user_input = input("You: ")

    if user_input.lower() == 'exit':
        print("Chatbot: Goodbye!")
        break

    response, history = predict(user_input, history)
    print("Chatbot:", response)
print(history)
"""
import gradio as gr
gr.Interface(fn=predict,
             inputs=["text",'state'],
             outputs=["chatbot", 'state']).launch(debug = True, share = True)
"""
