from fastapi import FastAPI
import psycopg2
from psycopg2.extras import DictCursor
import random
import string

# Configuración de conexión a la base de datos
DB_CONFIG = {
    "user": "postgres",
    "password": "DarioDavid-bd-UBU-1",
    "host": "92.112.176.191",
    "port": 5432,
    "database": "stock-TEST"
}

app = FastAPI()

def generar_codigo_barras():
    """Genera un código de barras aleatorio de 9 dígitos."""
    return ''.join(random.choices(string.digits, k=9))

def insertar_registros_en_bd():
    """Inserta 50,000 registros en la tabla de productos."""
    try:
        # Conexión a la base de datos
        conexion = psycopg2.connect(**DB_CONFIG)
        cursor = conexion.cursor(cursor_factory=DictCursor)

        # Consulta SQL para insertar productos
        sql = """
        INSERT INTO productos (marca, nombre, descripcion, precio, stock_actual, stock_minimo, stock_maximo, id_proveedor, codigo_barras)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        # Generar e insertar 50,000 registros
        for _ in range(50000):
            marca = "Marca_" + random.choice(string.ascii_uppercase)
            nombre = "Producto_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            descripcion = "Descripcion del producto " + nombre
            precio = round(random.uniform(10, 500), 2)
            stock_actual = random.randint(0, 100)
            stock_minimo = random.randint(0, 10)
            stock_maximo = stock_actual + random.randint(10, 50)
            id_proveedor = random.choice([1, 2, 3])
            codigo_barras = generar_codigo_barras()

            # Ejecutar la consulta
            cursor.execute(sql, (marca, nombre, descripcion, precio, stock_actual, stock_minimo, stock_maximo, id_proveedor, codigo_barras))

        # Confirmar los cambios en la base de datos
        conexion.commit()
        return {"status": "success", "message": "Se han insertado 50,000 registros exitosamente."}

    except Exception as e:
        if conexion:
            conexion.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        # Cerrar la conexión
        if conexion:
            cursor.close()
            conexion.close()

@app.post("/insertar-registros")
async def insertar_registros():
    """Endpoint para insertar 50,000 registros en la base de datos."""
    resultado = insertar_registros_en_bd()
    return resultado
