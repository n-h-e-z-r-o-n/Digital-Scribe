key = "AIzaSyAnTOy2dwsq1WB7Df90-M4fU8P29zsxVP0"



import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


genai.configure(api_key=key)


for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

model = genai.GenerativeModel(
    model_name =  'gemini-1.5-flash',
    system_instruction="""
    my report section = [
    APPENDIX
APPENDIX .1 Speech Recognition Engine Evaluation
The following table presents the evaluation results of the speech recognition engine used in the Digital Scribe system, tested on a diverse set of audio samples with varying accents, background noise levels, and medical terminology.
Evaluation Metric	Result
Word Error Rate (WER) on clean audio	5.2%
WER on audio with background noise	8.7%
WER on audio with accented speech	7.4%
WER on medical domain-specific audio	6.9%

APPENDIX .2 Natural Language Processing (NLP) Module Performance
The NLP module's performance in identifying and extracting relevant medical entities is summarized in the following table:
Entity Type	Precision	Recall	F1-Score
Diagnoses	0.92	0.88	0.90
Procedures	0.89	0.91	0.90
Medications	0.94	0.87	0.90
Allergies	0.91	0.93	0.92
Clinical Findings	0.88	0.86	0.87

APPENDIX .3 System Performance Benchmarks
The following table presents the performance benchmarks of the Digital Scribe system under various workloads and stress conditions:
Concurrent Users	Average Response Time (ms)	CPU Utilization	Memory Usage (GB)
10	247	28%	2.1
50	312	41%	3.5
100	387	57%	5.2
200	472	71%	7.8

APPENDIX .4 User Acceptance Testing Results
User acceptance testing was conducted with a diverse group of healthcare professionals, including physicians, nurses, and medical scribes. The following table summarizes the results:
Evaluation Metric	Average Rating (1-5 scale)
Ease of use	4.2
Integration with clinical workflows	4.1
Accuracy of generated clinical notes	4.3
Overall satisfaction	4.4

APPENDIX .6 Test Schedule and Milestones
The testing schedule and milestones are outlined as follows:
Activity	Start Date	End Date
Test Planning	2024-05-01	2024-05-07
Test Case Development	2024-05-08	2024-05-14
Test Execution	2024-05-15	2024-05-28
Test Evaluation	2024-05-29	2024-06-05

]

    """
                              )


messages = []


while True:
    user_query = input(": ")

    messages.append({'role':'user',
                     'parts':[user_query]})
    response = model.generate_content(messages)

    print(response.text)

    messages.append({'role':'model',
                     'parts':[response.text]})