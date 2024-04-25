# pip install -U langchain
# pip install gradientai


from langchain.chains import LLMChain
from langchain_community.llms import GradientLLM
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os
from gradientai import Gradient

os.environ['GRADIENT_ACCESS_TOKEN'] = "IuQrYCURHsRzzk1BgSDy3xn3V97walUO"
os.environ['GRADIENT_WORKSPACE_ID'] = "d87be754-5abb-4085-97f9-556d00e71fbd_workspace" #"1b99bbdd-1360-4321-a152-fc8822334cd0_workspace"

fine_tuned_Model_Id = "d189f721-ae17-4545-a0ad-f95194e857f5_model_adapter"  #  initializes a GradientLLM with our fine-tuned model by specifying our model ID.

gradient =  Gradient()

base_model = gradient.get_base_model(base_model_slug="nous-hermes2")
print(base_model.id)


llm = GradientLLM(
    model=base_model.id,
    model_kwargs=dict(max_generated_token_count=128),
)




#template = """### Instruction: {Instruction} \n\n### Response:"""

template = """You are a AI having a conversation with a human.
{chat_history}
Human: {Instruction}
Chatbot:"""

prompt = PromptTemplate(template=template, input_variables=["Instruction", 'chat_history'])

memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True,   memory=memory )

#Question = "What diseases are prevelant in dairy small ruminant, and what managment practice can mitigate their impact "

#Answer = llm_chain.invoke(input=f"{Question}")
#print(Answer['text'])

while True:
    Question = """could you structure  and make grammatical correction on the below text extracted from an image:


our enty into the
 creation inplimentation
 and felsvising
 speciangation Sports
 events has gwen our best
 t oppertunity for
 doing this for showing The systems
 feel it.Theseevents often inolved a
 coordirated effort among five or six of
 owr comypanies.Each events vaniesfrom
 the next,and Thowgh we have yet to
 create q structre to define what They
 are who's doing them or how They are
 supposed to worh
 J.sewa
 Kuma
 IRE
 2 6
 St.JOeph>MATSEL
 ASchoul

"""

    Answer = llm_chain.invoke(input=f"{str(Question)}")
    print(Answer['text'])
    break