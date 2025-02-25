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
        self._precio_venta_ars = None
        self._precio_venta_usd = None

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
                raise ValueError(f"Producto con id {self._id_producto} no encontrado.")
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
    
    async def agregar_producto(self, id_marca, nombre, descripcion, precio_venta_ars,precio_venta_usd, codigo_barras,id_categoria, imagen_producto=None, force_add=False,):
        """
        Agrega un producto (variante) a la base de datos, verificando si ya existe un producto con el mismo código de barras.
        Si force_add es True, permite duplicar el producto aunque tenga el mismo código de barras.
        """
        return await self.repository.agregar_producto(id_marca, nombre, descripcion, precio_venta_ars,precio_venta_usd, codigo_barras,id_categoria, imagen_producto, force_add)

    
###############################eliminar_producto#######################################################################
            
    async def eliminarProducto(self, producto_id):
       
        return await self.repository.eliminarProducto(producto_id)      


    
#################################buscarPorCodigoDeBarras#######################################################
    async def buscarPorCodigoDeBarras(self, codigo_barras,estado):
       
        return await self.repository.buscarPorCodigoDeBarras(codigo_barras,estado)    
    

    
#################################editarProducto#######################################################
    async def editarProducto(self,id_producto, id_marca, nombre, descripcion, precio_venta_ars,precio_venta_usd, codigo_barras,id_categoria,id_usuario, imagen_producto=None):
        
        return await self.repository.editarProducto(id_producto,id_marca, nombre, descripcion, precio_venta_ars,precio_venta_usd, codigo_barras,id_categoria,id_usuario,imagen_producto)

#################################editarProducto#######################################################
    async def consultarHistorialProducto(self,id_producto):        
        return await self.repository.consultarHistorialProducto(id_producto)

#######################################################################################################
    async def obtener_configuracion(self):        
        return await self.repository.obtener_configuracion()

    
    async def actualizar_configuracion(self,permitir_precio_menor_costo_ars, permitir_precio_menor_costo_usd,
        ajuste_precio_porcentaje_ars, ajuste_precio_porcentaje_usd, valor_dolar):        
        return await self.repository.actualizar_configuracion(permitir_precio_menor_costo_ars, permitir_precio_menor_costo_usd,
        ajuste_precio_porcentaje_ars, ajuste_precio_porcentaje_usd, valor_dolar)

    
    async def convertir_precios_dolares(self):        
        return await self.repository.convertir_precios_dolares()
   


    