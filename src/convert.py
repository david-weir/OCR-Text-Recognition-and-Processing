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

    return file_name

def download_split_mp3(lang, file, directory):
    path = directory + '/' + file
    with open(path) as f:
        text = f.read()

    recording = gTTS(text=text, lang=lang, slow=False)
    file_name = file.replace(".txt", "")
    recording.save("{}/{}.mp3".format(directory, file_name))

    return "{}/{}.mp3".format(directory, file_name)

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
    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, 75)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename, 'F')


def split_txtfile(txtfile):
    with open(txtfile, 'r') as f:
        words = f.read()
        words_lst = words.split()
        files = []
        chunk = 100
        for c, i in enumerate(range(0, len(words_lst), chunk)):
                with open("mp3_segments/part_{}.txt".format(c+1), "w") as out:
                    out.write(" ".join(words_lst[i:i+chunk]))
                    files.append("part_{}.txt".format(c+1))

        return files