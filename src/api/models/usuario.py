from fastapi.responses import JSONResponse
from routers import conexion
from typing import Optional
from services.emailService import EmailService

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



    