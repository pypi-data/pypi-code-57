from reportlab.lib.pagesizes import legal
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Image

def create_pdf(pdf_filename, images_filenames):
    reversed_legal = (14*inch,8.5*inch)

    c = canvas.Canvas(pdf_filename, pagesize=reversed_legal)
    for src in images_filenames:
        img = Image(src, width=14*inch, height=8.5*inch)
        img.hAlign = 'CENTER'
        img.wrapOn(c, *reversed_legal)
        img.drawOn(c,0,0)
        c.showPage()
    c.save()