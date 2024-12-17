#from fastapi.responses import JSONResponse
from routers import conexion
from typing import Optional
from psycopg2.extras import DictCursor
from fastapi import HTTPException
from .producto_refractor import ProductoRepository



class Producto(conexion.Conexion):
    def __init__(self, id_producto=None):
        self._id_producto = id_producto
        self._estado = None
        self._nombre = None
        self._marca = None
        # Otros atributos que pueden inicializarse
        self._descripcion = None
        self._precio = None
        self.repository = ProductoRepository()

    # Propiedades
    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        if value not in ['Activo', 'Inactivo']:
            raise ValueError("El estado debe ser 'Activo' o 'Inactivo'.")
        self._estado = value

    @property
    def nombre(self):
        return self._nombre

    @property
    def marca(self):
        return self._marca
        
################################# CARGA DATOS DEL OBJETO ############################################################
    async def cargar_estado(self):
        """Método para cargar el estado actual del proveedor desde la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "SELECT estado FROM productos WHERE id_producto = %s"
            cursor.execute(sql, (self._id_producto,))
            result = cursor.fetchone()
            print ("muestro el objeti cargado",self._id_producto)
            if result:
                self._estado = result[0]
            else:
                raise ValueError(f"Recibo con id {self._id_producto} no encontrado.")
        finally:
            conexion.close()
##################################### CAMBIA ESTADO AL OBJETO #################################################
    async def cambiar_estado(self, nuevo_estado):
        """Método para cambiar el estado del producto."""
        if nuevo_estado not in ['Activo', 'Inactivo']:
            raise ValueError("El estado debe ser 'Activo' o 'Inactivo'.")

        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            # Actualiza el estado del producto
            sql_update = """
            UPDATE productos
            SET estado = %s
            WHERE id_producto = %s
            """
            cursor.execute(sql_update, (nuevo_estado, self._id_producto))
            conexion.commit()

            # Verifica si realmente se cambió el estado
            sql_select = "SELECT estado FROM productos WHERE id_producto = %s"
            cursor.execute(sql_select, (self._id_producto,))
            result = cursor.fetchone()

            if result and result[0] == nuevo_estado:
                self._estado = nuevo_estado
                return {"status": "success", "estado": nuevo_estado, "id_producto": self._id_producto}
            else:
                # Si no coincide el nuevo estado, se devuelve un error
                return {"status": "error", "message": f"Error al actualizar el estado a {nuevo_estado}."}
        finally:
            conexion.close()



########################verTodosLosProductos########################################################################
            




    async def verTodosLosProductos(self, estado):
        """Lista productos según su estado."""
        return await self.repository.verTodosLosProductos(estado)      


    

##########################agregar_producto#########################################################################
    
    async def agregar_producto(self, marca, nombre, descripcion, precio, codigo_barras,id_categoria, imagen_producto=None, force_add=False,):
        """
        Agrega un producto (variante) a la base de datos, verificando si ya existe un producto con el mismo código de barras.
        Si force_add es True, permite duplicar el producto aunque tenga el mismo código de barras.
        """
        return await self.repository.agregar_producto(marca, nombre, descripcion, precio, codigo_barras,id_categoria, imagen_producto, force_add)


    
###############################eliminar_producto#######################################################################
            
    async def eliminarProducto(self, producto_id):
       
        return await self.repository.eliminarProducto(producto_id)      


    
########################################################################################


    async def buscarPorCodigoDeBarras(self, codigo_barras):
        """
        Busca todas las variantes asociadas a un código de barras.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT p.id_producto, p.nombre, p.descripcion, p.precio, s.stock_actual, s.stock_minimo, s.stock_maximo
            FROM productos p
            JOIN stock s ON p.id_producto = s.id_producto
            WHERE p.codigo_barras = %s;
            """
            cursor.execute(sql, (codigo_barras,))
            variantes = cursor.fetchall()

            if not variantes:
                return {"status": "error", "message": "No se encontraron productos con este código de barras."}

            return {
                "status": "success",
                "variantes": [
                    {
                        "id_producto": var[0],
                        "nombre": var[1],
                        "descripcion": var[2],
                        "precio": var[3],
                        "stock_actual": var[4],
                        "stock_minimo": var[5],
                        "stock_maximo": var[6]
                    }
                    for var in variantes
                ]
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

        finally:
            conexion.close()



########################################################################################

