from gtts import gTTS
import os
from fpdf import FPDF
import textwrap

def convert_to_mp3(lang, file):
    with open(file) as f:
        text = f.read()

    recording = gTTS(text=text, lang=lang, slow=False)
    recording.save("speech.mp3")

    os.system("mpg321 speech.mp3")


def covert_to_pdf(file):
    pdf = FPDF()  
    
    # Add a page
    pdf.add_page()
    
    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size = 11)
    
    # open the text file in read mode
    f = open(file, "r")
    
    # insert the texts in pdf
    for x in f:
        pdf.cell(w=200, h=10, txt = x, ln = 1, align = 'L')
    
    # save the pdf with name .pdf
    pdf.output("mygfg.pdf") 

# convert_to_mp3("en", "text.txt")
covert_to_pdf("text.txt")
# https://stackoverflow.com/questions/10112244/convert-plain-text-to-pdf-in-python
def convert_to_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename, 'F')

input_filename = 'text.txt'
output_filename = 'output.pdf'
file = open(input_filename)
text = file.read()
file.close()
convert_to_pdf(text, output_filename)