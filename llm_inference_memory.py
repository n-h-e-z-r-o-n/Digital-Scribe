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
    Question = """ Extract Clinical infomation form bellow text


No Mut Herts Hurts Hons
Latle Be Lite More Even More Whole Lot

VA NORTH COUNTRY
HealthCare

5
Huet
Wort

REVIEW OF SYMPTOMS: (Circle if present, X-outif absent, blank if not asked

Constitutional: fever chills sweats weakness fatigue weight fT _ weight |
Eyes: diplopia blurry vision eye pain
ENT: sore throat coryza vision A _postnasal drip ear pain __ hearing loss
Cardiac: chest pain / pressure palpitations orthopnea DOE PND A Exercise tolerance pedal edema
Respiratory: short of breath cough wheezing
GI: nausea vomiting fatty-food intolerance reflux heart burn_dysphagia_melena
diarrhea constipation A bowel or bladder _abd pain
GU: frequency urgency dysuria hesitancy nocturia dribbling ED hematuria
irregular menses heavy menses discharge _ menopausal symptoms
Musculoskeletal: myalgias joint pain focal weakness _ back pain
Skin: bruising rashes atypical / changing moles _ hives _ hair loss
Neuro: syncope scizures numbness / tingling / weakness falling headache vertigo light-headed
Psych: Ainsleep appetite energy concentration mood _ ideation
anxicty depression
Endocrine: hot / cold intolerance _skin/hair changes polyuria _polydipsia__polyphagia
Hematologic / Lymphatic: swollen glands night sweats _casy bruising
Rheum: joint pain myalgias joint swelling Raynauds

Family History: CAD DM _ Sudden Death HTN Cholesterol Thyroid Asthma Breast / Ovarian CA _ other:

Social History: married single partner separated divorced _ widowed children:
retired occupation exercise? living will?

Surgeries: choly TAH BSO_appy tonsils _ hernia
Additional Notes:

Signature: Date:

- revised 7/08



Process finished with exit code 0

"""

    Answer = llm_chain.invoke(input=f"{str(Question)}")
    print(Answer['text'])
    break