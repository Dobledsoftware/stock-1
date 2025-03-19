from fastapi.responses import JSONResponse
from routers import conexion
from typing import Optional
from services.emailService import EmailService
import bcrypt
import string
import random


class Usuario(conexion.Conexion):
     
    @staticmethod
    async def cambiar_estado_usuario(id_usuario: int, estado: bool):
        conexion = Usuario().conectar()
        try:
            cursor = conexion.cursor()
            sql = "UPDATE usuarios SET estado = %s WHERE id_usuario = %s"
            cursor.execute(sql, (estado, id_usuario))
            conexion.commit()

            if cursor.rowcount > 0:
                return {"message": f"Usuario {'activado' if estado else 'desactivado'} correctamente", "code": 200}
            else:
                return {"message": "Usuario no encontrado", "code": 404}
        except Exception as e:
            print(f"Error al cambiar estado del usuario: {e}")
            return {"message": "Error interno al cambiar estado del usuario", "code": 500}
        finally:
            cursor.close()
            conexion.close()

##################################editar_usuario#######################################################################################

    @staticmethod
    async def editar_usuario(id_usuario: int, nombre: str, apellido: str, email: str, usuario: str):
        """Editar un usuario en la base de datos sin modificar el estado."""
        conexion = Usuario().conectar()
        try:
            cursor = conexion.cursor()

            # Obtener los datos actuales del usuario
            cursor.execute("SELECT nombre, apellido, email, usuario FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            datos_actuales = cursor.fetchone()
            if not datos_actuales:
                return {"message": "Usuario no encontrado", "code": 404}

            # Convertir los datos actuales en una tupla para comparación
            nuevos_datos = (nombre.strip(), apellido.strip(), email.strip(), usuario.strip())
            datos_actuales = (datos_actuales[0].strip(), datos_actuales[1].strip(), datos_actuales[2].strip(), datos_actuales[3].strip())

            if datos_actuales == nuevos_datos:
                return {"message": "No se detectaron cambios en los datos del usuario", "code": 304}

            # Verificar si el email ya está en uso por otro usuario
            cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s AND id_usuario <> %s", (email.strip(), id_usuario))
            if cursor.fetchone():
                return {"message": "El email ya está registrado por otro usuario", "code": 409}

            # Verificar si el nombre de usuario ya está en uso por otro usuario
            cursor.execute("SELECT id_usuario FROM usuarios WHERE usuario = %s AND id_usuario <> %s", (usuario.strip(), id_usuario))
            if cursor.fetchone():
                return {"message": "El nombre de usuario ya está en uso", "code": 409}

            # Si hay cambios, actualizar el usuario (sin modificar el estado)
            sql = """
                UPDATE usuarios 
                SET nombre = %s, apellido = %s, email = %s, usuario = %s
                WHERE id_usuario = %s
            """
            cursor.execute(sql, (nombre.strip(), apellido.strip(), email.strip(), usuario.strip(), id_usuario))
            conexion.commit()

            return {"message": "Usuario actualizado correctamente", "code": 200}

        except Exception as e:
            print(f"Error al editar usuario: {e}")
            return {"message": "Error interno al editar el usuario", "code": 500}
        finally:
            cursor.close()
            conexion.close()


##################################obtener_historial_logins#######################################################################################



    async def obtener_historial_logins(id_usuario: int):
        """Obtener el historial de logins de un usuario por su ID."""
        conexion = Usuario().conectar()
        try:
            cursor = conexion.cursor()

            # Verificar si el usuario existe antes de buscar el historial
            cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            if not cursor.fetchone():
                return {"message": "Usuario no encontrado", "code": 404}

            # Obtener historial de logins
            sql = """
                SELECT id_usuario, fecha_logins, ip_origen, exito, motivo_fallo 
                FROM logs_logins 
                WHERE id_usuario = %s
                ORDER BY fecha_logins DESC
            """
            cursor.execute(sql, (id_usuario,))
            historial = cursor.fetchall()

            # Si no hay registros, devolver mensaje adecuado
            if not historial:
                return {"message": "No hay registros de inicio de sesión para este usuario", "code": 204}

            # Convertir los resultados a un diccionario legible
            historial_list = [
                {
                    "id_usuario": row[0],
                    "fecha_logins": row[1],
                    "ip_origen": row[2],
                    "exito": row[3],
                    "motivo_fallo": row[4]
                }
                for row in historial
            ]

            return {"message": "Historial obtenido exitosamente", "code": 200, "historial": historial_list}

        except Exception as e:
            print(f"Error al obtener el historial de logins: {e}")
            return {"message": "Error interno al obtener el historial de logins", "code": 500}
        finally:
            cursor.close()
            conexion.close()



  ##################################agregar_usuario#######################################################################################
  

    async def agregar_usuario(nombre: str, apellido: str, email: str, usuario: str, password: str):
        """ Agregar un nuevo usuario con contraseña encriptada usando bcrypt (estado=True por defecto) """
        conexion = Usuario().conectar()
        try:
            cursor = conexion.cursor()

            # Verificar si el email ya está registrado
            cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email.strip(),))
            if cursor.fetchone():
                return {"message": "El email ya está registrado", "code": 409}

            # Verificar si el nombre de usuario ya está en uso
            cursor.execute("SELECT id_usuario FROM usuarios WHERE usuario = %s", (usuario.strip(),))
            if cursor.fetchone():
                return {"message": "El nombre de usuario ya está en uso", "code": 409}

            # Encriptar la contraseña con bcrypt
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

            # Insertar nuevo usuario SIN enviar el estado (ya que por defecto es TRUE)
            sql = """
                INSERT INTO usuarios (nombre, apellido, email, usuario, password)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_usuario
            """
            cursor.execute(sql, (nombre.strip(), apellido.strip(), email.strip(), usuario.strip(), hashed_password.decode("utf-8")))
            id_usuario = cursor.fetchone()[0]
            conexion.commit()

            return {"message": "Usuario agregado correctamente", "id_usuario": id_usuario, "code": 201}

        except Exception as e:
            print(f"Error al agregar usuario: {e}")
            return {"message": "Error interno al agregar usuario", "code": 500}
        finally:
            cursor.close()
            conexion.close()



  ##################################cambiar_password (desde el propio usuario)#######################################################################################


    @staticmethod
    async def cambiar_password_usuario(id_usuario: int, password_actual: str, password_nuevo: str):
        """
        Permite a un usuario cambiar su propia contraseña verificando la actual.
        """
        conexion = Usuario().conectar()
        try:
            cursor = conexion.cursor()

            # Buscar la contraseña actual del usuario
            cursor.execute("SELECT password FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            row = cursor.fetchone()

            if not row:
                return {"message": "Usuario no encontrado", "code": 404}

            password_hash_db = row[0]  # Contraseña almacenada en la BD

            # Verificar si la contraseña actual ingresada es correcta
            if not bcrypt.checkpw(password_actual.encode("utf-8"), password_hash_db.encode("utf-8")):
                return {"message": "La contraseña actual es incorrecta", "code": 401}

            # Hashear la nueva contraseña
            salt = bcrypt.gensalt()
            password_nuevo_hash = bcrypt.hashpw(password_nuevo.encode("utf-8"), salt).decode("utf-8")

            # Actualizar la contraseña en la base de datos
            cursor.execute("UPDATE usuarios SET password = %s WHERE id_usuario = %s", (password_nuevo_hash, id_usuario))
            conexion.commit()

            return {"message": "Contraseña actualizada correctamente", "code": 200}

        except Exception as e:
            print(f"❌ Error en cambiar_password_usuario: {e}")
            return {"message": "Error interno al cambiar la contraseña", "code": 500}

        finally:
            cursor.close()
            conexion.close()
  ##################################cambiar_password (desde el propio usuario)#######################################################################################

    @staticmethod
    async def resetear_password_admin(id_usuario: int):
        """
        Permite a un administrador resetear la contraseña de un usuario y devolverla en la respuesta JSON.
        """
        conexion = Usuario().conectar()
        try:
            cursor = conexion.cursor()

            # Obtener el email del usuario
            cursor.execute("SELECT email FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            row = cursor.fetchone()

            if not row:
                return {"message": "Usuario no encontrado", "code": 404}

            email_usuario = row[0]  # Correo del usuario

            # Generar una contraseña temporal aleatoria
            caracteres = string.ascii_letters + string.digits
            password_temporal = ''.join(random.choices(caracteres, k=10))

            # Hashear la contraseña temporal antes de guardarla en la BD
            salt = bcrypt.gensalt()
            password_temporal_hash = bcrypt.hashpw(password_temporal.encode("utf-8"), salt).decode("utf-8")

            # Actualizar la contraseña en la BD
            cursor.execute("UPDATE usuarios SET password = %s WHERE id_usuario = %s", (password_temporal_hash, id_usuario))
            conexion.commit()

            return {
                "message": "Contraseña reseteada correctamente",
                "password_temporal": password_temporal,  # ✅ Devolvemos la contraseña temporal en el JSON
                "code": 200
            }

        except Exception as e:
            print(f"❌ Error en resetear_password_admin: {e}")
            return {"message": "Error interno al resetear la contraseña", "code": 500}

        finally:
            cursor.close()
            conexion.close()