#from fastapi.responses import JSONResponse
from routers import conexion
from psycopg2.extras import DictCursor


class Producto(conexion.Conexion):
    def __init__(self, id_recibo=None):
        self._id_recibo = id_recibo
        self._estado = None  # Inicialmente no conocemos el estado

    @property
    def estado(self):
        return self._estado
################################# CARGA DATOS DEL OBJETO ############################################################
    async def cargar_estado(self):
        """Método para cargar el estado actual del recibo desde la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "SELECT estado FROM productos WHERE id_recibo = %s"
            cursor.execute(sql, (self._id_recibo,))
            result = cursor.fetchone()
            print ("muestro el objeti cargado",self._id_recibo)
            if result:
                self._estado = result[0]
            else:
                raise ValueError(f"Recibo con id {self._id_recibo} no encontrado.")
        finally:
            conexion.close()
##################################### CAMBIA ESTADO AL OBJETO #################################################
    async def cambiar_estado(self, nuevo_estado):
        """Método para cambiar el estado del recibo."""
        if nuevo_estado not in ['Activado', 'Desactivado']:
            raise ValueError("El estado debe ser 'Activado' o 'Desactivado'.")

        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            # Actualiza el estado del recibo
            sql_update = """
            UPDATE recibos
            SET estado = %s
            WHERE id_recibo = %s
            """
            cursor.execute(sql_update, (nuevo_estado, self._id_recibo))
            conexion.commit()

            # Verifica si realmente se cambió el estado
            sql_select = "SELECT estado FROM recibos WHERE id_recibo = %s"
            cursor.execute(sql_select, (self._id_recibo,))
            result = cursor.fetchone()

            if result and result[0] == nuevo_estado:
                self._estado = nuevo_estado
                return {"status": "success", "estado": nuevo_estado, "id_recibo": self._id_recibo}
            else:
                # Si no coincide el nuevo estado, se devuelve un error
                return {"status": "error", "message": f"Error al actualizar el estado a {nuevo_estado}."}
        finally:
            conexion.close()

################################################################################################
    async def download(self):
        """Método para obtener la URL (ruta relativa) del archivo del recibo a partir de su ID."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()

            # Verifica que el ID del recibo sea correcto (tipo y contenido)
            print(f"Valor de id_recibo en la consulta: {self._id_recibo} (tipo: {type(self._id_recibo)})")

            # Corregir la consulta SQL para que seleccione el archivo donde id_recibo coincida
            sql = "SELECT archivo FROM recibos WHERE id_recibo = %s and estado='Activado'"
            cursor.execute(sql, (self._id_recibo,))

            # Depurar el resultado de la consulta
            result = cursor.fetchone()
            if result:
                return result[0]  # Retornar la ruta relativa del archivo
            else:
                # Lanzar excepción si no se encuentra el registro
                raise ValueError(f"Recibo con id_reciboxxxxx='{self._id_recibo}' no encontrado.")
        finally:
            conexion.close()
   

################################################################################################


    async def verTodosLosProductos(self, estado):
        """Obtiene todos los productos según su estado."""
        conexion = self.conectar()

        try:
            # Usa DictCursor para resultados como diccionario
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql = """
            SELECT 
                p.id AS producto_id, 
                p.nombre AS producto_nombre, 
                p.descripcion AS producto_descripcion, 
                p.precio AS producto_precio, 
                p.stock_actual AS producto_stock, 
                p.fecha_creacion AS producto_fecha_creacion,
                p.fecha_ultima_modificacion AS producto_fecha_modificacion,
                p.estado AS producto_estado,
                pr.id AS proveedor_id, 
                pr.nombre AS proveedor_nombre, 
                pr.direccion AS proveedor_direccion,
                pr.telefono AS proveedor_telefono,
                pr.correo_contacto AS proveedor_correo
            FROM 
                productos p
            JOIN 
                proveedores pr 
            ON 
                p.proveedor_id = pr.id
            WHERE 
                p.estado = %s
            ORDER BY 
                p.nombre ASC;
            """
            # Ejecutar la consulta
            cursor.execute(sql, (estado,))
            data = cursor.fetchall()

            # Convertir a lista de diccionarios (opcional si ya es DictCursor)
            return [dict(row) for row in data]
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return {"error": str(e)}
        finally:
            conexion.close()

#################################################################################
            

    async def agregar_producto(self, nombre, descripcion, precio, stock_actual, proveedor_id, estado="Activo"):
        """Método para agregar un nuevo producto a la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            INSERT INTO productos (nombre, descripcion, precio, stock_actual, proveedor_id, estado, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            RETURNING id;
            """
            cursor.execute(sql, (nombre, descripcion, precio, stock_actual, proveedor_id, estado))
            producto_id = cursor.fetchone()[0]
            conexion.commit()

            return {
                "status": "success",
                "producto_id": producto_id,
                "message": f"Producto '{nombre}' agregado exitosamente."
            }
        except Exception as e:
            print(f"Error al agregar el producto: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()


######################################################################################################
            

    async def eliminar_producto(self, producto_id):
        """Método para eliminar un producto de la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM productos WHERE id = %s;"
            cursor.execute(sql, (producto_id,))
            conexion.commit()

            if cursor.rowcount > 0:
                return {
                    "status": "success",
                    "message": f"Producto con ID {producto_id} eliminado exitosamente."
                }
            else:
                return {
                    "status": "error",
                    "message": f"No se encontró ningún producto con ID {producto_id}."
                }
        except Exception as e:
            print(f"Error al eliminar el producto: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()
