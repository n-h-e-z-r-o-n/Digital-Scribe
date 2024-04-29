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
    model_kwargs=dict(max_generated_token_count=510),
)




#template = """### Instruction: {Instruction} \n\n### Response:"""

template = """You are a AI that analyzes data exacted from images and present it in a formatted way. 
Human: {Instruction}
Chatbot:"""

prompt = PromptTemplate(template=template, input_variables=["Instruction"])



llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)

#Question = "What diseases are prevelant in dairy small ruminant, and what managment practice can mitigate their impact "

#Answer = llm_chain.invoke(input=f"{Question}")
#print(Answer['text'])

while True:
    Question = """extracted data from an image: "NORTH COUNTRY HealthCare NOH creating healthier communities LaieMo Hurt REVIEWOFSYMPTOMS: Circle if present, X-out if absent blank if not asked Constitutional: fever chills sweats weakness fatigue weight weight Eyes:diplopia blurry vision eye pain ENT: sore throat coryza vision postnasal drip ear pain hearing loss Cardiac: chest pain/pressure palpitations orthopnea DOE PND Exercise tolerance pedal edema Respiratory: short of breath cough wheezing GI: nausea vomiting fatty-food intolerance reflux heart burn dysphagia melena diarrhea constipation bowel or bladder abd pain GU: frequency urgency dysuria hesitancy nocturia dribblingED hematuria irregular menses discharge heavy menses menopausal symptoms Musculoskeletal: myalgias joint pain focal weakness back pain Skin: bruising rashes atypical /changing moles hives hair loss Neuro:syncope seizures numbness/tingling/weakness falling headache vertigo light-headed Psych: in sleep appetite energy concentration mood ideation anxiety depression Endocrine:hot/cold intolerance skin/hair changes polyuria polydipsia polyphagia Hematologic/Lymphatic:swollen glands night sweats easy bruising Rheum: joint pain myalgiasjoint swellingRaynauds Family History:CAD DMSudden Death HTNCholesterol Thyroid Asthma Breast/Ovarian CA other: Social History: married single partner divorced widowed children: separated retired occupation exercise? living will? Surgeries: choly TAH BSO appy tonsils hernia Additional Notes: Signature: Date: -revised 7/08"
    Dont explain the data, just analyze the extracted data and present it in a formatted way. 
"""

    Answer = llm_chain.invoke(input=f"{str(Question)}")
    print(Answer['text'])
    break