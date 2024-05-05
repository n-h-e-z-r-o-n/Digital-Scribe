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
 Hi, Mr. Jones. How are you? I'm good, Dr. Smith, I have to see you. Thanks for seeing you again. What brings you back? Well, my back's been hurting again. I see. I've seen you a number of times for the havenine. You were ever since I got hurt on the job three years ago, and something that just keeps coming back. You'll be fine for a while, and then I'll end out, or I'll move with a weird way, and then, boom, it'll just go out again. Unfortunately, that can happen, and I do have quite a few patients who get reoccurring episodes of back pain. Have you been keeping up with a therapy that we had you on before? Which of the pills? Actually, I was talking about the physical therapy that we had you doing. The pills are only meant for short-term, because they don't actually prevent the back pain from coming back. So, yeah, once my back started feeling better, I was happy not to go to the therapist anymore. Why was that? Well, it started to become kind of a hassle with my work schedule, and the cost was an issue, but I was able to get back to work, so, and I could use the money. Do you think the physical therapy was helping? Yeah, but we're slow-gulling at first. I see physical therapy is a bit slower than medications, but the point is to build up the core muscles in your back and your abdomen. Physical therapy is also less invasive than medications, so that's why we had you doing the therapy. But you mentioned that cost was getting to be a real issue for you. Can you tell me more about that? Well, the insurers I had only covered certain number of sessions, and then they moved my therapy office, because they were trying to work out my schedule work, but that was really far away, and then I had to do with parking, and it just started to get really expensive. Got it, I understand. So, for now I'd like you to try using a heating pad for your back pain, so that should help in the short term. Our goal is to get your back pain under better control without creating additional problems for you like cost. Let's talk about some different options, and the pros and cons of each. So the physical therapy is actually really good for your back pain, but there are other things we can be doing to help. Yes, I definitely don't need to lose any more time to work and just lie around the household day. Okay, was there some alternative therapies like yoga, or Tai Chi classes, or meditation therapies that might be able to help? And they might also be closer to you, and be less expensive with that something you'd be interested in. Sure, that'd be great. Good. Let's talk about some of the other costs of your care. In the past we had you on some tram at all, because the physical therapy alone wasn't working. Yeah, that medicine was working really well, but again, the cost of it got really expensive. Yeah, yeah. So that is something in the future we could order something like a generic medication, and then there are also resources for people to look up the cheapest costs of their medications. But for now, I'd like to stick with the non-prescription medications. And if we can have you go to yoga, or Tai Chi classes like I mentioned, that could alleviate the need for ordering prescriptions. Okay, that sounds great. Great. Are there any other costs that are a problem for you and your care? Well, my insurance isn't going down, but that seems to be the case for everybody that I talk to, but I should be able to make it work, yeah. Unfortunately, that is an issue for a lot of people, but I would encourage you during open season to look at your different insurance options to see which plan is more cost-effective for you. Okay. Yes, that sounds great. Great. Well, I appreciate you talking to me today. Yeah, I'm glad you're able to come in. What I'll do is I'll have my office team research the different things that you and I talked about today. And then looks at a time early next week, say Tuesday, where we can talk over the phone about what we were able to come up with for you and see if those would work.
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
content in the documents. if you dont know the answer say you don't know.
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
    Query = "What are the main symptoms or concerns mentioned by the patient in the conversation?"
    print(LLM_Run(query))