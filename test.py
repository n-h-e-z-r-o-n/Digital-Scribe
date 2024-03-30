# pip install -U langchain
# pip install gradientai


from langchain.chains import LLMChain
from langchain_community.llms import GradientLLM
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os
from gradientai import Gradient

os.environ['GRADIENT_ACCESS_TOKEN'] = "MU96F09nGNZC8R1B3d4XfbKqgyKrfqIs"
os.environ['GRADIENT_WORKSPACE_ID'] = "1b99bbdd-1360-4321-a152-fc8822334cd0_workspace" #"1b99bbdd-1360-4321-a152-fc8822334cd0_workspace"

fine_tuned_Model_Id = "d189f721-ae17-4545-a0ad-f95194e857f5_model_adapter"  #  initializes a GradientLLM with our fine-tuned model by specifying our model ID.

gradient = Gradient()

base_model = gradient.get_base_model(base_model_slug="nous-hermes2")
print(base_model.id)

llm = GradientLLM(
    model=base_model.id,
    model_kwargs=dict(max_generated_token_count=510),
)

template = """Given the conversation between two or more people. formats the conversation with correct grammar and flo.
conversation: {conversation}
Chatbot:"""

prompt = PromptTemplate(template=template, input_variables=["conversation"])

llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)

while True:
    Question = input()
    Answer = llm_chain.invoke(input=f"{Question}")
    print(Answer['text'])