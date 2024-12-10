#from fastapi.responses import JSONResponse
from routers import conexion
from psycopg2.extras import DictCursor


class Proveedor(conexion.Conexion):
    def __init__(self, id_proveedor=None):
        self._id_proveedor = id_proveedor
        self._estado = None  # Inicialmente no conocemos el estado

    @property
    def estado(self):
        return self._estado
################################# CARGA DATOS DEL OBJETO ############################################################
    async def cargar_estado(self):
        """Método para cargar el estado actual del proveedor desde la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "SELECT estado FROM proveedores WHERE id_proveedor = %s"
            cursor.execute(sql, (self._id_proveedor,))
            result = cursor.fetchone()
            print ("muestro el objeto cargado",self._id_proveedor)
            if result:
                self._estado = result[0]
            else:
                raise ValueError(f"Recibo con id {self._id_proveedor} no encontrado.")
        finally:
            conexion.close()
##################################### CAMBIA ESTADO AL OBJETO #################################################
    async def cambiar_estado(self, nuevo_estado):
        """Método para cambiar el estado del proveedor."""
        if nuevo_estado not in ['Activado', 'Desactivado']:
            raise ValueError("El estado debe ser 'Activado' o 'Desactivado'.")

        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            # Actualiza el estado del proveedor
            sql_update = """
            UPDATE proveedores
            SET estado = %s
            WHERE id_proveedor = %s
            """
            cursor.execute(sql_update, (nuevo_estado, self._id_proveedor))
            conexion.commit()

            # Verifica si realmente se cambió el estado
            sql_select = "SELECT estado FROM proveedores WHERE id_proveedor = %s"
            cursor.execute(sql_select, (self._id_proveedor,))
            result = cursor.fetchone()

            if result and result[0] == nuevo_estado:
                self._estado = nuevo_estado
                return {"status": "success", "estado": nuevo_estado, "id_proveedor": self._id_proveedor}
            else:
                # Si no coincide el nuevo estado, se devuelve un error
                return {"status": "error", "message": f"Error al actualizar el estado a {nuevo_estado}."}
        finally:
            conexion.close()

   
   

################################################################################################


    async def verTodosLosProductos(self, estado):
        """Obtiene todos los proveedors según su estado."""
        conexion = self.conectar()

        try:
            # Usa DictCursor para resultados como diccionario
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql = """
            SELECT 
                p.id_proveedor AS proveedor_id, 
                p.nombre AS proveedor_nombre, 
                p.descripcion AS proveedor_descripcion, 
                p.precio AS proveedor_precio, 
                p.stock_actual AS proveedor_stock, 
                p.fecha_creacion AS proveedor_fecha_creacion,
                p.fecha_ultima_modificacion AS proveedor_fecha_modificacion,
                p.estado AS proveedor_estado,
                pr.id AS proveedor_id, 
                pr.nombre AS proveedor_nombre, 
                pr.direccion AS proveedor_direccion,
                pr.telefono AS proveedor_telefono,
                pr.correo_contacto AS proveedor_correo
            FROM 
                proveedors p            
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
            

    async def agregar_proveedor(self, nombre, descripcion, precio, stock_actual, proveedor_id, estado="Activo"):
        """Método para agregar un nuevo proveedor a la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            INSERT INTO proveedors (nombre, descripcion, precio, stock_actual, proveedor_id, estado, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            RETURNING id_proveedor;
            """
            cursor.execute(sql, (nombre, descripcion, precio, stock_actual, proveedor_id, estado))
            proveedor_id = cursor.fetchone()[0]
            conexion.commit()

            return {
                "status": "success",
                "proveedor_id": proveedor_id,
                "message": f"Producto '{nombre}' agregado exitosamente."
            }
        except Exception as e:
            print(f"Error al agregar el proveedor: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()


######################################################################################################
            

    async def eliminar_proveedor(self, proveedor_id):
        """Método para eliminar un proveedor de la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM proveedores WHERE id_proveedor = %s;"
            cursor.execute(sql, (proveedor_id,))
            conexion.commit()

            if cursor.rowcount > 0:
                return {
                    "status": "success",
                    "message": f"Producto con ID {proveedor_id} eliminado exitosamente."
                }
            else:
                return {
                    "status": "error",
                    "message": f"No se encontró ningún proveedor con ID {proveedor_id}."
                }
        except Exception as e:
            print(f"Error al eliminar el proveedor: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()
