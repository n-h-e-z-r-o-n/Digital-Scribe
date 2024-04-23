from fpdf import FPDF

# save FPDF() class into
# a variable pdf
pdf = FPDF()

# Add a page
pdf.add_page()

# set style and size of font
# that you want in the pdf
pdf.set_font("Arial", size=15)

# open the text file in read mode
f = open(r"C:\Users\HEZRON WEKESA\Desktop\New Text Document.txt", "r")

# insert the texts in pdf
for x in f:
    pdf.cell(20, 4, txt=x, ln=1, align='l')

# save the pdf with name .pdf
pdf.output("mygfg.pdf")