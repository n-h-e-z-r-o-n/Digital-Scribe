# pip install -U langchain
# pip install gradientai
# pip install -U langchain-community

from langchain.chains import LLMChain
from langchain_community.llms import GradientLLM
from langchain.prompts import PromptTemplate
import gradientai
import os
from gradientai import Gradient

os.environ['GRADIENT_ACCESS_TOKEN'] = "MU96F09nGNZC8R1B3d4XfbKqgyKrfqIs"
os.environ['GRADIENT_WORKSPACE_ID'] = "1b99bbdd-1360-4321-a152-fc8822334cd0_workspace"

fine_tuned_Model_Id = "d189f721-ae17-4545-a0ad-f95194e857f5_model_adapter"  #  initializes a GradientLLM with our fine-tuned model by specifying our model ID.

gradient =  Gradient()

base_model = gradient.get_base_model(base_model_slug="nous-hermes2")
print(base_model.id)

llm = GradientLLM(
    model="99148c6d-c2a0-4fbe-a4a7-e7c05bdb8a09_base_ml_model",
    model_kwargs={
        "max_generated_token_count": 128,
        "temperature": 0.75,
        "top_p": 0.95,
        "top_k": 20,
        "stop": [],
    },
    #model_kwargs=dict(max_generated_token_count=128),
)

template = """### Instruction: {Instruction} \n\n### Response:"""

prompt = PromptTemplate(template=template, input_variables=["Instruction"])

llm_chain = LLMChain(prompt=prompt, llm=llm)

Question = "What diseases are prevelant in dairy small ruminant, and what managment practice can mitigate their impact "

Answer = llm_chain.invoke(input=f"{Question}")
print(Answer['text'])