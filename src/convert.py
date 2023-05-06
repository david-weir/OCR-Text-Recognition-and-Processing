from gtts import gTTS
import os
from fpdf import FPDF
import textwrap

# function to convert a text file into an mp3
def download_mp3(lang, file):
    with open(file) as f:
        text = f.read()
    
    # uses gTTS -> Google's text to speech
    recording = gTTS(text=text, lang=lang, slow=False)
    file_name = os.path.basename(file).replace(".txt", ".mp3")
    file_path = os.path.dirname(file) # new file path is constructed

    new_file = os.path.join(file_path, file_name)
    recording.save(new_file) # the mp3 is downloaded

    return new_file

# based on code at https://stackoverflow.com/questions/10112244/convert-plain-text-to-pdf-in-python
def convert_to_pdf(text, filename):
    with open(text, 'r') as input_file:
        input_file = input_file.read()

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(True, margin=20)
        pdf.set_margins(20, 20, 20) # create margins around the page of the pdf
        pdf.add_page()
        pdf.add_font('DejaVu', '', '../fonts/DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12) # add a font that can handle unicode characters
        paragraphs = input_file.split('\n')

        for paragraph in paragraphs:
            lines = textwrap.wrap(paragraph, width=75) # wrap text to prevent run off

            if len(lines) == 0:
                pdf.ln() # add new line

            for wrap in lines:
                pdf.cell(w=0, h=6, txt=wrap, ln=1) # copy each line into a line in the PDF

        pdf.output(filename + '.pdf', 'F') # append pdf file extension and download