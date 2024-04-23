import pdfplumber

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Example usage
pdf_path = 'example.pdf'  # Replace with the path to your PDF file
text = extract_text_from_pdf(pdf_path)
print(text)