import fitz

def extract_resume_text(pdf_path):
    document = fitz.open(pdf_path)

    resume_text = ""

    for page in document:
        resume_text += page.get_text()

    document.close()

    return resume_text