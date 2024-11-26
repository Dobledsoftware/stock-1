import fitz  # PyMuPDF
import mariadb
import sys
import os
from datetime import datetime
import logging
from routers.conexion import Conexion


logging.basicConfig(level=logging.DEBUG, filename='../public/pdf/app.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.debug('Entro')
def extract_text_from_area(page):
    rect_nombre = fitz.Rect(100, 100, 260, 115)
    rect_cuil = fitz.Rect(260, 100, 350, 115)
    rect_periodo = fitz.Rect(40, 160, 100, 170)
    rect_desc = fitz.Rect(120, 160, 310, 170)

    nombre = page.get_text("text", clip=rect_nombre).replace('\n', '')
    cuil = page.get_text("text", clip=rect_cuil).replace('\n', '').replace('-', '')
    periodo = page.get_text("text", clip=rect_periodo).replace('\n', '').replace('/', '')
    desc = page.get_text("text", clip=rect_desc).replace('\n', '')
    return {'name': nombre, 'cuil': cuil, 'periodo': periodo, 'description': desc}

def main_parcer(ifn, ofn):
    

 # Crear una instancia de la clase Conexion
    conn = Conexion()

    # Llamar al método conectar() para obtener la conexión
    cnx = conn.conectar()

        

    # Abrir el PDF con PyMuPDF
    doc = fitz.open(ifn)
    page_count = doc.page_count
    fecha_subida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    from_page = 0
    pdf_name_older = None

    try:
        for i in range(page_count):
            cursor = cnx.cursor()
            page = doc.load_page(i)
            data = extract_text_from_area(page)
            pdf_name = '_'.join([data[k].replace(',', '').replace('/', '').replace(' ', '') for k in data.keys()])
            if not data.get('periodo', False):
                return {"error": "El periodo no fue encontrado en los datos"}, 400

            if not os.path.exists(ofn + "/" + data.get('periodo')):
                _ofn = ofn + "/" + data.get('periodo')
                os.makedirs(_ofn)

            pdf_name = u"/" + data.get('periodo') + '/' + pdf_name + '.pdf'
            pdf_route = "{}/{}.pdf".format("/" + data.get('periodo'), pdf_name.replace(' ', '_'))

            if pdf_name != pdf_name_older:
                if pdf_name_older:
                    # Guardar el PDF anterior
                    new_doc.save("{}{}".format(ofn, pdf_name_older))
                    new_doc.close()

                pdf_name_older = pdf_name
                new_doc = fitz.open()
                from_page = i

            new_doc.insert_pdf(doc, from_page=from_page, to_page=i)
            from_page = i + 1

            query = ("SELECT id_usuario FROM usuarios WHERE cuil = %s;")
            cursor.execute(query, (data['cuil'],))
            id_usuario_list = cursor.fetchone()

            # Obtener el periodo
            query = ("SELECT id_periodo FROM recibos_periodos WHERE periodo = %s;")
            cursor.execute(query, (data['periodo'],))
            id_periodo = cursor.fetchone()

            # Si no existe el periodo, lo creamos
            if not id_periodo:
                query = (
                    "INSERT INTO recibos_periodos (periodo) "
                    "VALUES (%s);"
                )
                cursor.execute(query, (data['periodo'],))
                cnx.commit()
                query = ("SELECT id_periodo FROM recibos_periodos WHERE periodo = %s;")
                cursor.execute(query, (data['periodo'],))
                id_periodo = cursor.fetchone()

            id_periodo = id_periodo[0]

            query = ("SELECT id_recibo, id_periodo, descripcion_archivo FROM recibos "
                     "WHERE id_periodo = %s AND descripcion_archivo = %s AND cuil = %s;")
            cursor.execute(query, (id_periodo, data['description'], data['cuil']))
            recibo_update = cursor.fetchone()

            if recibo_update:
                query_recibo = (
                    "UPDATE recibos SET fecha_subida = %s, descripcion_archivo = %s, archivo = %s "
                    "WHERE id_recibo = %s;"
                )
                cursor.execute(query_recibo, (fecha_subida, data['description'], pdf_name, recibo_update[0]))
            else:
                if id_usuario_list:
                    id_usuario = id_usuario_list[0]
                    query_recibo = (
                        "INSERT INTO recibos (id_usuario, id_periodo, fecha_subida, descripcion_archivo, archivo, cuil) "
                        "VALUES (%s, %s, %s, %s, %s, %s);"
                    )
                    cursor.execute(query_recibo, (id_usuario, id_periodo, fecha_subida, data['description'], pdf_name, data['cuil']))
                else:
                    query_recibo = (
                        "INSERT INTO recibos (id_periodo, fecha_subida, descripcion_archivo, archivo, cuil) "
                        "VALUES (%s, %s, %s, %s, %s);"
                    )
                    cursor.execute(query_recibo, (id_periodo, fecha_subida, data['description'], pdf_name, data['cuil']))

            cursor.close()

        # Guardar el último PDF
        if new_doc.page_count > 0:
            new_doc.save("{}{}".format(ofn, pdf_name_older))
            new_doc.close()

        cnx.commit()

    except Exception as e:
        cnx.rollback()
        return {"error": f"Error procesando el PDF: {e}"}, 500

    finally:
        cnx.close()

    return {"message": "Procesado con éxito"}, 200
