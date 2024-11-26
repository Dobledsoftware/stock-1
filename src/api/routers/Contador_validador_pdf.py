import os
import fitz  # PyMuPDF
import logging
import json


# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Definición de los valores válidos para la validación
VALIDATE = {'header1': 'Recibo de Haberes', 'header2': 'HOSP. NAC. PROF.  ALEJANDRO POSADAS', 'header3': '30-63597680-9'}



def validate_pdf(ifn):
    """Validar si el PDF contiene los headers esperados."""
    doc = fitz.open(ifn)
    page_count = doc.page_count
    if page_count >= 1:
        page = doc.load_page(0)  # Cargar la primera página
        data = extract_text_from_area_encabezado(page)
        valid = data == VALIDATE
        logger.debug(f"Validación: {valid}, datos extraídos: {data}")
        return valid
    return False

#           CONTADOR


#verifica que el encabezado sea siempre igual
def extract_text_from_area_encabezado(page):
    """Extraer texto de áreas específicas del PDF."""
    rect_header1 = fitz.Rect(150, 1, 270, 30)
    rect_header2 = fitz.Rect(100, 50, 330, 60)
    rect_header3 = fitz.Rect(130, 70, 190, 90)

    header1 = page.get_text("text", clip=rect_header1).replace('\n', '').replace('-', '').lstrip()
    header2 = page.get_text("text", clip=rect_header2).replace('\n', '').replace('/', '').lstrip()
    header3 = page.get_text("text", clip=rect_header3).replace('\n', '').replace('/', '').lstrip()
    
    return {
        'header1': header1,
        'header2': header2,
        'header3': header3
    }

def extract_text_from_area(page):
    rect_cuil = fitz.Rect(250, 100, 350, 115)
    rect_periodo = fitz.Rect(40, 160, 100, 170)

    cuil = page.get_text("text", clip=rect_cuil).replace('\n', '').replace('-', '')
    periodo = page.get_text("text", clip=rect_periodo).replace('\n', '').replace('/', '')
    return {'cuil': cuil, 'periodo': periodo}

def count_recibos_in_pdf(ifn):
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
    return json.dumps(res)

# Si el script se ejecuta directamente, ejecutar main
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: script.py <archivo_pdf>")
        sys.exit(1)

    input_file = sys.argv[1]
    print(count_recibos_in_pdf(input_file))
    sys.exit(0)

def process_pdf(input_file_path, output_dir):
    """Función para procesar el PDF. Actualmente solo devuelve un mensaje de éxito."""
    # Lógica de procesamiento (por ahora, solo devuelve un mensaje)
    return "ESTA TODO BIEN"

def save_uploaded_file(file):
    """Guardar el archivo subido en el directorio deseado."""
    upload_directory = os.path.join(os.getcwd(),'pdf', 'sabana')
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)
    
    file_path = os.path.join(upload_directory, file.filename)
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    logger.debug(f"Archivo guardado en: {file_path}")
    return file_path

# Aquí puedes agregar las funciones de firma y verificación
def sign_pdf(input_file_path, output_file_path, private_key_path):
    # Lógica para firmar el PDF
    logger.debug(f"Firmando PDF: {input_file_path}")
    return output_file_path  # Retorna el path del PDF firmado

def verify_pdf_signature(signed_pdf_path, public_key_path):
    # Lógica para verificar la firma del PDF
    logger.debug(f"Verificando firma del PDF: {signed_pdf_path}")
    return True  # Retorna True si la firma es válida




