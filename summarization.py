from gradientai import SummarizeParamsLength
from gradientai import ExtractParamsSchemaValueType, Gradient
import os

# # Set the environment variables for gradient.ai
os.environ['GRADIENT_ACCESS_TOKEN'] = "Fz8v1bayVU3mQ11BoCLgtvquK8OHTL68"
os.environ['GRADIENT_WORKSPACE_ID'] = "345ce93a-40e9-4940-aa2e-fa76f1668fcd_workspace"

mygradient = Gradient()

document = (
""" Good morning, Doctor. I hope you're doing well today.

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

 You're welcome. It's my job to ensure your health and well-being. Let's work together to get to the bottom of these headaches and find the best course of action moving forward."""
)


result_from_examples = mygradient.summarize(
    document=document,
    # examples=examples,
)

length = SummarizeParamsLength.MEDIUM
result_from_length = mygradient.summarize(document=document, length=length)

print(result_from_examples['summary'])