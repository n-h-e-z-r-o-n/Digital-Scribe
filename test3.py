
f = open(r"C:\Users\HEZRON WEKESA\Desktop\New Text Document.txt", "r")

# insert the texts in pdf
print(f)
text = ''
for x in f:
    text += x.strip()

#print(text)

from reportlab.pdfgen import canvas

file_name = "example.pdf"

# Create a PDF document
pdf_canvas = canvas.Canvas(file_name)

# Set font and size
pdf_canvas.setFont("Courier", 12)

# Define the position of the text in the PDF
pdf_canvas.drawString(100, 750, text)

# Save the PDF
pdf_canvas.save()