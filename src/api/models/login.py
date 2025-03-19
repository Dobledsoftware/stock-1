import bcrypt
from routers import conexion
import jwt
import datetime
from fastapi import HTTPException
from .validateTokenApi import Token
from collections import namedtuple

SECRET_KEY = "STOCK"

class Login(conexion.Conexion):
    @staticmethod
    async def login_usuario(usuario: str, password: str):
        """Autentica al usuario comparando la contraseña encriptada con `bcrypt`."""
        conexion = Login().conectar()
        try:
            cursor = conexion.cursor()

            # Buscar el usuario en la base de datos
            sql = """
                SELECT id_usuario, nombre, apellido, email, usuario, password, estado 
                FROM usuarios 
                WHERE usuario = %s
            """
            cursor.execute(sql, (usuario,))
            row = cursor.fetchone()

            if row:
                Usuario = namedtuple("Usuario", ["id_usuario", "nombre", "apellido", "email", "usuario", "password", "estado"])
                user = Usuario._make(row)

                # **Comparar la contraseña encriptada con `bcrypt`**
                if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")) and user.estado:
                    token = Token()

                    # Obtener el perfil del usuario y su nombre
                    cursor.execute("""
                        SELECT p.id_perfil, p.nombre
                        FROM usuarios_perfiles up
                        JOIN perfiles p ON up.id_perfil = p.id_perfil
                        WHERE up.id_usuario = %s AND up.estado = TRUE
                    """, (user.id_usuario,))
                    perfil = cursor.fetchone()

                    if not perfil:
                        return {"message": "El usuario no tiene un perfil asignado", "code": 403}

                    id_perfil, nombre_perfil = perfil

                    # Obtener funciones del perfil con permisos
                    cursor.execute("""
                        SELECT f.id_funcion, pf.lectura, pf.escritura
                        FROM funciones f
                        JOIN perfil_funcion pf ON f.id_funcion = pf.id_funcion
                        WHERE pf.id_perfil = %s
                    """, (id_perfil,))

                    funciones = [
                        {
                            "id_funcion": row[0],                            
                            "lectura": row[1],
                            "escritura": row[2]
                        }
                        for row in cursor.fetchall()
                    ]

                    auth_token = await token.crearTokenLocal(user.id_usuario, funciones)

                    return {
                        "id_usuario": user.id_usuario,
                        "nombre": user.nombre,
                        "apellido": user.apellido,
                        "email": user.email,
                        "usuario": user.usuario,
                        "auth_token": auth_token,
                        "id_perfil": id_perfil,  # ✅ Ahora enviamos también el ID del perfil
                        "nombre_perfil": nombre_perfil,  # ✅ Ahora enviamos el nombre del perfil
                        "funciones": funciones
                    }

                else:
                    return {"message": "Usuario o contraseña incorrectos", "code": 0}

        finally:
            cursor.close()
            conexion.close()
