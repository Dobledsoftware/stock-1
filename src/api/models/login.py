from routers import conexion
import jwt
import datetime

class Login(conexion.Conexion):
    @staticmethod
    async def login_usuario(cuil, password):
        conexion = Login().conectar()
        cursor = None
        print("ENTRO esta son las variables: " + cuil + password)
        try:
            cursor = conexion.cursor()
            # Se seleccionan todas las columnas de la tabla usuarios
            sql = "SELECT * FROM usuarios WHERE cuil = %s"
            
            cursor.execute(sql, (cuil,))
            user_db = cursor.fetchone()            
            columns = [desc[0] for desc in cursor.description]  # cursor.description contiene los nombres de las columnas                
                # Convertimos la fila de datos en un diccionario, con los nombres de las columnas como claves
            user_data = dict(zip(columns, user_db))

                # Ahora podemos acceder a los datos por nombre de columna, de forma segura
            print("Datos obtenidos de la base de datos:", user_data)

                # Si los datos esperados existen, podemos trabajar con ellos
            if 'id_usuario' in user_data and 'nombre' in user_data:
                    id_usuario = user_data['id_usuario']
                    nombre = user_data['nombre']
                    apellido = user_data.get('apellido', 'No disponible')  # Valor por defecto si no existe
                    email = user_data.get('email', 'No disponible')
                    pass_db = user_data.get('user_pass', 'No disponible')
                    rol = user_data.get('rol', 'No disponible')
                    fecha_creacion = user_data.get('fecha_creacion', 'No disponible')
                    habilitado = user_data.get('habilitado', False)
                    validacion_correo = user_data.get('validacion_correo', False)
                    cuil_db = user_data.get('cuil_db', 'No disponible')
            else:
                    print("Faltan algunos datos esperados.")
                    return {"message": "Error en los datos de la base de datos", "code": 6}
         

                # Validación de la contraseña y habilitación del usuario
            print("************"+password+"***"+pass_db)

            if password == pass_db:
                    # Validamos el correo si está habilitado
                    
                        auth_token = create_jwt_token(id_usuario, rol, cuil)
                        return {
                            "id_usuario": id_usuario,
                            "rol": rol,
                            "cuil": cuil,
                            "nombre": nombre,
                            "apellido": apellido,
                            "email": email,
                            "auth_token": auth_token
                        }              
                        
            else:
                print("No se encontró el usuario.")
                return {"message": "Usuario no encontrado", "code": 1}

        except Exception as e:
            print(f"Error en el proceso de login: {e}")
            return {"message": "Error interno", "code": 5}

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()




SECRET_KEY = "Recibos"


def create_jwt_token(user_id, rol, cuil):
    payload = {
        "user_id": user_id,
        "rol": rol,
        "cuil": cuil,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
