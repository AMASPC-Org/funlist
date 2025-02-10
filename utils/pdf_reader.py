
import PyPDF2
import os

def read_brand_guide():
    try:
        pdf_path = os.path.join('attached_assets', 'AMA_LogoStyleGuide - Copy.pdf')
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_content = ''
            for page in pdf_reader.pages:
                text_content += page.extract_text()
            return text_content
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
