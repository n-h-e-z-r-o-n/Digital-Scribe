
f = open(r"C:\Users\HEZRON WEKESA\Desktop\New Text Document.txt", "r")

# insert the texts in pdf
print(f)
text = ''
for x in f:
    text += x

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph



# Output PDF file
file_name = "example.pdf"

# Create a PDF document
pdf_document = SimpleDocTemplate(file_name)
pdf_elements = []

# Create a stylesheet for styling
styles = getSampleStyleSheet()

# Parse the HTML-like text into a Paragraph
paragraph = Paragraph(text, styles["Normal"])

# Add the Paragraph to the PDF elements
pdf_elements.append(paragraph)

# Build the PDF document
pdf_document.build(pdf_elements)
