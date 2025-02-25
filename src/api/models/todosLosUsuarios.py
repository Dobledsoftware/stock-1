from routers import conexion
from collections import namedtuple

class TodosLosUsuarios(conexion.Conexion):
    @staticmethod
    async def obtener_todos(estado: bool):
        conexion = TodosLosUsuarios().conectar()
        try:
            cursor = conexion.cursor()
            sql = "SELECT id_usuario, nombre, apellido, email, usuario, estado FROM usuarios WHERE estado = %s"
            cursor.execute(sql, (estado,))
            rows = cursor.fetchall()

            # Convertimos cada usuario en una NamedTuple para mejorar la legibilidad
            Usuario = namedtuple("Usuario", ["id_usuario", "nombre", "apellido", "email", "usuario", "estado"])
            usuarios = [Usuario._make(row)._asdict() for row in rows]

            return usuarios
        except Exception as e:
            print(f"Error al obtener los usuarios: {e}")
            return {"message": "Error al obtener los usuarios", "code": 500}
        finally:
            cursor.close()
            conexion.close()
