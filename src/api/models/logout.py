from fastapi import HTTPException, Response
from routers.conexion import Conexion  # ✅ Importamos la conexión correctamente

class Logout(Conexion):
    """Clase para manejar el cierre de sesión eliminando el token de `tokens_activos`."""

    @staticmethod
    async def cerrar_sesion(response: Response, token: str):
        conexion = Logout().conectar()  # ✅ Ahora usa `Conexion`
        if not conexion:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos.")

        try:
            cursor = conexion.cursor()

            # ✅ Verificar si el token existe en `tokens_activos`
            cursor.execute("SELECT token FROM tokens_activos WHERE token = %s;", (token,))
            token_existente = cursor.fetchone()

            if not token_existente:
                raise HTTPException(status_code=401, detail="Token inválido o ya expirado.")

            # ✅ Si el token existe, eliminarlo
            sql = "DELETE FROM tokens_activos WHERE token = %s;"
            cursor.execute(sql, (token,))
            conexion.commit()

            # ✅ Eliminar la cookie del token
            response.delete_cookie(key="auth_token")

            return {"status": "success", "message": "Sesión cerrada correctamente."}

        except Exception as e:
            conexion.rollback()
            raise HTTPException(status_code=500, detail=f"Error al cerrar sesión: {str(e)}")
        finally:
            cursor.close()
            conexion.close()
