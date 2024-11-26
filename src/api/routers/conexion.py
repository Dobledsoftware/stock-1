import mariadb
import os
class Conexion:
    def conectar(self):
        return mariadb.connect(
            user=os.getenv('DB_USER', 'pablo'),
            password=os.getenv('DB_PASSWORD', 'P4bl0'),
            host=os.getenv('DB_HOST', '10.5.0.124'),
            port=3306,
            database=os.getenv('DB_NAME', 'recibosdb')
        )
    
    
def cursor(self):
        return self.conexion.cursor()

def close(self):
        if self.conexion.is_connected():
            self.conexion.close()