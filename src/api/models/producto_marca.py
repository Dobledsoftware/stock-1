from routers import conexion
from psycopg2.extras import DictCursor
from typing import Optional
from fastapi import HTTPException


class ProductoMarca(conexion.Conexion):
    def __init__(self, id_marca=None):
        self._id_marca = id_marca
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

################################ ALTA DE MARCA ############################################################
    async def agregar_marca(self, descripcion, estado=True):
        """
        Agrega una nueva marca a la base de datos.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            INSERT INTO producto_marca (descripcion, estado)
            VALUES (%s, %s)
            RETURNING id_marca;
            """
            cursor.execute(sql, (descripcion, estado))
            id_marca = cursor.fetchone()[0]
            conexion.commit()
            return {"status": "success", "id_marca": id_marca, "descripcion": descripcion}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conexion.close()

################################ MODIFICAR MARCA ###########################################################
            
    async def modificar_marca(self, id_marca, descripcion: Optional[str] = None, estado: Optional[bool] = None):
        """
        Modifica los datos de una marca existente en la base de datos.
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

            valores.append(id_marca)
            sql = f"""
            UPDATE producto_marca
            SET {', '.join(campos)}
            WHERE id_marca = %s;
            """
            cursor.execute(sql, valores)
            conexion.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"Marca con id {id_marca} no encontrada.")

            return {"status": "success", "id_marca": id_marca}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conexion.close()

################################ ELIMINAR MARCA #############################################################
    async def eliminar_marca(self, id_marca):
        """
        Elimina una marca de la base de datos (soft delete cambiando estado a FALSE).
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE producto_marca
            SET estado = FALSE
            WHERE id_marca = %s;
            """
            cursor.execute(sql, (id_marca,))
            conexion.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"Marca con id {id_marca} no encontrada.")

            return {"status": "success", "message": "Marca desactivada", "id_marca": id_marca}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conexion.close()

################################ VER TODAS LAS MARCAS #######################################################
    async def ver_todas_marcas(self, estado):
        """
        Lista todas las marcas activas o inactivas dependiendo del parámetro.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)            
            sql = f"SELECT * FROM producto_marca WHERE estado = {str(estado).upper()} ORDER BY id_marca;"
            cursor.execute(sql)
            marcas = cursor.fetchall()
            return [dict(marca) for marca in marcas]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conexion.close()
