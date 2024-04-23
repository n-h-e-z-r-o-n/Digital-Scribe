
f = open(r"C:\Users\HEZRON WEKESA\Desktop\New Text Document.txt", "r")

# insert the texts in pdf
text = ''
for x in f:
    text += x
     x)
    print(,
from reportlab.pdfgen import canvas

# Example of a sentence
input_text = "This is an example of a simple sentence."

# Output PDF file
file_name = "example.pdf"

# Create a PDF document
pdf_canvas = canvas.Canvas(file_name)

# Set font and size
pdf_canvas.setFont("Courier", 12)

# Define the position of the text in the PDF
pdf_canvas.drawString(100, 750, input_text)

# Save the PDF
pdf_canvas.save()