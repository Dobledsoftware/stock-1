from fastapi import APIRouter, HTTPException, UploadFile, File, Form,Query  # Importa APIRouter para crear grupos de rutas y HTTPException para gestion errores.
from fastapi.responses import JSONResponse, Response  # Importa JSONResponse para devolver respuestas JSON personalizadas.
from pydantic import BaseModel  # Importa BaseModel para definir esquemas de solicitudes y respuestas.
from typing import List,Optional,Dict, Any
from datetime import date



#importa las clases
from models.producto import Producto # Importa Clase Producto
from models.proveedor import Proveedor # Importa Clase Proveedor
from models.almacen import Almacen # Importa Clase Almacen
from models.almacen_estante import Estante # Importa Clase Almacen


from models.producto_categoria import ProductoCategoria # Importa Clase productocategoria
from models.producto_marca import ProductoMarca # Importa Clase productocategoria

from models.stock import Stock

from models.login import Login
from models.usuario import Usuario

#importa los schemas
from schemas import  Producto_request,Proveedor_request,Categoria_request, Marca_request,movimientoStockRequest,Almacen_request,Estante_request,MovimientoStockResponse,FiltrosStock

import logging  



logger = logging.getLogger(__name__)
# Crea un enrutador para agrupar las rutas relacionadas con recibos.
router = APIRouter()

#####################################productos###########################################################


# Endpoint para ver productos según el estado
@router.get("/productos",tags=["Productos"])
async def ver_todos_los_productos(
    estado: bool = Query(..., description="Estado del producto (True: Activo, False: Inactivo)"),
):
    """
    Endpoint para consultar productos por estado.
    Proporcionar el parámetro `estado` para obtener productos activos o inactivos.
    """
    try:
        # Ver todos los productos según el estado
        producto = Producto()
        response = await producto.verTodosLosProductos(estado)
        return {"data": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    


    # Endpoint para buscar productos por código de barras
@router.get("/producto/codigo_barras",tags=["Productos"])
async def buscar_por_codigo_de_barras(
    codigo_barras: str = Query(..., description="Código de barras del producto a buscar"),
    estado: bool = Query(..., description="Estado del producto (True: Activo, False: Inactivo)"),
):
    """
    Endpoint para buscar un producto por su código de barras.
    Se puede proporcionar el parámetro `estado` para filtrar el producto por estado.
    """
    try:
        producto = Producto()
        response = await producto.buscarPorCodigoDeBarras(codigo_barras, estado)
        
        if not response:
            raise HTTPException(
                status_code=404, detail="Producto no encontrado con el código de barras proporcionado."
            )
        return {"data": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    # Endpoint para buscar productos por código de barras
@router.get("/producto/historial",tags=["Productos"])
async def consultarHistorialProducto(
    id_producto: int = Query(..., description="ID del producto a buscar"),
):
    """
    Endpoint para buscar un producto por su código de barras.
    Se puede proporcionar el parámetro `estado` para filtrar el producto por estado.
    """
    try:
        producto = Producto()
        response = await producto.consultarHistorialProducto(id_producto)
        
        if not response:
            raise HTTPException(
                status_code=404, detail="historial de producto no encontrado."
            )
        return {"data": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/productos",tags=["Productos"])
async def productos(request: Producto_request):
    """
        🛍️ **API de Gestión de Productos**  
        📌 Este endpoint permite realizar operaciones CRUD en la gestión de productos.  

        ---  

        ## ✨ **Acciones Disponibles**  

        📌 **Editar Producto** 🔄  
        📌 **Agregar Producto** 🆕  
        📌 **Eliminar Producto** 🗑️  
        📌 **Buscar por Código de Barras** 🔍  


     ### 📝 **Ejemplo de Payload para Editar un Producto** ✏️ 
    ---  

        
        Utiliza este JSON para modificar un producto existente en la base de datos.  

        🔹 Nota: Se requiere el ID del producto para poder editarlo correctamente.



        ```json
        {
            "accion": "editarProducto",
            "id_producto": 29,
            "id_marca": 2,
            "nombre": "Zapatillas Air Max 2025",
            "descripcion": "Edición 2025 con nueva tecnología de amortiguación",
            "precio_venta_ars": 160.99,
            "precio_venta_usd": 199.99,
            "aplicar_incremento_automatico_ars": false,
            "aplicar_incremento_automatico_usd": false,
            "es_dolar": false,
            "codigo_barras": "1234567890123",
            "id_categoria": 3,
            "imagen_producto": "https://drive.google.com/uc?id=ID_NUEVA_IMAGEN",
            "id_usuario": 123
        }
            ```
    ---  

    ### **🆕 Agregar nuevo Producto** 🛒.
        -
            Este payload permite registrar un nuevo producto en el sistema.


        ✅ Importante:

        forceAdd: Si es true, agrega el producto aunque el código de barras ya exista.
        id_categoria: Debe ser un ID válido de una categoría existente.

        ```json
            
        
            {
            "accion": "agregarProducto",
            "id_marca": 1,
            "nombre": "Zapatillas Air Max 2024",
            "descripcion": "Zapatillas deportivas de alta calidad, edición 2024",
            "precio_venta_ars": 16.99,
            "precio_venta_usd": 19.99,
            "aplicar_incremento_automatico_ars": false,
            "aplicar_incremento_automatico_usd": false,
            "es_dolar": false,
            "codigo_barras": "1234567890123aaa",
            "id_categoria": 1,
            "imagen_producto": "https://drive.google.com/uc?id=ID_DE_TU_IMAGEN",
            "forceAdd": false
            }
        
        ```
    ---

    ### **🗑️ Eliminar Producto 🚫**

    
        ```json
            
        {
        "accion": "eliminarProducto",
        "id_producto": 29
        }
        ```    
        ```
    """
    try:       
        
        if request.accion == "agregarProducto":
                
            """
            Endpoint que maneja la solicitud de agregar un producto.
            Verifica si ya existe un producto con el mismo código de barras y maneja el caso de forceAdd.
            """
                    # Verificar parámetros requeridos
            if not all([request.id_marca, request.nombre, request.descripcion, request.precio_venta_ars,request.precio_venta_usd, request.codigo_barras,request.id_categoria]):
                raise HTTPException(
                    status_code=400,
                    detail="Los parámetros 'id_marca', 'nombre', 'descripcion', 'precio_venta_ars','precio_venta_usd', 'codigo_barras' y  'id_categoria'son requeridos."
                )
            # Crear instancia de Producto
            producto = Producto()
            # Llamar al método agregar_producto
            response = await producto.agregar_producto(
                id_marca=request.id_marca,
                nombre=request.nombre,
                descripcion=request.descripcion,
                precio_venta_ars=request.precio_venta_ars,
                precio_venta_usd=request.precio_venta_usd,
                aplicar_incremento_automatico_ars=request.aplicar_incremento_automatico_ars,
                aplicar_incremento_automatico_usd=request.aplicar_incremento_automatico_usd,
                es_dolar=request.es_dolar,
                codigo_barras=request.codigo_barras,
                id_categoria=request.id_categoria,
                imagen_producto=request.imagen_producto,                
                force_add=request.forceAdd                
            )

            return response
        
#Editar producto

        elif request.accion == "editarProducto":
                
            """
            Endpoint que maneja la solicitud de editar un producto.
            """
                    # Verificar parámetros requeridos
            if not all([request.id_producto,request.id_marca, request.nombre, request.descripcion, request.precio_venta_ars,request.precio_venta_usd, request.codigo_barras,request.id_categoria]):
                raise HTTPException(
                    status_code=400,
                    detail="Los parámetros 'id_producto','id_marca', 'nombre', 'descripcion', 'precio_venta_ars', 'precio_venta_usd','codigo_barras' y  'id_categoria'son requeridos."
                )
            # Crear instancia de Producto
            producto = Producto()
            # Llamar al método editarProducto
            response = await producto.editarProducto(
                request.id_producto,
                request.id_marca,
                request.nombre, 
                request.descripcion, 
                request.precio_venta_ars, 
                request.precio_venta_usd, 
                request.codigo_barras,
                request.id_categoria, 
                request.id_usuario,
                request.imagen_producto              
            )

            return response



# Eliminar producto
        elif request.accion == "eliminarProducto":
            if request.id_producto is None:
                raise HTTPException(
                    status_code=400,
                    detail="El parámetro 'id_producto' es requerido para esta acción."
                )
            producto = Producto()
            response = await producto.eliminarProducto(request.id_producto)
            return response

        else:
            # Acción no válida
            raise HTTPException(
                status_code=400,
                detail="Acción no válida. Las acciones soportadas son: 'agregarProducto', 'eliminarProducto'."
            )

    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(status_code=500, detail=str(e))
    
    


###############################gestion_proveedor############################################################################################

# GET endpoint para ver todos los proveedores por estado
@router.get("/proveedores",tags=["Proveedores"])
async def ver_todos_los_proveedores(
    estado: bool = Query(..., description="Estado del proveedor (True: Activo, False: Inactivo)"),
):
    """
    Endpoint para consultar todos los proveedores por estado.
    Se proporciona el parámetro `estado` para obtener proveedores activos o inactivos.
    """
    try:
        # Ver todos los proveedores según el estado
        proveedor = Proveedor()
        response = await proveedor.verTodosLosProveedores(estado)
        return {"data": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/proveedor",tags=["Proveedores"])
async def gestion_proveedor(request: Proveedor_request):
    """
    Endpoint para gestion provedores.
    Soporta las acciones: 
    - 'verTodosLosProveedores': 
   

    - 'cambiarEstado': Cambia de estado solo acepta true o false.
         ```Jsoon

        {
            "accion": "cambiarEstado",
            "id_proveedor": 1,
            "estado": false
        }
        ```
    - 'agregarProveedor': Agregar un nuevo Proveedor.
         ```Jsoon
        {        
        "accion": "agregarProveedor",
        "nombre": "Nuevo prove",
        "direccion": "el picaflor sn",
        "telefono": "1168462777",
        "correo_contacto": "nuevoProveeeeee@provee"
        }
        
        ```    
    
    - 'editarProveedor' : Editar un Proveedor por ID.

        ```Jsoon
            {
            "accion": "editarProveedor",
            "id_proveedor": 8,
            "nombre": "aaaaaa",
            "direccion":"aaaaaaaaaa",
            "telefono":" 5555555555555",
            "correo_contacto": "aaaaaaaa@AAAAAA.com"
            }
        
        ```
    
    - 'en caso de error al editar devuelve':

        ```Jsoon
            {
            "status": "warning",
            "message": "No se realizaron cambios, ya que los valores proporcionados son los mismos."
            }
        ```

    """
    try:
# Agregar nuevo proveedor
        if request.accion == "agregarProveedor":
            if not all([request.nombre, request.direccion,  request.telefono, request.correo_contacto]):
                raise HTTPException(
                    status_code=400,
                    detail="Todos los parámetros 'nombre', 'direccion', 'telefono', 'correo_contacto'."
                )
            proveedor = Proveedor()
            response = await proveedor.agregarProveedor(               
            request.nombre,       
            request.direccion,    
            request.telefono,     
            request.correo_contacto 
            )
            return response

        # Eliminar proveedor
        elif request.accion == "eliminarProveedor":
            if request.id_proveedor is None:
                raise HTTPException(
                    status_code=400,
                    detail="El parámetro 'id_proveedor' es requerido para esta acción."
                )
            proveedor = Proveedor()
            response = await proveedor.eliminarProveedor(request.id_proveedor)
            return response

# Editar proveedor
        elif request.accion == "editarProveedor":
            print("entro a editar")
            if request.id_proveedor is None:
                raise HTTPException(
                    status_code=400,
                    detail="El parámetro 'id_proveedor' es requerido para esta acción."
                )
            
# Asegurarse de que los parámetros a editar estén definidos, si se requieren.
            if not any([request.nombre, request.direccion, request.telefono, request.correo_contacto]):
                raise HTTPException(
                    status_code=400,
                    detail="Al menos uno de los parámetros 'nombre', 'direccion', 'telefono', 'correo_contacto' debe ser proporcionado para editar."
                )

            proveedor = Proveedor()
            response = await proveedor.editarProveedor(
                request.id_proveedor,  # El ID del proveedor que se va a editar
                request.nombre,        # El nuevo nombre, si se proporciona
                request.direccion,     # La nueva dirección, si se proporciona
                request.telefono,      # El nuevo teléfono, si se proporciona
                request.correo_contacto  # El nuevo correo, si se proporciona
            )
            return response
        
                # Cambiar estado del proveedor
        elif request.accion == "cambiarEstado":
            if request.id_proveedor is None or request.estado is None:
                raise HTTPException(
                    status_code=400,
                    detail="Los parámetros 'id_proveedor' y 'estado' son requeridos para esta acción."
                )
            proveedor = Proveedor(id_proveedor=request.id_proveedor)
            response = await proveedor.cambiar_estado(request.estado)
            return response
                

        else:
            # Acción no válida
            raise HTTPException(
                status_code=400,
                detail="Acción no válida. Las acciones soportadas son: 'verTodosLosProveedores', 'agregarProveedor', 'eliminarProveedor'."
            )
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(status_code=500, detail=str(e))
    


###############################producto_categoria############################################################################################

# GET endpoint para ver todas las categorías
@router.get("/productos_categorias",tags=["Producto Categoria"])
async def ver_todas_las_categorias(
    estado: bool = Query(..., description="Estado de categorías inactivas.TRUE = activas FALSE = inactiva"),
):
    """
    Endpoint para consultar todas las categorías.
    Se proporciona el parámetro `estado` para incluir categorías activas o inactivas.
    """
    try:
        categoria = ProductoCategoria()
        resultado = await categoria.ver_todas_categorias(estado)
        return {"status": "success", "data": resultado}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#POST
    
@router.post("/producto_categoria",tags=["Producto Categoria"])
async def producto_categoria(request: Categoria_request):
    """
    Endpoint para gestion categorías de productos.
    Soporta las acciones:    

    - 'agregarCategoria': Agregar una nueva categoría.
        ```json

            {
            "accion": "agregarCategoria",
            "descripcion": "Electrodomésticos",
            "estado": true
            }
        ```


    - 'modificarCategoria': Modificar una categoría existente.
        ```json

            {
            "accion": "modificarCategoria",
            "id_categoria": 1,
            "descripcion": "Electrónicssssa"
            }

            {
            "accion": "modificarCategoria",
            "id_categoria": 1,
            "estado": false
            }

            {
            "accion": "modificarCategoria",
            "id_categoria": 1,
            "descripcion": "Electrónica avanzada",
            "estado": true
            }

        ```
    - 'eliminarCategoria': Eliminar (soft delete) una categoría.
        ```json

            {
            "accion": "eliminarCategoria",
            "id_categoria": 1
            }
        ```


    """
    try:
        categoria = ProductoCategoria()
        
        # Agregar una nueva categoría
        if request.accion == "agregarCategoria":
            if not request.descripcion:
                raise HTTPException(status_code=400, detail="El campo 'descripcion' es requerido.")
            resultado = await categoria.agregar_categoria(request.descripcion, request.estado)
            return resultado

        # Modificar una categoría existente
        elif request.accion == "modificarCategoria":
            if not request.id_categoria:
                raise HTTPException(status_code=400, detail="El campo 'id_categoria' es requerido.")
            if not (request.descripcion or request.estado is not None):
                raise HTTPException(status_code=400, detail="Debe proporcionar 'descripcion' o 'estado' para modificar.")
            resultado = await categoria.modificar_categoria(request.id_categoria, request.descripcion, request.estado)
            return resultado

        # Eliminar una categoría (soft delete)
        elif request.accion == "eliminarCategoria":
            if not request.id_categoria:
                raise HTTPException(status_code=400, detail="El campo 'id_categoria' es requerido.")
            resultado = await categoria.eliminar_categoria(request.id_categoria)
            return resultado

        else:
            # Acción no válida
            raise HTTPException(status_code=400, detail="Acción no válida. Verifique la documentación.")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    








    ####################################marca#####################################################################

# GET endpoint para ver todas las marcas
@router.get("/producto_marcas",tags=["Producto Marca"])
async def ver_todas_las_marcas(
    estado: bool = Query(..., description="TRUE = activa FALSE = inactivas"),
):
    """
    Endpoint para consultar todas las marcas.
    Se proporciona el parámetro `estado` TRUE = activa FALSE = inactivas.
    """
    try:
        marca = ProductoMarca()
        resultado = await marca.ver_todas_marcas(estado)
        return {"status": "success", "data": resultado}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#POST


@router.post("/producto_marca",tags=["Producto Marca"])
async def producto_marca(request: Marca_request):
    """
    Endpoint para gestion marcas de productos.
    Soporta las acciones:

    - 'agregarMarcas': Agregar una nueva marca.
        ```json

            {
            "accion": "agregarMarca",
            "descripcion": "Coca Cola",
            "estado": true
            }
        ```


    - 'modificarMarca': Modificar una marca existente.
        ```json

            {
            "accion": "modificarMarca",
            "id_marca": 1,
            "descripcion": "Electrónicssssa"
            }

            {
            "accion": "modificarMarca",
            "id_marca": 1,
            "estado": false
            }

            {
            "accion": "modificarMarca",
            "id_marca": 1,
            "descripcion": "Electrónica avanzada",
            "estado": true
            }

        ```
    - 'eliminarMarca': Eliminar (soft delete) una marca.
        ```json

            {
            "accion": "eliminarMarca",
            "id_marca": 1
            }
        ```
    """
    try:
        marca = ProductoMarca()
        
        # Agregar una nueva marca
        if request.accion == "agregarMarca":
            if not request.descripcion:
                raise HTTPException(status_code=400, detail="El campo 'descripcion' es requerido.")
            resultado = await marca.agregar_marca(request.descripcion, request.estado)
            return resultado

        # Modificar una marca existente
        elif request.accion == "modificarMarca":
            if not request.id_marca:
                raise HTTPException(status_code=400, detail="El campo 'id_marca' es requerido.")
            if not (request.descripcion or request.estado is not None):
                raise HTTPException(status_code=400, detail="Debe proporcionar 'descripcion' o 'estado' para modificar.")
            resultado = await marca.modificar_marca(request.id_marca, request.descripcion, request.estado)
            return resultado

        # Eliminar una marca (soft delete)
        elif request.accion == "eliminarMarca":
            if not request.id_marca:
                raise HTTPException(status_code=400, detail="El campo 'id_marca' es requerido.")
            resultado = await marca.eliminar_marca(request.id_marca)
            return resultado

        else:
            # Acción no válida
            raise HTTPException(status_code=400, detail="Acción no válida. Verifique la documentación.")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    



############################Movimiento_stock#######################################################################
# Definir operaciones válidas al inicio del archivo
OPERACIONES_VALIDAS = [
    "Entrada",
    "Salida por venta",
    "Salida por devolución",
    "Salida por producto dañado o vencido"
]

@router.post("/movimiento_stock",tags=["Movimiento de stock y Tipo de Movimiento para el stock"])
async def movimiento_stock(request: movimientoStockRequest):
    """
    Procesa múltiples movimientos de stock en una sola transacción.

    ### Ejemplo de Payload de Entrada:
    ```json
    {
        "movimientos": [
            {
                "id_producto": 1,
                "cantidad": 10,
                "id_tipo_movimiento": 1,
                "id_usuario": 123,
                "id_proveedor": 5,
                "id_almacen": 2,
                "id_estante": 1,
                "precio_costo_ars":110,
                "precio_costo_usd":10,
                "descripcion": "Recepción de mercancía"
            },
            {
                "id_producto": 2,
                "cantidad": 5,
                "id_tipo_movimiento": 2,
                "id_usuario": 123,
                "id_proveedor": 5,
                "id_almacen": 2,
                "id_estante": 1,
                "descripcion": "Venta de producto"
            }
        ]
    }

        {
        "movimientos": [
            {
                "id_producto": 1,
                "cantidad": 10,
                "id_tipo_movimiento": 2,
                "id_usuario": 123,
                "id_proveedor": 10,
                "id_almacen": 2,
                "id_estante": 1,
                "descripcion": "Venta de 10 unidades del producto 1"
            }
        ]
    }
    ```

    ### Consideraciones:
    - Si el proveedor cambia, se crea un nuevo stock si es relevante para la gestión del inventario.
    - Si el almacén o el estante cambia, solo se registra un movimiento sin crear un nuevo stock, ya que solo se está cambiando la ubicación del producto.

    Args:
    - productos: Lista de productos involucrados en el movimiento.
    - id_usuario: ID del usuario que realiza el movimiento.
    - id_proveedor: ID del proveedor (puede cambiar).
    - id_almacen: ID del almacén (puede cambiar).
    - id_estante: ID del estante (puede cambiar).
    - descripcion: Descripción del movimiento (por ejemplo, "Recepción de mercancía").
    - id_tipo_movimiento: ID del tipo de movimiento (por ejemplo, entrada o salida).
    - identificador_evento: Identificador global del evento, si es proporcionado.

    Returns:
    - Respuesta con el resultado del movimiento.
    """
    resultados = []
    stock = Stock()
    identificador_evento_global = None

    for movimiento in request.movimientos:
        try:
            # Validar que el id_tipo_movimiento esté activo antes de procesar
            await stock.obtener_estado_tipo_movimiento(movimiento.id_tipo_movimiento)

            # Ejecutar el procedimiento adecuado según el tipo de movimiento
            resultado = await stock.procesar_movimiento_stock(
                productos=[{"id_producto": movimiento.id_producto, "cantidad": movimiento.cantidad}],
                id_usuario=movimiento.id_usuario,
                id_proveedor=movimiento.id_proveedor,
                id_almacen=movimiento.id_almacen,
                id_estante=movimiento.id_estante,
                precio_costo_ars=movimiento.precio_costo_ars,
                precio_costo_usd=movimiento.precio_costo_usd,

                descripcion=movimiento.descripcion,
                id_tipo_movimiento=movimiento.id_tipo_movimiento,
                identificador_evento=identificador_evento_global
            )

            # Si es el primer movimiento, establecemos el identificador global
            if identificador_evento_global is None:
                identificador_evento_global = resultado["identificador_evento"]

            resultados.append({
                "id_producto": movimiento.id_producto,
                "status": "success",
                "mensaje": resultado["mensaje"],
                "identificador_evento": resultado["identificador_evento"]
            })

        except HTTPException as e:
            resultados.append({
                "id_producto": movimiento.id_producto,
                "status": "error",
                "mensaje": str(e.detail)
            })
        except Exception as e:
            resultados.append({
                "id_producto": movimiento.id_producto,
                "status": "error",
                "mensaje": f"Error interno: {str(e)}"
            })

    return {"resultados": resultados}

# ----------------------------- Tipo de Movimiento ----------------------------- #

# GET endpoint para ver todos los tipos de movimientos de stock 
@router.get("/tipo_movimiento_stock",tags=["Movimiento de stock y Tipo de Movimiento para el stock"])
async def ver_tipo_movimiento_stock(
    estado: bool = Query(..., description="Estado de tipo de movimientos .TRUE = activas FALSE = inactiva"),
):
    """
    Endpoint para consultar todas los estantes de un almacen especifico.
    Se proporciona el parámetro `estado` para incluir categorías activas o inactivas.
    """
    try:
        sotck = Stock()
        resultado = await sotck.verTodosLosTiposMovimientos(estado)
        
        return {"status": "success", "data": resultado}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

###########################Almacen#################################################

# GET endpoint para ver todas los almacenes
@router.get("/almacen",tags=["Almacenes y Estantes"])
async def ver_todas_las_categorias(
    estado: bool = Query(..., description="Estado de almacen.TRUE = activas FALSE = inactiva"),
):
    """
    Endpoint para consultar todas las categorías.
    Se proporciona el parámetro `estado` para incluir categorías activas o inactivas.
    """
    try:
        almacen = Almacen()
        resultado = await almacen.verTodosLosAlmacenes(estado)
        
        return {"status": "success", "data": resultado}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#post

@router.post("/almacen",tags=["Almacenes y Estantes"])
async def gestion_almacen(request: Almacen_request):
    """
    Endpoint para gestion almacen.
    Soporta las acciones: 
    

    - 'cambiarEstado': Cambia de estado solo acepta true o false.
         ```Jsoon

        {
            "accion": "cambiarEstado",
            "id_almacen": 1,
            "estado": false
        }
        ```
    - 'agregarAlmacen': Agregar un nuevo Almacen.
         ```Jsoon
        {        
        "accion": "agregarAlmacen",
        "descripcion": "almcaen 2"
        
        }
        
        ```    
    
    - 'editarAlmacen' : Editar un Almacen por ID.

        ```Jsoon
            {
            "accion": "editarAlmacen",
            "id_almacen": 8,
            "descripcion": "aaaaaa"
            }
        
        ```
    
    - 'en caso de error al editar devuelve':

        ```Jsoon
            {
            "status": "warning",
            "message": "No se realizaron cambios, ya que los valores proporcionados son los mismos."
            }
        ```

    """
    try:
# Agregar nuevo almacen
        if request.accion == "agregarAlmacen":
            if not all([request.descripcion]):
                raise HTTPException(
                    status_code=400,
                    detail="Todos los parámetros 'descripcion'son requeridos."
                )
            almacen = Almacen()
            response = await almacen.agregarAlmacen(               
            request.descripcion
            )
            return response
# Eliminar almacen
        elif request.accion == "eliminarAlmacen":
            if request.id_almacen is None:
                raise HTTPException(
                    status_code=400,
                    detail="El parámetro 'id_almacen' es requerido para esta acción."
                )
            almacen = Almacen()
            response = await almacen.eliminarAlmacen(request.id_almacen)
            return response

# Editar almacen
        elif request.accion == "editarAlmacen":
            if request.id_almacen is None:
                raise HTTPException(
                    status_code=400,
                    detail="El parámetro 'id_almacen' es requerido para esta acción."
                )
            
# Asegurarse de que los parámetros a editar estén definidos, si se requieren.
            if not any([request.descripcion]):
                raise HTTPException(
                    status_code=400,
                    detail="Al menos uno de los parámetros  'descripcion' debe ser proporcionado para editar."
                )

            almacen = Almacen()
            response = await almacen.editaralmacen(
                request.id_almacen,  # El ID del almacen que se va a editar
                request.descripcion  # El nuevo correo, si se proporciona
            )
            return response
        
        # Cambiar estado del almacen
        elif request.accion == "cambiarEstado":
            if request.id_almacen is None or request.estado is None:
                raise HTTPException(
                    status_code=400,
                    detail="Los parámetros 'id_almacen' y 'estado' son requeridos para esta acción."
                )
            almacen = Almacen(id_almacen=request.id_almacen)
            response = await almacen.cambiar_estado(request.estado)
            return response
                

        else:
            # Acción no válida
            raise HTTPException(
                status_code=400,
                detail="Acción no válida. Las acciones soportadas son: 'verTodosLosAlmacenes', 'agregarAlmacen', 'eliminarEstante'."
            )
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(status_code=500, detail=str(e))
    

###################################almacen_estante###################################

# GET endpoint para ver todas los estantes que tienen los almacenes
@router.get("/almacen_estante",tags=["Almacenes y Estantes"])
async def ver_todas_las_categorias(
    id_almacen: int = Query(..., id_almacen="Estado de almacen_estante .TRUE = activas FALSE = inactiva"),
    estado: bool = Query(..., description="Estado de almacen_estante .TRUE = activas FALSE = inactiva"),
):
    """
    Endpoint para consultar todas los estantes de un almacen especifico.
    Se proporciona el parámetro `estado` para incluir categorías activas o inactivas.
    """
    try:
        estante = Estante()
        resultado = await estante.verTodosLosestantes(id_almacen,estado)
        
        return {"status": "success", "data": resultado}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/almacen_estante",tags=["Almacenes y Estantes"])
async def gestion_almacen_estante(request: Estante_request):
    """
    Endpoint para gestion estante.
    Soporta las acciones: 
    
    - 'cambiarEstado': Cambia de estado solo acepta true o false.
         ```Jsoon

        {
            "accion": "cambiarEstado",
            "id_estante": 1,
            "estado": false
        }
        ```
    - 'agregarEstante': Agregar un nuevo Estante.
         ```Jsoon
        {        
        "accion": "agregarEstante",
        "id_almacen":1,
        "descripcion": "estante 2"
        
        }
        
        ```    
    
    - 'editarEstante' : Editar un Estante por ID.

        ```Jsoon
            {
            "accion": "editarEstante",
            "id_estante": 8,
            "descripcion": "aaaaaa"
            }
        
        ```
    
    - 'en caso de error al editar devuelve':

        ```Jsoon
            {
            "status": "warning",
            "message": "No se realizaron cambios, ya que los valores proporcionados son los mismos."
            }
        ```

    """
    try:

# Agregar nuevo estante
        if request.accion == "agregarEstante":
            if not all([request.descripcion]):
                raise HTTPException(
                    status_code=400,
                    detail="Todos los parámetros 'id_almacen', 'descripcion'son requeridos."
                )
            estante = Estante()
            response = await estante.agregarEstante( 
            request.id_almacen,              
            request.descripcion
            )
            return response
# Eliminar estante
        elif request.accion == "eliminarEstante":
            if request.id_estante is None:
                raise HTTPException(
                    status_code=400,
                    detail="El parámetro 'id_estante' es requerido para esta acción."
                )
            estante = Estante()
            response = await estante.eliminarEstante(request.id_estante)
            return response

# Editar estante
        elif request.accion == "editarEstante":
            if request.id_estante is None:
                raise HTTPException(
                    status_code=400,
                    detail="El parámetro 'id_estante' es requerido para esta acción."
                )
            
# Asegurarse de que los parámetros a editar estén definidos, si se requieren.
            if not any([request.descripcion]):
                raise HTTPException(
                    status_code=400,
                    detail="Al menos uno de los parámetros  'descripcion' debe ser proporcionado para editar."
                )

            estante = Estante()
            response = await estante.editarEstante(
                request.id_estante,  # El ID del estante que se va a editar
                request.descripcion  # El nuevo correo, si se proporciona
            )
            return response
        
        # Cambiar estado del estante
        elif request.accion == "cambiarEstado":
            if request.id_estante is None or request.estado is None:
                raise HTTPException(
                    status_code=400,
                    detail="Los parámetros 'id_estante' y 'estado' son requeridos para esta acción."
                )
            estante = Estante(id_estante=request.id_estante)
            response = await estante.cambiar_estado(request.estado)
            return response
                

        else:
            # Acción no válida
            raise HTTPException(
                status_code=400,
                detail="Acción no válida. Las acciones soportadas son: 'verTodosLosEstantes', 'agregarEstante', 'eliminarEstante'."
            )
    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(status_code=500, detail=str(e))
    

############################stock#######################################################################
##@router.post("/tabla_stock", response_model=List[StockResponse])
@router.get("/inventario", response_model=List[Dict[str, Any]],tags=["Inventario"])
async def inventario(
    id_producto: int = Query(None, description="ID del producto a filtrar (opcional)"),
    id_almacen: int = Query(None, description="ID del almacén a filtrar (opcional)"),
    estado: str = Query(None, description="Estado del stock a filtrar (opcional)"),
    codigo_barras: str = Query(None, description="Código de barras del producto (opcional)"),
    nombre: str = Query(None, description="Nombre del producto o parte del nombre (opcional)"),
):
    """
    Endpoint para consultar la tabla 'stock'. Si no se pasan filtros, devuelve todos los registros.
    
    Parámetros de consulta:
    - `id_producto`: ID del producto (opcional).
    - `id_almacen`: ID del almacén (opcional).
    - `estado`: Estado del stock (opcional).
    - `codigo_barras`: Código de barras del producto (opcional).
    - `nombre`: Parte del nombre del producto (opcional).

    Ejemplo:
    - `/inventario` -> Devuelve todo el stock.
    - `/inventario?id_producto=1` -> Filtra por producto.
    - `/inventario?codigo_barras=123456789` -> Filtra por código de barras.
    - `/inventario?nombre=zap` -> Busca productos cuyo nombre contenga "zap".
    """
    stock = Stock()  # Instancia de la clase Stock
    try:
        resultados = await stock.inventario(
            id_producto=id_producto,
            id_almacen=id_almacen,
            estado=estado,
            codigo_barras=codigo_barras,
            nombre=nombre
        )
        return resultados
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")



############################stock_movimientos_endpoints#######################################################################


@router.get("/tabla_consulta_stock_movimientos", response_model=List[Dict[str, Any]],tags=["Tabla de movimientos de stock/inventario"])
async def consultar_movimientos(
    id_producto: Optional[int] = Query(None, description="ID del producto a filtrar (opcional)"),
    id_usuario: Optional[int] = Query(None, description="ID del usuario a filtrar (opcional)"),
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio para filtrar movimientos (opcional, formato: YYYY-MM-DD)"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin para filtrar movimientos (opcional, formato: YYYY-MM-DD)"),
    id_tipo_movimiento: Optional[int] = Query(None, description="ID del tipo de movimiento a filtrar (opcional)"),
):
    """
    Endpoint para consultar la tabla 'stock_movimientos' con filtros opcionales.

    Parámetros de consulta:
    - `id_producto`: Filtrar por ID del producto.
    - `id_usuario`: Filtrar por ID del usuario que realizó el movimiento.
    - `fecha_inicio`: Filtrar movimientos desde esta fecha (inclusive).
    - `fecha_fin`: Filtrar movimientos hasta esta fecha (inclusive).
    - `id_tipo_movimiento`: Filtrar por ID del tipo de movimiento.

    Si no se pasan filtros, devuelve todos los movimientos de stock.
    """
    stock = Stock()  # Instancia de la clase Stock
    try:
        resultados = await stock.obtener_movimientos(
            id_producto=id_producto,
            id_usuario=id_usuario,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            id_tipo_movimiento=id_tipo_movimiento,
        )
        return resultados
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


############################Panel de configuracionde precios#######################################################################


@router.get("/configuracion/precios",tags=["Panel configuracion precios"])
async def obtener_configuracion():
    producto=Producto()
    """Devuelve la configuración actual de precios."""
    resultado = await producto.obtener_configuracion()
    return resultado


@router.post("/configuracion/precios_ars", tags=["Panel configuración precios"])
async def actualizar_configuracion_ars(permitir_precio_menor_costo_ars: bool,
    ajuste_precio_porcentaje_ars: float,):
    """Actualiza la configuración de precios."""
    producto = Producto()
    resultado = await producto.actualizar_configuracion_ars(
        permitir_precio_menor_costo_ars,
        ajuste_precio_porcentaje_ars)
    return resultado


@router.post("/configuracion/precios_usd", tags=["Panel configuración precios"])
async def actualizar_configuracion_usd(permitir_precio_menor_costo_usd: bool,
    ajuste_precio_porcentaje_usd: float):
    """Actualiza la configuración de precios."""
    producto = Producto()
    resultado = await producto.actualizar_configuracion_usd(
         permitir_precio_menor_costo_usd,
         ajuste_precio_porcentaje_usd)
    return resultado


@router.post("/configuracion/aplicar_precios_ars", tags=["Panel configuración precios"])
async def aplicar_precios_ars():
    """Aplica los cambios de precios en ARS según la configuración."""
    producto = Producto()
    resultado = await producto.ajustar_precios_ars()
    return resultado


@router.post("/configuracion/aplicar_precios_usd", tags=["Panel configuración precios"])
async def aplicar_precios_usd():
    """Aplica los cambios de precios en USD según la configuración."""
    producto = Producto()
    resultado = await producto.ajustar_precios_usd()
    return resultado


@router.post("/configuracion/convertir_precios", tags=["Conversión de precios"])
async def convertir_precios_dolares(valor_dolar: float):
    """Convierte los precios de los productos en dólares a pesos argentinos según el valor del dólar."""
    producto = Producto()
    resultado = await producto.convertir_precios_dolares(valor_dolar)
    return resultado

    