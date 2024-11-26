import fitz  # PyMuPDF
import sys
import random

VALIDATE = {'header1': 'Recibo de Haberes', 'header2': 'HOSP. NAC. PROF.  ALEJANDRO POSADAS', 'header3': '30-63597680-9'}

def extract_text_from_area(page):
    rect_header1 = fitz.Rect(150, 1, 270, 30)
    rect_header2 = fitz.Rect(100, 50, 330, 60)
    rect_header3 = fitz.Rect(130, 70, 190, 90)

    header1 = page.get_text("text", clip=rect_header1).replace('\n', '').replace('-', '').lstrip()
    header2 = page.get_text("text", clip=rect_header2).replace('\n', '').replace('/', '').lstrip()
    header3 = page.get_text("text", clip=rect_header3).replace('\n', '').replace('/', '').lstrip()
    return {'header1': header1, 'header2': header2, 'header3': header3}


def main(ifn):

    # Abrir el PDF con PyMuPDF
    doc = fitz.open(ifn)
    page_count = doc.page_count
    if page_count >= 1:
        page = doc.load_page(random.randrange(page_count-1))
        data = extract_text_from_area(page)
        if data == VALIDATE:
            print('OK')
            sys.exit(0)
    
    else:
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: script.py <archivo_pdf>")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)
    
