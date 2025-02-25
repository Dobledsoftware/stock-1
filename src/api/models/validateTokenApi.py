import jwt
from datetime import datetime, timezone as dt_timezone, timedelta,timezone
import uuid
import pytz  # Se requiere para trabajar con zonas horarias específicas como "America/Argentina/Buenos_Aires"
from pytz import timezone as pytz_timezone  # Renombramos para evitar colisión

from routers import conexion
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import aiohttp


SECRET_KEY = "RECIBOS"  

#########################crearTokenLocal#########################################3

class Token(conexion.Conexion):
   
    async def crearTokenLocal(self, id_usuario,funciones):
        try:
            token_instance = Token()
            await token_instance.eliminarTokensExpirados()

            utc_now = datetime.now(timezone.utc)  # Hora actual en UTC
            
            payload = {
                "id_usuario": id_usuario,
                "funciones":funciones,
                "iat": int(utc_now.timestamp()),  # Momento en que se creó el token
                "jti": str(uuid.uuid4())  # ID único para cada token
            }
            print("payload",payload)

            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            print("TOKEN QUE SE GENERA",token)
            # Guardar token en la base de datos
            resultado = await token_instance.guardar_o_actualizar_token(token, id_usuario)
            return resultado  # Devuelve el mensaje de éxito o error

        except Exception as e:
            print(f"Error al almacenar el token: {e}")
            return None



    async def guardar_o_actualizar_token(self, token, id_usuario):
        conexion = self.conectar()
        if conexion is None:
            raise ValueError("Error: No se pudo establecer la conexión a la base de datos.")
        try:
            cursor = conexion.cursor() 
            # Obtener hora actual en UTC-3 (Argentina)
            utc_now = datetime.now(timezone.utc)
            argentina_tz = pytz.timezone("America/Argentina/Buenos_Aires")
            exp_local = utc_now + timedelta(minutes=10)  # Agregar 10 minutos        
            exp_local = exp_local.astimezone(argentina_tz)  # Convertir a UTC-3
            exp_str = exp_local.strftime('%Y-%m-%d %H:%M:%S')  # Formatear fecha
            utc_now = utc_now.astimezone(argentina_tz)  # Convertir a UTC-3
            utc_now=utc_now.strftime('%Y-%m-%d %H:%M:%S')
            # Verificar si ya existe un token activo para el usuario
            consulta_verificar = """
                SELECT token, exp FROM tokens_activos WHERE id_usuario = %s
            """
            cursor.execute(consulta_verificar, (id_usuario,))
            resultado = cursor.fetchone()

            if resultado:
                token_actual, exp_actual = resultado
                exp_actual_dt = exp_actual
                #Convierto para poder usar el operador de comparacion
                exp_actual_dt = datetime.strptime(exp_actual, '%Y-%m-%d %H:%M:%S') if isinstance(exp_actual, str) else exp_actual
                utc_now = datetime.strptime(utc_now, '%Y-%m-%d %H:%M:%S') if isinstance(utc_now, str) else utc_now
                # Si el token aún es válido, solo actualizamos la expiración
                if exp_actual_dt > utc_now:
                    consulta_actualizar = """
                        UPDATE tokens_activos SET exp = %s WHERE id_usuario = %s
                    """
                    cursor.execute(consulta_actualizar, (exp_str, id_usuario))
                    conexion.commit()
                    return "Sesión ya iniciada, tiempo de expiración actualizado."

                else:
                    # Token expirado, generamos uno nuevo
                    consulta_actualizar = """
                        UPDATE tokens_activos SET token = %s, exp = %s WHERE id_usuario = %s
                    """
                    cursor.execute(consulta_actualizar, (token, exp_str, id_usuario))
                    conexion.commit()
                    return "Token expirado, se generó uno nuevo."

            else:
                print("ENTRA A guardar_o_actualizar_token")

                # No existe un token previo, se crea uno nuevo
                consulta_insertar = """
                    INSERT INTO tokens_activos (token, id_usuario, exp)
                    VALUES (%s, %s, %s)
                """
                print("ENTRA A guardar_o_actualizar_token",consulta_insertar)
                cursor.execute(consulta_insertar, (token, id_usuario, exp_str))
                conexion.commit()
                return token

        except Exception as e:
            print(f"Error al manejar el token: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()
#########################checkTokenGeneral#########################################3

    @staticmethod
    async def checkTokenGeneral(token: str) -> dict:
        """
        Valida un token usando:
        1. Validación contra un servicio externo (LDAP).
        2. Validación local si la validación LDAP indica que el token es inválido.
        Si ninguna validación es exitosa, retorna un error.
        """
        ldap_url = "http://10.5.0.124:8000/check/validatetoken"  # URL del servicio LDAP
        headers = {'Authorization': f'Bearer {token}'}
# Validación contra LDAP
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(ldap_url, headers=headers) as response:
                    if response.status == 200:
                        ldap_data = await response.json()
                        if "samaccountname" in ldap_data and ldap_data["samaccountname"]:                            
                            return ldap_data
                    else:
                        token_local = await Token.validateLocalToken(token)                        
                        return token_local
        except aiohttp.ClientError as e:
            print(f"Error al conectar con LDAP: {str(e)}")
            # Continúa con la validación local

        # Validación local
        local_validation = await Token.validateLocalToken(token)
        if local_validation["validate"]:
            return {"validate": True, "source": "Local", "data": local_validation["data"]}

        # Si ninguna validación es exitosa
        return {"validate": False, "error": "Token inválido en ambas validaciones (LDAP y local)."}
    
#########################eliminarTokensExpirados#########################################3
      
    async def eliminarTokensExpirados(self):
        """
        Elimina los tokens que ya han expirado de la base de datos.
        """
        conexion = self.conectar()
  # Usamos tu conexión sincrónica
        if not conexion:
            return {"validate": False, "error": "Error de conexión a la base de datos."}
        
        try:
            with conexion.cursor() as cursor:
                # Eliminar tokens expirados
                consulta_eliminar_expirados = """
                    DELETE FROM tokens_activos
                    WHERE exp < NOW()
                """
                cursor.execute(consulta_eliminar_expirados)
                conexion.commit()
                return {"validate": True}  # Retorna un mensaje de éxito
        except Exception as e:
            return {"validate": False, "error": str(e)}  # Devuelve el error
        finally:
            conexion.close()  # Asegúrate de cerrar la conexión


#########################validateLocalToken#########################################3

    @staticmethod
    async def validateLocalToken(token):
        """
        Valida el token y verifica en la base de datos si es el único activo para el usuario.
        Si está cerca de expirar, extiende la fecha de expiración.
        Si ha expirado, lo elimina de la base de datos.
        """
        conexion = Token().conectar()  # Usamos tu conexión sincrónica   
        if not conexion:
            return {"validate": False, "error": "Error de conexión a la base de datos."}
        try:
            # Eliminar los tokens expirados
            token_instance = Token()
            await token_instance.eliminarTokensExpirados()
            # Decodificar el token
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Extraer información del token
            id_usuario = payload.get("id_usuario")  

            if not id_usuario:
                return {"validate": False, "error": "El token no contiene un id_usuario válido."}                                                                            

            with conexion.cursor() as cursor:
                # Consultar si el token está activo para el usuario
                consulta_verificar = """
                    SELECT token, exp
                    FROM tokens_activos
                    WHERE id_usuario = %s
                    """
                cursor.execute(consulta_verificar, (id_usuario,))
                resultado = cursor.fetchone()                  
                # Si el token no está en la base de datos, lo consideramos no válido
                if not resultado:  
                    # Eliminar los tokens expirados
                    token_instance = Token()
                    await token_instance.eliminarTokensExpirados()
                    return {"validate": False, "error": "El token no está activo para el usuario."}                                       
                # Si el token está cerca de expirar, actualizamos la fecha de expiración
                #await token_instance.guardar_o_actualizar_token(token,id_usuario)
                await Token().guardar_o_actualizar_token(token, id_usuario)
                # Actualizamos la fecha de expiración en la base de datos 
                return {"validate": True, "data": payload}

        except jwt.ExpiredSignatureError:
            return {"validate": False, "error": "El token ha expirado."}
        except jwt.InvalidTokenError as e:
            return {"validate": False, "error": "El token no es válido."}
        except Exception as e:
            return {"validate": False, "error": f"Error interno: {str(e)}"}
        finally:
            if conexion:
                conexion.close()