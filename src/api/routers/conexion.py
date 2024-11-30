import psycopg2
import os

class Conexion:
    def __init__(self):
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = psycopg2.connect(
                user=os.getenv('DATABASE_USER', 'postgres'),
                password=os.getenv('DATABASE_PASS', 'DarioDavid-bd-UBU-1'),
                host=os.getenv('DATABASE_HOST', '92.112.176.191'),
                port=int(os.getenv('DATABASE_PORT', 5432)),
                database=os.getenv('DATABASE', 'stock_TEST')
            )
            return self.conexion  # Devuelve la conexión
        except psycopg2.Error as e:
            print(f"Error al conectar a PostgreSQL: {e}")
            raise

    def cursor(self):
        if not self.conexion:
            raise Exception("No hay conexión activa. Llama a 'conectar()' primero.")
        return self.conexion.cursor()

    def close(self):
        if self.conexion and not self.conexion.closed:
            self.conexion.close()
            print("Conexión cerrada.")
