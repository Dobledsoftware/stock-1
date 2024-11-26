import fitz  # PyMuPDF
import sys
import json

def extract_text_from_area(page):
    rect_cuil = fitz.Rect(250, 100, 350, 115)
    rect_periodo = fitz.Rect(40, 160, 100, 170)

    cuil = page.get_text("text", clip=rect_cuil).replace('\n', '').replace('-', '')
    periodo = page.get_text("text", clip=rect_periodo).replace('\n', '').replace('/', '')
    return {'cuil': cuil, 'periodo': periodo}


def main(ifn):

    # Abrir el PDF con PyMuPDF
    doc = fitz.open(ifn)
    count = 0
    cuil = None
    periodo = None
    for page in doc.pages():
        data = extract_text_from_area(page)

        if cuil != data.get('cuil', False):
            count += 1
        
        if not periodo:
            periodo = data.get('periodo', False)
    
    res = {'count': count, 'periodo': periodo}

   
    print(json.dumps(res))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: script.py <archivo_pdf>")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)
    sys.exit(0)
