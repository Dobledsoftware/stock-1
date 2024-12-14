from routers import conexion
from psycopg2.extras import DictCursor
from typing import Optional


class ProductoCategoria(conexion.Conexion):
    def __init__(self, id_categoria=None):
        self._id_categoria = id_categoria
        self._descripcion = None
        self._fecha_alta = None
        self._estado = None

    # Propiedades
    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, value):
        if not value or len(value) > 255:
            raise ValueError("La descripcion debe ser una cadena no vacía y menor a 255 caracteres.")
        self._descripcion = value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        if not isinstance(value, bool):
            raise ValueError("El estado debe ser un valor booleano.")
        self._estado = value

################################ ALTA DE CATEGORIA ############################################################
    async def agregar_categoria(self, descripcion, estado=True):
        """
        Agrega una nueva categoría a la base de datos.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            INSERT INTO categoria_producto (descripcion, estado)
            VALUES (%s, %s)
            RETURNING id_categoria;
            """
            cursor.execute(sql, (descripcion, estado))
            id_categoria = cursor.fetchone()[0]
            conexion.commit()
            return {"status": "success", "id_categoria": id_categoria, "descripcion": descripcion}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conexion.close()

################################ MODIFICAR CATEGORIA ###########################################################
    async def modificar_categoria(self, id_categoria, descripcion: Optional[str] = None, estado: Optional[bool] = None):
        """
        Modifica los datos de una categoría existente en la base de datos.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            campos = []
            valores = []

            if descripcion:
                campos.append("descripcion = %s")
                valores.append(descripcion)

            if estado is not None:
                campos.append("estado = %s")
                valores.append(estado)

            if not campos:
                raise ValueError("No se proporcionó ningún campo para actualizar.")

            valores.append(id_categoria)
            sql = f"""
            UPDATE categoria_producto
            SET {', '.join(campos)}
            WHERE id_categoria = %s;
            """
            cursor.execute(sql, valores)
            conexion.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"Categoria con id {id_categoria} no encontrada.")

            return {"status": "success", "id_categoria": id_categoria}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conexion.close()

################################ ELIMINAR CATEGORIA #############################################################
    async def eliminar_categoria(self, id_categoria):
        """
        Elimina una categoría de la base de datos (soft delete cambiando estado a FALSE).
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE categoria_producto
            SET estado = FALSE
            WHERE id_categoria = %s;
            """
            cursor.execute(sql, (id_categoria,))
            conexion.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"Categoria con id {id_categoria} no encontrada.")

            return {"status": "success", "message": "Categoría desactivada", "id_categoria": id_categoria}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conexion.close()

################################ VER TODAS LAS CATEGORIAS #######################################################
    async def ver_todas_categorias(self, incluir_inactivas=False):
        """
        Lista todas las categorías activas o inactivas dependiendo del parámetro.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql = "SELECT * FROM categoria_producto"
            if not incluir_inactivas:
                sql += " WHERE estado = TRUE"
            sql += " ORDER BY id_categoria;"

            cursor.execute(sql)
            categorias = cursor.fetchall()

            return [dict(categoria) for categoria in categorias]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conexion.close()
