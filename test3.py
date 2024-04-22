from fpdf import FPDF
from PyPDF2 import PdfFileMerger

def create_pdf(input_file):
    # Create a new FPDF object
    pdf = FPDF()

    # Open the text file and read its contents
    with open(input_file, 'r') as f:
        text = f.read()

    # Add a new page to the PDF
    pdf.add_page()

    # Set the font and font size
    pdf.set_font('Arial', size=12)

    # Write the text to the PDF
    pdf.write(5, text)

    # Save the PDF
    pdf.output('output.pdf')

    # If a template PDF is specified, merge it with the new PDF
    merger = PdfFileMerger()
    template_pdf = 'template.pdf'
    if template_pdf:
        merger.append(PdfFileReader(open(template_pdf, 'rb')))
        merger.append(PdfFileReader(open('output.pdf', 'rb')))
        merger.write('merged_output.pdf')

create_pdf("C:\Users\HEZRON WEKESA\Desktop\New Text Document.txt")