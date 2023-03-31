from gtts import gTTS
import os
from fpdf import FPDF
import textwrap
from pygame import mixer
import time

def download_mp3(lang, file):
    with open(file) as f:
        text = f.read()

    recording = gTTS(text=text, lang=lang, slow=False)
    recording.save("test.mp3")

    # os.system("mpg321 speech.mp3")
def play_mp3(lang, file):
    with open(file) as f:
        text = f.read()

    recording = gTTS(text=text, lang=lang, slow=False, tld='ie')
    recording.save("test.mp3")
    
    mixer.init()
    mixer.music.load("test.mp3")
    mixer.music.play(0)
    # time.sleep(2)
    # os.system("mpg321 speech.mp3")


# convert_to_mp3("en", "text.txt")
# https://stackoverflow.com/questions/10112244/convert-plain-text-to-pdf-in-python
def convert_to_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.5
    fontsize_pt = 12
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 20
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.set_margins(20, 20, 20)
    pdf.add_page()
    pdf.set_font(family='Arial', size=fontsize_pt)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, 85)

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