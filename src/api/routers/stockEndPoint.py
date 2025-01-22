from fastapi import APIRouter, HTTPException, UploadFile, File, Form,Query  # Importa APIRouter para crear grupos de rutas y HTTPException para gestion errores.
from fastapi.responses import JSONResponse, Response  # Importa JSONResponse para devolver respuestas JSON personalizadas.
from pydantic import BaseModel  # Importa BaseModel para definir esquemas de solicitudes y respuestas.
from typing import List,Optional,Dict, Any


#importa las clases
from models.producto import Producto # Importa Clase Producto
from models.proveedor import Proveedor # Importa Clase Proveedor
from models.almacen import Almacen # Importa Clase Almacen
from models.almacen_estante import Estante # Importa Clase Almacen

from models.producto_categoria import ProductoCategoria # Importa Clase productocategoria
from models.producto_marca import ProductoMarca # Importa Clase productocategoria

from models.stock import Stock


from models.login import Login,create_jwt_token
#importa los schemas
from schemas import TodosLosUsuarios_request, UsuarioLogin_request,Usuario_request,Producto_request,Proveedor_request,Categoria_request,Stock_request, Stock_response,Marca_request,MovimientoStock,Almacen_request,Estante_request,Stock_request,StockResponse,MovimientoStockResponse,FiltrosStock

import logging
import json
import os
import subprocess
import calendar
from datetime import datetime
#from fastapi.responses import FileResponse

  
import psycopg2
from psycopg2.extras import DictCursor
import random
import string



logger = logging.getLogger(__name__)
# Crea un enrutador para agrupar las rutas relacionadas con recibos.
router = APIRouter()
################################################################################################

""" # Ruta para obtener todos los recibos
@router.post('/todosLosPecibos', response_model=TodosLosRecibos_response)
async def todosLosRecibos(request: TodosLosRecibos_request):
    cuil = request.cuil  # Obtiene el CUIL de la solicitud.    
    if not cuil:  # Verifica si el CUIL está presente en la solicitud.
        raise HTTPException(status_code=400, detail="Parámetros 'cuil' faltan.")  # Lanza una excepción si falta el CUIL.    
    try:
        recibos = Recibo()  # Crea una instancia de la clase TodosLosRecibos.
        response = await recibos.todosLosRecibos(cuil)  # Llama al método para obtener todos los recibos.        
        if response is None:  # Verifica si la respuesta es válida.
            raise HTTPException(status_code=500, detail="Error al cargar los datos en la tabla de recibos.")  # Lanza una excepción si la carga falla.
        if not response:  # Verifica si hay recibos disponibles para el CUIL proporcionado.
            raise HTTPException(status_code=404, detail="No se encontraron recibos para el CUIL proporcionado.")  # Lanza una excepción si no se encuentran recibos.        
        # Construye la respuesta JSON, formateando fechas adecuadamente.
        descripciones = [{
            "id_recibo": recibo["id_recibo"],
            "periodo": recibo["periodo"],
            "fecha_subida": recibo["fecha_subida"].strftime("%d/%m/%Y") if isinstance(recibo["fecha_subida"], datetime) else recibo["fecha_subida"],
            "descripcion_archivo": recibo["descripcion_archivo"],
            "estado": recibo["estado"]
        } for recibo in response]        
        # Devuelve una respuesta exitosa con la lista de objetos JSON.
        return JSONResponse(content=descripciones)
    except Exception as e:  # Maneja cualquier excepción ocurrida durante el proceso.
        print(f"Error en todosLosRecibos: {e}")  # Imprime el error para depuración.
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")  # Lanza una excepción con el mensaje de error. """

################################################################################################

# Ruta para obtener todos los recibos
""" @router.post('/todosLosUsuarios', response_model=TodosLosUsuarios_response)
async def todosLosUsuarios(request: TodosLosUsuarios_request):
    cuil = request.cuil  # Obtiene el CUIL de la solicitud.   
    if not cuil:  # Verifica si el CUIL está presente en la solicitud.
        raise HTTPException(status_code=400, detail="Parámetros 'cuil' faltan.")  # Lanza una excepción si falta el CUIL.
    
    try:
        todosLosUsuarios = TodosLosUsuarios()  # Crea una instancia de la clase TodosLosRecibos.
        response = await todosLosUsuarios.todosLosUsuarios(cuil)  # Llama al método para obtener todos los recibos.
        if response is None:  # Verifica si la respuesta es válida.
            raise HTTPException(status_code=500, detail="Error al cargar los datos en la tabla de recibos.")  # Lanza una excepción si la carga falla.
        if not response:  # Verifica si hay recibos disponibles para el CUIL proporcionado.
            raise HTTPException(status_code=404, detail="No se encontraron recibos para el CUIL proporcionado.")  # Lanza una excepción si no se encuentran recibos.
        if response == "No tiene permisos":  # Verifica si hay recibos disponibles para el CUIL proporcionado.
            raise HTTPException(status_code=404, detail="No tiene los permisos necesarios para ver esta informacion")  # Lanza una excepción si no se encuentran recibos.
        # Construye la respuesta JSON, formateando fechas adecuadamente.
        descripciones = [{
            "id_usuario": usuario["id_usuario"],
            "nombre": usuario["nombre"],
            "apellido": usuario["apellido"],
            "legajo": usuario["legajo"],
            "email": usuario["email"],
            "cuil": usuario["cuil"]
        } for usuario in response]
        
        # Devuelve una respuesta exitosa con la lista de objetos JSON.
        return JSONResponse(content=descripciones)

    except Exception as e:  # Maneja cualquier excepción ocurrida durante el proceso.
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")  # Lanza una excepción con el mensaje de error. """

################################################################################################

@router.post("/producto")
async def producto(request: Producto_request):
    """
    Endpoint para gestion productos.
    Soporta las acciones: 

    - **verTodosLosProductos**: Ver todos los productos según su estado.
      ```json
      {
          "accion": "verTodosLosProductos",
          "estado": "Activo"
      }
      ```

    - **agregarProducto**: Agregar un nuevo producto.
        ```json
            
        
            {
            "accion": "agregarProducto",
            "id_marca": 1,
            "nombre": "Zapatillas Air Max 2024",
            "descripcion": "Zapatillas deportivas de alta calidad, edición 2024",
            "precio": 150.75,
            "codigo_barras": "1234567890123aaa",
            "id_categoria": 1,
            "imagen_producto": "https://drive.google.com/uc?id=ID_DE_TU_IMAGEN",
            "forceAdd": false
            }
        
        ```

    - **eliminarProducto**: Eliminar un producto por ID.
    
        ```json
            
        {
        "accion": "eliminarProducto",
        "id_producto": 29
        }
        ```
    

    - **buscarPorCodigoDeBarras**: Búsqueda rápida por código de barras.

    """
    try:
        
# Ver todos los productos
        if request.accion == "verTodosLosProductos":
            if request.estado is None:
                raise HTTPException(
                    status_code=400, detail="El parámetro 'estado' es requerido para esta acción."
                )
            producto = Producto()
            response = await producto.verTodosLosProductos(request.estado)
            return {"data": response}
        
# Buscar producto por código de barras
        elif request.accion == "buscarPorCodigoDeBarras":
            if not request.codigo_barras:
                raise HTTPException(
                    status_code=400, detail="El parámetro 'codigo_barras' es requerido para esta acción."
                )
                
           
            producto = Producto()
            response = await producto.buscarPorCodigoDeBarras(request.codigo_barras)
            if not response:
                raise HTTPException(
                status_code=404, detail="Producto no encontrado con el código de barras proporcionado."
                )
            return {"data": response}

# Agregar nuevo producto 
        
        elif request.accion == "agregarProducto":
                
            """
            Endpoint que maneja la solicitud de agregar un producto.
            Verifica si ya existe un producto con el mismo código de barras y maneja el caso de forceAdd.
            """
                    # Verificar parámetros requeridos
            if not all([request.id_marca, request.nombre, request.descripcion, request.precio, request.codigo_barras,request.id_categoria]):
                raise HTTPException(
                    status_code=400,
                    detail="Los parámetros 'id_marca', 'nombre', 'descripcion', 'precio', 'codigo_barras' y  'id_categoria'son requeridos."
                )
            # Crear instancia de Producto
            producto = Producto()
            # Llamar al método agregar_producto
            response = await producto.agregar_producto(
                id_marca=request.id_marca,
                nombre=request.nombre,
                descripcion=request.descripcion,
                precio=request.precio,
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
            if not all([request.id_marca, request.nombre, request.descripcion, request.precio, request.codigo_barras,request.id_categoria]):
                raise HTTPException(
                    status_code=400,
                    detail="Los parámetros 'id_marca', 'nombre', 'descripcion', 'precio', 'codigo_barras' y  'id_categoria'son requeridos."
                )
            # Crear instancia de Producto
            producto = Producto()
            # Llamar al método agregar_producto
            response = await producto.editarProducto(
                request.id_producto,
                request.id_marca,
                request.nombre, 
                request.descripcion, 
                request.precio, 
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
                detail="Acción no válida. Las acciones soportadas son: 'verTodosLosProductos', 'agregarProducto', 'eliminarProducto'."
            )

    except Exception as e:
        # Manejo de errores inesperados
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
######################/login##########################################################

@router.post("/login")        
async def login(usuario: UsuarioLogin_request, response: Response):
    """
    Endpoint login
    ```json
        {
        "cuil": "string",
        "password": "string"
        }
    ```

    """
    resultado = await Login.login_usuario(usuario.cuil, usuario.password)    
    # Verificamos si el resultado es un diccionario
    if isinstance(resultado, dict):
        # Manejo de los distintos casos devueltos
        if "code" in resultado:
            if resultado["code"] == 0:
                raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
            elif resultado["code"] == 50:
                raise HTTPException(status_code=403, detail="Usuario deshabilitado")        
        # Autenticación exitosa
        id_usuario = resultado["id_usuario"]
        cuil = resultado["cuil"]  # Asegúrate de que el CUIL se esté retornando correctamente
        rol = resultado["rol"]        
        nombre = resultado["nombre"]
        apellido = resultado["apellido"]
        email = resultado["email"]                           
        auth_token = create_jwt_token(id_usuario, rol, cuil)  # Genera el token con el ID, rol y CUIL del usuario
        # Establece el token en la cabecera Set-Cookie
        response.set_cookie(key="auth_token", value=auth_token, httponly=True)  # Cambia httponly=True según tus necesidades
        # Devuelve la respuesta con el CUIL y el auth_token
        return {
            "cuil": cuil,
            "rol": rol,
            "auth_token": auth_token,
            "nombre": nombre,
            "apellido":apellido,
            "email":email
        }    
    # Si el resultado no es un diccionario, lanza un error de servidor
    raise HTTPException(status_code=500, detail="Error en la respuesta del servidor, no se pudo autenticar.")

################################################################################################

# @router.post("/usuarios", response_model=dict)
# async def gestionar_usuario(usuario_data: Usuario_request):
#     print("entro a usuario")
#     try:
#         if usuario_data.accion == "insert":
#             # Acción para crear un nuevo usuario
#             usuario = Usuario()  # Crear la instancia de Usuario
#             response = await usuario.insert(
#                 nombre=usuario_data.nombre,
#                 apellido=usuario_data.apellido,
#                 cuil=usuario_data.cuil,
#                 legajo=usuario_data.legajo,
#                 email=usuario_data.email,
#                 habilitado=usuario_data.habilitado if usuario_data.habilitado is not None else 1  # Activado por defecto
#             )
#             return {
#                 "data": response  # Aquí asignas una clave "data" al valor correspondiente
#             }
        
#         elif usuario_data.accion == "update":
#             # Acción para modificar un usuario existente
#             if not usuario_data.id_usuario:
#                 raise HTTPException(status_code=400, detail="Se requiere el ID del usuario para actualizar.")
#             usuario = Usuario(id_usuario=usuario_data.id_usuario)  # Cargar la instancia del usuario con su ID
#             response = await usuario.update(
#                 nombre=usuario_data.nombre,
#                 apellido=usuario_data.apellido,
#                 cuil=usuario_data.cuil,
#                 legajo=usuario_data.legajo,
#                 email=usuario_data.email
#             )
#             return {
#                 "data": response  # Aquí asignas una clave "data" al valor correspondiente
#             }
#         elif usuario_data.accion == "resetPassword":
#             # Acción para modificar un usuario existente
#             if not usuario_data.id_usuario:
#                 raise HTTPException(status_code=400, detail="Se requiere el ID del usuario para reestablecer la contraseña.")
#             usuario = Usuario(id_usuario=usuario_data.id_usuario)  # Cargar la instancia del usuario con su ID
#             response = await usuario.resetPassword()
#             return {
#                 "data": response  # Aquí asignas una clave "data" al valor correspondiente
#             }
#         elif usuario_data.accion == "newPassword":
#             print("entro a newPassword")
#             # Acción para modificar un usuario existente
#             if not usuario_data.id_usuario:
#                 raise HTTPException(status_code=400, detail="Se requiere el ID del usuario para reestablecer la contraseña.")
#             password = usuario_data.password
#             password1 = usuario_data.password1
#             usuario = Usuario(id_usuario=usuario_data.id_usuario)  # Cargar la instancia del usuario con su ID
#             response = await usuario.newPassword(password, password1)
#             return {
#                 "data": response  # Aquí asignas una clave "data" al valor correspondiente
#             }
#         else:
#             raise HTTPException(status_code=400, detail="Acción no válida. Las acciones permitidas son: 'insert', 'update', 'activar', 'desactivar'.")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
###############################gestion_proveedor############################################################################################



@router.post("/proveedor")
async def gestion_proveedor(request: Proveedor_request):
    """
    Endpoint para gestion provedores.
    Soporta las acciones: 
    - 'verTodosLosProveedores': 

    ```Jsoon
        {
        "accion": "verTodosLosProveedores",
        "estado": true
        }


         {
        "accion": "verTodosLosProveedores",
        "estado": false
        }
    ```

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
# Ver todos los proveedores
        if request.accion == "verTodosLosProveedores":
            if request.estado is None:
                raise HTTPException(
                    status_code=400, detail="El parámetro 'estado' es requerido para esta acción."
                )            
            proveedor = Proveedor()            
            response = await proveedor.verTodosLosProveedores(request.estado)
            return {"data": response}

# Agregar nuevo proveedor
        elif request.accion == "agregarProveedor":
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
    



# ########################script automatico###############################################
# @router.post("/insertar-registros")
# async def insertar_registros():
#         """Endpoint para insertar 50,000 registros en la base de datos."""
#         resultado = insertar_registros()
#         return resultado    
#         # Configuración de conexión a la base de datos
# DB_CONFIG = {
#             "user": "postgres",
#             "password": "DarioDavid-bd-UBU-1",
#             "host": "92.112.176.191",
#             "port": 5432,
#             "database": "stock_TEST"
#         }

# def generar_codigo_barras():
#             """Genera un código de barras aleatorio de 9 dígitos."""
#             return ''.join(random.choices(string.digits, k=9))

# def insertar_registros():
#     """Inserta 50,000 registros en la tabla de productos."""
#     conexion = None  # Inicializar la variable fuera del bloque try
#     try:
#         # Conexión a la base de datos
#         conexion = psycopg2.connect(**DB_CONFIG)
#         cursor = conexion.cursor(cursor_factory=DictCursor)

#         # Consulta SQL para insertar productos
#         sql_producto = """
#         INSERT INTO productos (marca, nombre, descripcion, precio, codigo_barras, id_proveedor, estado, fecha_creacion)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
#         RETURNING id_producto;
#         """

#         # Consulta SQL para insertar stock
#         sql_stock = """
#         INSERT INTO stock (id_producto, stock_actual, stock_minimo, stock_maximo)
#         VALUES (%s, %s, %s, %s);
#         """

#         # Generar e insertar 50,000 registros
#         for _ in range(50000):
#             marca = "Marca_" + random.choice(string.ascii_uppercase)
#             nombre = "Producto_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#             descripcion = "Descripcion del producto " + nombre
#             precio = round(random.uniform(10, 500), 2)
#             stock_actual = random.randint(0, 100)
#             stock_minimo = random.randint(0, 10)
#             stock_maximo = stock_actual + random.randint(10, 50)
#             id_proveedor = random.choice([1, 2, 3])
#             codigo_barras = generar_codigo_barras()
#             estado = 'activo'

#             # Insertar producto y obtener id_producto
#             cursor.execute(sql_producto, (marca, nombre, descripcion, precio, codigo_barras, id_proveedor, estado))
#             id_producto = cursor.fetchone()[0]

#             # Insertar stock para el producto
#             cursor.execute(sql_stock, (id_producto, stock_actual, stock_minimo, stock_maximo))

#         # Confirmar los cambios en la base de datos
#         conexion.commit()
#         print("Se han insertado 50,000 registros exitosamente.")

#     except Exception as e:
#         print(f"Error al insertar registros: {e}")
#         if conexion:  # Verificar si la conexión existe antes de usarla
#             conexion.rollback()

#     finally:
#         # Cerrar la conexión
#         if conexion:  # Verificar si la conexión existe antes de usarla
#             cursor.close()
#             conexion.close()

###############################producto_categoria############################################################################################


@router.post("/producto_categoria")
async def producto_categoria(request: Categoria_request):
    """
    Endpoint para gestion categorías de productos.
    Soporta las acciones:
    - 'verTodasLasCategorias': Listar todas las categorías.
        ```json
            {
            "accion": "verTodasLasCategorias",
            "incluir_inactivas": true
            }
        

            {
            "accion": "verTodasLasCategorias",
            "incluir_inactivas": false
            }
        ```

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

        # Listar todas las categorías
        if request.accion == "verTodasLasCategorias":
            resultado = await categoria.ver_todas_categorias(request.incluir_inactivas)
            return {"status": "success", "data": resultado}

        # Agregar una nueva categoría
        elif request.accion == "agregarCategoria":
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




@router.post("/producto_marca")
async def producto_marca(request: Marca_request):
    """
    Endpoint para gestion marcas de productos.
    Soporta las acciones:
    - 'verTodasLasMarcas': Listar todas las marcas.
        ```json
            {
            "accion": "verTodasLasMarcas",
            "incluir_inactivas": true
            }
        

            {
            "accion": "verTodasLasMarcas",
            "incluir_inactivas": false
            }
        ```

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
        # Listar todas las marcas
        if request.accion == "verTodasLasMarcas":
            resultado = await marca.ver_todas_marcas(request.incluir_inactivas)
            return {"status": "success", "data": resultado}

        # Agregar una nueva marca
        elif request.accion == "agregarMarca":
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

@router.post("/movimiento_stock")
async def movimiento_stock(request: Stock_request):
    """
        Ejemplo de Payload de Entrada:

            ```json
                    {
                "movimientos": [
                {
                "id_producto": 1,
                "cantidad": 10,
                "operacion": "incrementar",
                "id_usuario": 123,
                "observaciones": "Reabastecimiento",
                "id_proveedor": 1,
                "id_almacen": 1,
                "id_estante": 1,
                "descripcion": "primer producto en entrar"
                },
                {
                "id_producto": 2,
                "cantidad": 10,
                "operacion": "incrementar",
                "id_usuario": 123,
                "observaciones": "Reabastecimiento",
                "id_proveedor": 1,
                "id_almacen": 1,
                "id_estante": 1,
                "descripcion": "segundo producto en entrar"
                }
            ]
            }

            ```    
    """       
        


    resultados = []  # Aquí guardaremos el resultado de cada movimiento
    print("entra antes de instanciar el objeto")
    stock = Stock()

    for movimiento in request.movimientos:
        try:
            if movimiento.operacion == "incrementar":
                resultado = await stock.entradaStock(
                    id_producto=movimiento.id_producto,
                    cantidad=movimiento.cantidad,
                    id_usuario=movimiento.id_usuario,                    
                    id_proveedor=movimiento.id_proveedor,
                    id_almacen=movimiento.id_almacen,
                    id_estante=movimiento.id_estante,
                    descripcion=movimiento.descripcion,
                    operacion=movimiento.operacion
                )
            elif movimiento.operacion == "disminuir":
                resultado = await stock.salidaStock(
                    id_producto=movimiento.id_producto,
                    cantidad=movimiento.cantidad,
                    id_usuario=movimiento.id_usuario,                    
                    id_proveedor=movimiento.id_proveedor,
                    id_almacen=movimiento.id_almacen,
                    id_estante=movimiento.id_estante,
                    descripcion=movimiento.descripcion,
                    operacion=movimiento.operacion
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Operación no válida: {movimiento.operacion}"
                )

            # Agregar resultado al listado
            resultados.append({
                "id_producto": movimiento.id_producto,
                "status": "success",
                "mensaje": f"Stock {movimiento.operacion} correctamente para el producto {movimiento.id_producto}.",
                "stock_actualizado": resultado.get("stock_actualizado")  # Ajusta según la respuesta de tus métodos
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

###########################Almacen#################################################


@router.post("/almacen")
async def gestion_almacen(request: Almacen_request):
    """
    Endpoint para gestion almacen.
    Soporta las acciones: 
    - 'verTodosLosAlmacenes': 

    ```Jsoon
        {
        "accion": "verTodosLosAlmacenes",
        "estado": true
        }


         {
        "accion": "verTodosLosAlmacenes",
        "estado": false
        }
    ```

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
# Ver todos los almacenes
        if request.accion == "verTodosLosAlmacenes":
            if request.estado is None:
                raise HTTPException(
                    status_code=400, detail="El parámetro 'estado' es requerido para esta acción."
                )            
            almacen = Almacen()            
            response = await almacen.verTodosLosAlmacenes(request.estado)
            return {"data": response}

# Agregar nuevo almacen
        elif request.accion == "agregarAlmacen":
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


@router.post("/almacen_estante")
async def gestion_almacen_estante(request: Estante_request):
    """
    Endpoint para gestion estante.
    Soporta las acciones: 
    - 'verTodosLosEstantes': 

    ```Jsoon
        {
        "accion": "verTodosLosEstantes",
        "id_almacen": 1,
        "estado": true
        }


         {
        "accion": "verTodosLosEstantes",
        "estado": false
        }
    ```

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
# Ver todos los estantes
        if request.accion == "verTodosLosEstantes":
            if request.estado is None:
                raise HTTPException(
                    status_code=400, detail="El parámetro 'estado' es requerido para esta acción."
                )            
            estante = Estante()            
            response = await estante.verTodosLosestantes(request.id_almacen,request.estado)
            return {"data": response}

# Agregar nuevo estante
        elif request.accion == "agregarEstante":
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
@router.post("/stock", response_model=List[Dict[str, Any]])
async def consultar_stock(
    filtros: FiltrosStock  # Recibimos los filtros en el cuerpo de la solicitud
):
    """
    Endpoint para consultar la tabla 'stock' con filtros en el cuerpo de la solicitud.
        Endpoint para gestion estante.
        Soporta las acciones: 
        - 'verTodosLosEstantes': 

    ```Json
        {            
        }
     ```
    """
    stock = Stock()  # Instancia de la clase Stock
    try:
        resultados = await stock.obtener_stock(  # Usamos el método obtener_stock
            id_producto=filtros.id_producto,
            id_almacen=filtros.id_almacen,
            estado=filtros.estado
        )
        return resultados
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


############################stock_movimientos_endpoints#######################################################################


@router.post("/tabla_consulta_stock_movimientos")
async def consultar_movimientos(
    filtros: FiltrosStock  # Recibimos un objeto con los filtros en el cuerpo de la solicitud
):
    """
    Endpoint para consultar la tabla 'stock_movimientos' con filtros en el cuerpo de la solicitud.
     ```Json
        {            
        }
     ```
    """
    stock = Stock()  # Instancia de la clase Stock
    try:
        # Pasamos los parámetros desde el cuerpo de la solicitud
        resultados = await stock.obtener_movimientos(
            id_producto=filtros.id_producto,
            id_usuario=filtros.id_usuario,
            fecha_inicio=filtros.fecha_inicio,
            fecha_fin=filtros.fecha_fin
        )
        return resultados  # Devuelve la respuesta directamente
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    