# !pip install gradient_haystack==0.2.0
from gradient_haystack.embedders.gradient_document_embedder import GradientDocumentEmbedder
from gradient_haystack.embedders.gradient_text_embedder import GradientTextEmbedder
from gradient_haystack.generator.base import GradientGenerator
from haystack import Document, Pipeline
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack.components.builders.answer_builder import AnswerBuilder
import os

os.environ['GRADIENT_ACCESS_TOKEN'] = "MU96F09nGNZC8R1B3d4XfbKqgyKrfqIs"
os.environ['GRADIENT_WORKSPACE_ID'] = "1b99bbdd-1360-4321-a152-fc8822334cd0_workspace"


fine_tuned_Model_Id = "d189f721-ae17-4545-a0ad-f95194e857f5_model_adapter"

document_store = InMemoryDocumentStore()
writer = DocumentWriter(document_store=document_store)


document_embedder = GradientDocumentEmbedder(
    access_token=os.environ["GRADIENT_ACCESS_TOKEN"],
    workspace_id=os.environ["GRADIENT_WORKSPACE_ID"],
)
"""
with open("./DataSet/Raw_Text_Data.txt", encoding="utf-8") as file:
    text_data = file.read()
"""
text_data = """
 Good morning, Doctor. I hope you're doing well today.

 Good morning! Yes, I'm doing well, thank you. How about yourself?

 Not too bad, thank you. I've been having some persistent headaches lately, and I thought it would be best to come in and get them checked out.

 I'm glad you came in. Headaches can be quite concerning. Can you tell me more about when they started and how often you've been experiencing them?

 Sure. They started about two weeks ago, and they seem to come and go throughout the day. Sometimes they're dull and achy, and other times they're more sharp and intense.

 Have you noticed any specific triggers or patterns associated with the headaches?

 Well, I've noticed that they tend to worsen when I'm stressed or when I haven't had enough sleep. But other than that, I haven't been able to identify any specific triggers.

 Okay, that's helpful to know. Have you experienced any other symptoms along with the headaches, such as nausea, dizziness, or changes in vision?

 No, not really. Just the headaches themselves.

 Alright. And have you tried taking any over-the-counter medications for the headaches? If so, did they provide any relief?

 Yes, I've tried taking ibuprofen a few times, but it only seems to provide temporary relief. The headaches always seem to come back.

 I see. Well, based on what you've described, it's possible that these headaches could be tension headaches or migraines. However, I'd like to conduct a thorough examination and possibly some tests to rule out any other underlying causes.

 That sounds like a good idea. I just want to make sure there's nothing serious going on.

 Of course. Let's start by checking your blood pressure and conducting a neurological examination. Depending on the results, we may need to consider further imaging studies or blood tests.

 Sounds good. Thank you, Doctor, for taking the time to listen to me and help figure this out.

 You're welcome. It's my job to ensure your health and well-being. Let's work together to get to the bottom of these headaches and find the best course of action moving forward.
"""
docs = [
    Document(content=text_data)
]

indexing_pipeline = Pipeline()
indexing_pipeline.add_component(instance=document_embedder, name="document_embedder")
indexing_pipeline.add_component(instance=writer, name="writer")
indexing_pipeline.connect("document_embedder", "writer")
indexing_pipeline.run({"document_embedder": {"documents": docs}})

text_embedder = GradientTextEmbedder(
    access_token=os.environ["GRADIENT_ACCESS_TOKEN"],
    workspace_id=os.environ["GRADIENT_WORKSPACE_ID"],
)

generator = GradientGenerator(
    access_token=os.environ["GRADIENT_ACCESS_TOKEN"],
    workspace_id=os.environ["GRADIENT_WORKSPACE_ID"],
    #model_adapter_id=fine_tuned_Model_Id,
    base_model_slug="nous-hermes2",
    max_generated_token_count=350,
)

prompt = """You are helpful assistant ment to answer questions to help in clinical documentation. Answer the query, based on the
content in the unstructured documents. if you dont know the answer say you don't know.
{{documents}}
Query: {{query}}
\nAnswer:
"""

retriever = InMemoryEmbeddingRetriever(document_store=document_store)
prompt_builder = PromptBuilder(template=prompt)

rag_pipeline = Pipeline()
rag_pipeline.add_component(instance=text_embedder, name="text_embedder")
rag_pipeline.add_component(instance=retriever, name="retriever")
rag_pipeline.add_component(instance=prompt_builder, name="prompt_builder")
rag_pipeline.add_component(instance=generator, name="generator")
rag_pipeline.add_component(instance=AnswerBuilder(), name="answer_builder")
rag_pipeline.connect("generator.replies", "answer_builder.replies")
rag_pipeline.connect("retriever", "answer_builder.documents")
rag_pipeline.connect("text_embedder", "retriever")
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "generator")


def LLM_Run(question):
    result = rag_pipeline.run(
        {
            "text_embedder": {"text": question},
            "prompt_builder": {"query": question},
            "answer_builder": {"query": question}
        }
    )
    return result["answer_builder"]["answers"][0].data

while True:
    query = input()
    Query = "I noticed some unusual lumps or swellings on one of my cows. Should I be worried?"
    print(LLM_Run(query))