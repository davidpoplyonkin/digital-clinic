from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph)
from io import BytesIO

def generate_pdf(obj):
    buffer = BytesIO()

    # Create a new PDF document
    pdf_doc = SimpleDocTemplate(buffer, pagesize=A4)

    Story = [Paragraph(str(obj))]
    pdf_doc.build(Story)
    pdf_value = buffer.getvalue()
    buffer.close()
    return pdf_value