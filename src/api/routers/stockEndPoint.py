from fastapi import APIRouter, HTTPException, UploadFile, File, Form  # Importa APIRouter para crear grupos de rutas y HTTPException para manejar errores.
from fastapi.responses import JSONResponse, Response  # Importa JSONResponse para devolver respuestas JSON personalizadas.
from pydantic import BaseModel  # Importa BaseModel para definir esquemas de solicitudes y respuestas.
from typing import Optional
#importa las clases
from models.todosLosUsuarios import TodosLosUsuarios
from models.producto import Producto # Importa Clase Producto
from models.proveedor import Proveedor # Importa Clase Proveedor

from models.login import Login,create_jwt_token # Importa Clase Recibo
#importa los schemas
from schemas import TodosLosUsuarios_response,TodosLosUsuarios_request, UsuarioLogin_request,Usuario_request,Producto_request,Producto_response,Proveedor_request
import logging
import json
import os
import subprocess
import calendar
from datetime import datetime
#from fastapi.responses import FileResponse



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
async def manejar_producto(request: Producto_request):
    """
    Endpoint para manejar productos.
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
        "marca": "Acme",
        "nombre": "Cigarros",
        "descripcion": "Cigarros electronicos",
        "precio": 50,
        "stock_actual": 0,
        "stock_minimo": 0,
        "stock_maximo": 0,
        "proveedor_id": 2,
        "codigo_barras": "xxxxxxxxx"
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
            # Verificamos si todos los parámetros necesarios están presentes
            if not all([request.marca, request.nombre, request.descripcion, request.precio, request.stock_actual, request.stock_minimo, request.stock_maximo, request.proveedor_id, request.codigo_barras]):
                raise HTTPException(
                    status_code=400,
                    detail="Todos los parámetros 'marca', 'nombre', 'descripcion', 'precio', 'stock_actual', 'stock_minimo', 'stock_maximo', 'proveedor_id' y 'codigo_barras' son requeridos."
                )

            # Crear una instancia de Producto
            producto = Producto()

            # Llamar al método agregar_producto de la clase Producto
            response = await producto.agregar_producto(
                request.marca,
                request.nombre,
                request.descripcion,
                request.precio,
                request.stock_actual,
                request.stock_minimo,
                request.stock_maximo,
                request.proveedor_id,
                request.codigo_barras,
                request.forceAdd,
                request.accion_stock
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
            response = await producto.eliminar_producto(request.id_producto)
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
    
################################################################################

@router.post("/login")        
async def login(usuario: UsuarioLogin_request, response: Response):
    """
    Endpoint login
        {
        "cuil": "string",
        "password": "string"
        }
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
###########################################################################################################################



@router.post("/proveedor")
async def manejar_proveedor(request: Proveedor_request):
    """
    Endpoint para manejar provedores.
    Soporta las acciones: 
    - 'verTodosLosProveedores': Ver todos los Proveedores según su estado.
    - 'agregarProveedor': Agregar un nuevo Proveedor.
    - 'eliminarProveedor': Eliminar un Proveedor por ID.
    - 'editarProveedor' : Editar un Proveedor por ID.
    """
    try:
        # Ver todos los proveedores
        if request.accion == "verTodosLosProveedores":
            if request.estado is None:
                raise HTTPException(
                    status_code=400, detail="El parámetro 'estado' es requerido para esta acción."
                )
            proveedor = Proveedor()
            response = await proveedor .verTodosLosProductos(request.estado)
            return {"data": response}

        # Agregar nuevo proveedor
        elif request.accion == "agregarProveedor":
            if not all([request.nombre, request.descripcion, request.precio, request.stock_actual, request.proveedor_id]):
                raise HTTPException(
                    status_code=400,
                    detail="Todos los parámetros 'nombre', 'descripcion', 'precio', 'stock_actual' y 'proveedor_id' son requeridos."
                )
            proveedor = Proveedor()
            response = await proveedor.agregar_proveedor(
                request.nombre, request.descripcion, request.precio, request.stock_actual, request.proveedor_id
            )
            return response

        # Eliminar proveedor
        elif request.accion == "eliminarProveedor":
            if request.id_producto is None:
                raise HTTPException(
                    status_code=400,
                    detail="El parámetro 'id_proveedor' es requerido para esta acción."
                )
            proveedor = Proveedor()
            response = await proveedor.eliminar_producto(request.id_producto)
            return response

        # Editar proveedor
        elif request.accion == "editarProveedor":
            if request.id_producto is None:
                raise HTTPException(
                    status_code=400,
                    detail="El parámetro 'id_proveedor' es requerido para esta acción."
                )
            proveedor = Proveedor()
            response = await proveedor.eliminar_producto(request.id_producto)
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