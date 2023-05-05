from gtts import gTTS
import os
from fpdf import FPDF
import textwrap

def download_mp3(lang, file):
    with open(file) as f:
        text = f.read()
    
    recording = gTTS(text=text, lang=lang, slow=False)
    file_name = os.path.basename(file).replace(".txt", ".mp3")
    file_path = os.path.dirname(file)

    new_file = os.path.join(file_path, file_name)
    recording.save(new_file)

    return new_file

# https://stackoverflow.com/questions/10112244/convert-plain-text-to-pdf-in-python
def convert_to_pdf(text, filename):
    with open(text, 'r') as input_file:
        input_file = input_file.read()
        pt_to_mm = 0.5
        fontsize_pt = 12
        fontsize_mm = fontsize_pt * pt_to_mm
        margin_bottom_mm = 20

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(True, margin=margin_bottom_mm)
        pdf.set_margins(20, 20, 20)
        pdf.add_page()
        pdf.add_font('DejaVu', '', '../fonts/DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)
        splitted = input_file.split('\n')

        for line in splitted:
            lines = textwrap.wrap(line, 75)

            if len(lines) == 0:
                pdf.ln()

            for wrap in lines:
                pdf.cell(0, fontsize_mm, wrap, ln=1)

        pdf.output(filename, 'F')