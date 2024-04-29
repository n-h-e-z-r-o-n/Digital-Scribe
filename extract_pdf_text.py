import pdfplumber  # used for extracting data from pdf
path = ("./new file name.pdf")
with pdfplumber.open(path) as pdf:
    text = ''
    for page in pdf.pages:
        text += page.extract_text()
print("-", text)
