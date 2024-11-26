from routers import conexion
import requests
import sqlite3
import jwt
from .recibo import Recibo # Importa Clase Recibo

import datetime
class Login(conexion.Conexion):

    # @staticmethod
    # def login_fallido(cuil, password, tipo_error):
    #     print("entro a login fallido")
    #     conexion = Login().conectar()
    #     try:
    #         cursor = conexion.cursor()
    #         # Obtener la IP de forma segura, manejando posibles errores
    #         try:
    #             ip_address = requests.get('https://api64.ipify.org?format=json').json().get('ip', 'IP no disponible')
    #         except requests.RequestException:
    #             ip_address = 'IP no disponible'
    #         # User agent y navegador
    #         user_agent = "Mozilla/5.0"
    #         host_name = "localhost"
    #         navegador = Login.determine_browser(user_agent)

    #         # Obtener datos geográficos (manejo de errores)
    #         token = '5b5c1330a20d77'
    #         city, country, google_maps_link = Login.get_geo_data(ip_address, token)
            
    #         # Insertar el intento de login fallido en la base de datos
    #         sql = """
    #             INSERT INTO t_logins_fallidos (usuario, pass, navegador, ip_adress, tipo_error, host_name, google_maps)
    #             VALUES (%s, %s, %s, %s, %s, %s, %s)
    #         """
    #         cursor.execute(sql, (cuil, password, navegador, ip_address, tipo_error, host_name, google_maps_link))
    #         conexion.commit()
    #     finally:
    #         cursor.close()
    #         conexion.close()

    @staticmethod
    async def login_usuario(cuil, password):
        conexion = Login().conectar()
        try:
            if conexion:
                print("Conexión a la base de datos establecida.")
            else:
                print("No se pudo establecer la conexión a la base de datos.")
            
            cursor = conexion.cursor()
            sql = "SELECT * FROM usuarios WHERE cuil = %s"
            
            cursor.execute(sql, (cuil,))
            user_db = cursor.fetchone()             
            if user_db:
                # Accede a los elementos usando índices
                id_usuario = user_db[0]
                cuil = user_db[1]
                nombre = user_db[2]
                apellido = user_db[3]
                rol = user_db[4] 
                legajo = user_db[5]
                email = user_db[6]
                validacionCorreo = user_db[7]   # Supongamos que el CUIL está en la posición 0
                user_pass = user_db[8]
                proceso_cambio_pass = user_db[9]  # Supongamos que la contraseña está en la posición 6
                habilitado = user_db[10]
                codigo_validacion_correo = user_db[11]          
                if password == user_pass and habilitado == 1:
                    #Login.registrar_login(cuil, user_db[1])  # Supongamos que el id_usuario está en la posición 1
                    if email and validacionCorreo == 1:
                        if proceso_cambio_pass == 1:
                            return {"message": "Proceso de cambio de contraseña activo", "code": 4}                                                 
                        auth_token = create_jwt_token(id_usuario, rol, cuil)
                        recibos = Recibo()  # Crea una instancia de la clase TodosLosRecibos.
                        response_recibo = await recibos.todosLosRecibos(cuil)
                        return {
                            "id_usuario": id_usuario,
                            "rol": rol,
                            "cuil": cuil,
                            "nombre":nombre,
                            "apellido":apellido,
                            "legajo":legajo,
                            "email": email,
                            "auth_token": auth_token,
                            "recibos": response_recibo 
                        }
                    elif validacionCorreo == 0:
                        print("Validación de correo requerida.")
                        return {"message": "Validación de correo requerida", "code": 2}
                    elif not email:
                        print("El correo electrónico no está declarado.")
                        return {"message": "Debe declarar su correo electrónico", "code": 3}
                else:
                    #Login.login_fallido(cuil, password, "Usuario o contraseña incorrectos")
                    return {"message": "Usuario o contraseña incorrectos", "code": 0}
        finally:
            cursor.close()
            conexion.close()

    #@staticmethod
    # def registrar_login(cuil, id_usuario):
    #     print("Registrar registrar")
    #     conexion = Login().conectar()
    #     try:
    #         cursor = conexion.cursor()
    #         sql = """
    #             INSERT INTO logins (usuario, id_usuario)
    #             VALUES (%s, %s)
    #         """
    #         cursor.execute(sql, (cuil, id_usuario))
    #         conexion.commit()
    #     finally:
    #         cursor.close()
    #         conexion.close()s
    
    # @staticmethod
    # def determine_browser(user_agent):
    #     if 'Opera' in user_agent or 'OPR' in user_agent:
    #         return 'Opera'
    #     elif 'Chrome' in user_agent:
    #         return 'Google Chrome'
    #     elif 'Firefox' in user_agent:
    #         return 'Mozilla Firefox'
    #     elif 'Edge' in user_agent:
    #         return 'Microsoft Edge'
    #     elif 'Safari' in user_agent:
    #         return 'Safari'
    #     else:
    #         return 'Otro navegador'



SECRET_KEY = "Recibos"  # Cambia esto por una clave secreta segura
def create_jwt_token(user_id, rol, cuil):
    payload = {
        "user_id": user_id,
        "rol": rol,
        "cuil": cuil,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)  # El token expira en 10 minutos
    }    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token