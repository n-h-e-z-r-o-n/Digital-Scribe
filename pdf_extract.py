from gradientai import Gradient
import gradientai
import os

os.environ['GRADIENT_ACCESS_TOKEN'] = "MU96F09nGNZC8R1B3d4XfbKqgyKrfqIs"
os.environ['GRADIENT_WORKSPACE_ID'] = "1b99bbdd-1360-4321-a152-fc8822334cd0_workspace"


gradient = Gradient()



filepath = r"C:\Users\HEZRON WEKESA\Downloads\CSC418 - Group 3 - LLM.docx.pdf"



result = gradient.extract_pdf(
    filepath=filepath
)

print(result)


print(result)