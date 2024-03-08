# pip install -U langchain
# pip install gradientai
# pip install -U langchain-community

from langchain.chains import LLMChain
from langchain_community.llms import GradientLLM
from langchain.prompts import PromptTemplate
import gradientai
import os


# # Set the environment variables for gradient.ai
os.environ['GRADIENT_ACCESS_TOKEN'] = "Dh8BfdF4J0CO7UBi7nXjZny7jh9breiK"
os.environ['GRADIENT_WORKSPACE_ID'] = "345ce93a-40e9-4940-aa2e-fa76f1668fcd_workspace"

fine_tuned_Model_Id = "d189f721-ae17-4545-a0ad-f95194e857f5_model_adapter"  #  initializes a GradientLLM with our fine-tuned model by specifying our model ID.


llm = GradientLLM(
    model=fine_tuned_Model_Id,
    model_kwargs=dict(max_generated_token_count=128),
)

template = """### Instruction: {Instruction} \n\n### Response:"""

prompt = PromptTemplate(template=template, input_variables=["Instruction"])

llm_chain = LLMChain(prompt=prompt, llm=llm)

Question = "What diseases are prevelant in dairy small ruminant, and what managment practice can mitigate their impact "

#Answer = llm_chain.invoke(input=f"{Question}")
#print(Answer['text'])