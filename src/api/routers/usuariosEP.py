from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query  # Importa APIRouter para crear grupos de rutas y HTTPException para manejar errores.
from fastapi.responses import JSONResponse, Response  # Importa JSONResponse para devolver respuestas JSON personalizadas.
from pydantic import BaseModel  # Importa BaseModel para definir esquemas de solicitudes y respuestas.
#importa las clases
from models.todosLosUsuarios import TodosLosUsuarios
from models.usuario import Usuario  # Importar tu clase Usuario
#from .usuario import Usuario # Importa Clase Recibo
from models.login import Login # Importa Clase Recibo
from models.logout import Logout  # ✅ Importamos la clase Logout
from models.getRol import GetRol  # Importa la clase 
from models.validateTokenApi import Token
from models.perfil import Perfil

from models.rol import validar_token_con_roles
from typing import List,Optional

#importa los schemas
from schemas import   UsuarioResponse,UsuarioCreate,PerfilRequest,UsuarioEditRequest,UsuarioLogin_request,GetRol_request,TodosLosRecibos_request,TodosLosRecibos_response,Usuario_request,Download_Request,Download_response,validateTockenApi
import logging
import json
import os
import subprocess
import calendar
from datetime import datetime
import aiohttp


logger = logging.getLogger(__name__)
# Crea un enrutador para agrupar las rutas relacionadas con recibos.
router = APIRouter()


router = APIRouter(tags=["Usuarios, Perfiles, Logins y Tokens"])


@router.post("/usuarios")
async def agregar_usuario(usuario_data: UsuarioCreate):
    """
    ✅ **Crear un nuevo usuario en el sistema**  

    📌 **Descripción:**  
    Este endpoint permite registrar un nuevo usuario en la base de datos.  
    Se valida que el email y el nombre de usuario sean únicos antes de crearlo.  

    📌 **Parámetros:**  
    - `usuario_data` (JSON, requerido): Datos del usuario a registrar.
      - `nombre` (str, requerido)
      - `apellido` (str, requerido)
      - `email` (EmailStr, requerido, debe ser único)
      - `usuario` (str, requerido, debe ser único)
      - `password` (str, requerido, mínimo 6 caracteres)

    📌 **Ejemplo de solicitud (`POST /usuarios`)**  
    ```json
    {
        "nombre": "Juan",
        "apellido": "Pérez",
        "email": "juan.perez@example.com",
        "usuario": "juanperez",
        "password": "segura123"
    }
    ```

    📌 **Ejemplo de Respuesta (`201 Created`)**  
    ```json
    {
        "message": "Usuario agregado correctamente",
        "id_usuario": 10,
        "code": 201
    }
    ```
    """
    logger.info(f"Intentando registrar usuario: {usuario_data.usuario} - Email: {usuario_data.email}")

    # Validación de la longitud de la contraseña
    if len(usuario_data.password) < 6:
        logger.warning(f"Contraseña demasiado corta para el usuario {usuario_data.usuario}")
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres.")

    # Llamada al servicio de usuarios para insertar el nuevo usuario en la BD
    resultado = await Usuario.agregar_usuario(
        usuario_data.nombre,
        usuario_data.apellido,
        usuario_data.email,
        usuario_data.usuario,
        usuario_data.password
    )

    # Manejo de respuestas
    if resultado["code"] == 409:
        logger.warning(f"Conflicto al registrar usuario: {usuario_data.usuario} - {resultado['message']}")
        raise HTTPException(status_code=409, detail=resultado["message"])

    if resultado["code"] == 500:
        logger.error(f"Error interno al registrar usuario: {usuario_data.usuario}")
        raise HTTPException(status_code=500, detail=resultado["message"])

    logger.info(f"Usuario {usuario_data.usuario} registrado correctamente con ID {resultado['id_usuario']}")
    return JSONResponse(content=resultado, status_code=201)

########################################################################


@router.get("/usuarios", response_model=List[dict])
async def obtener_usuarios(estado: bool):
    """
    *Obtener todos los usuarios filtrando por estado (`true` o `false`)*
    
    **Parámetros:**
    - `estado` (bool): `true` para activos, `false` para deshabilitados.

    **Códigos de respuesta:**
    ✅ Éxito → 200 OK  
    ✅ No hay usuarios → 404 Not Found  
    ✅ Error del servidor → 500 Internal Server Error  
    """
    resultado = await TodosLosUsuarios.obtener_todos(estado)

    # Si la lista está vacía, significa que no hay usuarios con ese estado
    if not resultado:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios con el estado especificado")

    # Si hay un error, devolvemos HTTP 500
    if isinstance(resultado, dict) and "code" in resultado and resultado["code"] == 500:
        raise HTTPException(status_code=500, detail="Error al obtener los usuarios")

    return resultado



###########################login#####################################################################

@router.post("/login")

async def login(usuario: UsuarioLogin_request, response: Response):
    """
    *Login

    ```json
    {
        "usuario": "str",
        "password": "str"
    }
    ```
    **Códigos de respuesta:**
    ✅ Usuario o contraseña incorrectos → 401 Unauthorized  
    ✅ Usuario deshabilitado → 403 Forbidden  
    ✅ Errores inesperados → 500 Internal Server Error  
    """
    resultado = await Login.login_usuario(usuario.usuario, usuario.password)

    print("que devuelve login_usuario:", resultado)

    # Si el usuario no existe (resultado es None), devolvemos un mensaje genérico para evitar enumeración de usuarios
    if resultado is None:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    # Mapeo de códigos de error a excepciones HTTP
    errores_http = {
        0: (401, "Usuario o contraseña incorrectos"),
        2: (403, "Usuario deshabilitado")
    }

    # Si el resultado contiene un código de error, lanzar excepción directamente
    if isinstance(resultado, dict) and "code" in resultado:
        status_code, mensaje = errores_http.get(resultado["code"], (500, "Error desconocido"))
        raise HTTPException(status_code=status_code, detail=mensaje)

    # Autenticación exitosa
    try:
        id_usuario = resultado["id_usuario"]
        usuario = resultado["usuario"]
        nombre = resultado["nombre"]
        apellido = resultado["apellido"]
        email = resultado["email"]
        auth_token = resultado["auth_token"]
        funciones=resultado["funciones"]
        # Configurar cookie segura para el token (opcional)
        response.set_cookie(key="auth_token", value=auth_token, httponly=True, samesite="Lax")
        return {
            "id_usuario": id_usuario,
            "usuario": usuario,
            "auth_token": auth_token,
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "funciones": funciones
        }
    except Exception as e:
        print(f"Error inesperado en login: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor al procesar la autenticación.")




###########################logout#####################################################################

@router.post("/logout")
async def logout(response: Response, usuario: validateTockenApi):
    """
    🔐 **Cerrar sesión eliminando el token de `tokens_activos`.**
    
    📌 Verifica si el token existe antes de eliminarlo.  
    📌 Si el token no está en la BD, devuelve un error `401 Unauthorized`.  
    📌 Si el token es válido, lo elimina y cierra sesión correctamente.  
    """
    return await Logout.cerrar_sesion(response, usuario.token)


###########################validateToken#####################################################################

@router.post("/validateTokenApi")
async def validateToken(usuario: validateTockenApi, response: Response):
    resultado = await Token.checkTokenGeneral(usuario.token)

    # Verifica si resultado es un diccionario antes de continuar
    if not isinstance(resultado, dict):
        raise HTTPException(status_code=500, detail="Error en la respuesta del servidor, no se pudo autenticar.")
    if "validate" in resultado and resultado["validate"]:
        data = resultado.get("data", {})
        id_usuario = data.get("id_usuario")
        rol = data.get("rol")
        cuil = data.get("cuil")
        if id_usuario and rol and cuil:
            # Aquí podrías generar un nuevo token si lo necesitas
            # token = await Token.crearTokenLocal(id_usuario, rol, cuil)
            # response.set_cookie(key="auth_token", value=token, httponly=True)

            return {"validate": True, "id_usuario": id_usuario, "rol": rol, "cuil": cuil}

    # Si la validación falla
    error_message = resultado.get("error", "Token inválido o expirado.")
    raise HTTPException(status_code=401, detail=error_message)

############################cambiar_estado_usuario####################################################################
@router.put("/usuarios/{id_usuario}/estado")
async def cambiar_estado_usuario(id_usuario: int, estado: bool):
    """
    *Activar o desactivar un usuario*
    
    **Parámetros:**
    - `id_usuario` (int): ID del usuario a modificar.
    - `estado` (bool): `true` para activar, `false` para desactivar.

    **Códigos de respuesta:**
    ✅ Usuario activado/desactivado → 200 OK  
    ✅ Usuario no encontrado → 404 Not Found  
    ✅ Error interno → 500 Internal Server Error  
    """
    resultado = await Usuario.cambiar_estado_usuario(id_usuario, estado)

    # Manejo de respuestas
    if resultado["code"] == 404:
        raise HTTPException(status_code=404, detail=resultado["message"])
    elif resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado


############################editar_usuario####################################################################

@router.put("/usuarios/{id_usuario}")
async def editar_usuario(id_usuario: int, request: UsuarioEditRequest):
    """
    📝 **Editar un usuario existente sin modificar su estado**  
    📌 Este endpoint permite actualizar los datos de un usuario en el sistema.  
    La activación o desactivación del usuario se maneja en otro endpoint.

    ---
    
    🔹 **Parámetros:**  
    - `id_usuario` (int): ID del usuario a modificar.  
    - `request` (JSON): Datos a actualizar (nombre, apellido, email, usuario).  

    ---
    
    🔹 **Ejemplo de solicitud (Request Body):**  
    ```json
    {
        "nombre": "Juan",
        "apellido": "Pérez",
        "email": "juan.perez@example.com",
        "usuario": "juanperez"
    }
    ```

    ---
    
    🔹 **Códigos de Respuesta:**  
    ✅ **200 OK** → Usuario actualizado correctamente.  
    ✅ **304 Not Modified** → No se detectaron cambios en los datos.  
    ✅ **404 Not Found** → Usuario no encontrado en la base de datos.  
    ✅ **409 Conflict** → Email o nombre de usuario ya en uso.  
    ✅ **500 Internal Server Error** → Error interno al procesar la solicitud.  

    ---
    
    🔹 **Ejemplo de Respuestas:**  
    **✅ Usuario actualizado correctamente (200 OK):**  
    ```json
    {
        "message": "Usuario actualizado correctamente",
        "code": 200
    }
    ```
    
    **⚠️ No se detectaron cambios (304 Not Modified):**  
    ```json
    {
        "message": "No se detectaron cambios en los datos del usuario",
        "code": 304
    }
    ```
    
    **🚫 Usuario no encontrado (404 Not Found):**  
    ```json
    {
        "message": "Usuario no encontrado",
        "code": 404
    }
    ```

    **🚫 Email o nombre de usuario en uso (409 Conflict):**  
    ```json
    {
        "message": "El email ya está registrado por otro usuario",
        "code": 409
    }
    ```

    **❌ Error interno (500 Internal Server Error):**  
    ```json
    {
        "message": "Error interno al editar el usuario",
        "code": 500
    }
    ```
    """
    resultado = await Usuario.editar_usuario(
        id_usuario,
        request.nombre,
        request.apellido,
        request.email,
        request.usuario
    )

    # Manejo de respuestas con códigos HTTP adecuados
    if resultado["code"] == 404:
        raise HTTPException(status_code=404, detail=resultado["message"])
    if resultado["code"] == 409:
        raise HTTPException(status_code=409, detail=resultado["message"])
    if resultado["code"] == 304:
        raise HTTPException(status_code=304, detail=resultado["message"])
    if resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado
#############################    🔐 **Cambiar contraseña (autogestionado por el usuario)**  #########################################
class CambiarPasswordRequest(BaseModel):
    password_actual: str
    password_nuevo: str
class CambiarPasswordRequest(BaseModel):
    password_actual: str
    password_nuevo: str

@router.put("/usuarios/{id_usuario}/cambiar-password")
async def cambiar_password_usuario(id_usuario: int, request: CambiarPasswordRequest):
    """
    🔐 **Cambiar contraseña (autogestionado por el usuario)**  
    📌 Permite a un usuario cambiar su propia contraseña verificando la actual antes de actualizarla.  

    ---
    
    🔹 **Parámetros:**  
    - `id_usuario` (int): ID del usuario que cambiará su contraseña.  
    - `request` (JSON):  
      - `password_actual` (str): Contraseña actual del usuario.  
      - `password_nuevo` (str): Nueva contraseña que se establecerá.  

    ---
    
    🔹 **Ejemplo de solicitud (Request Body):**  
    ```json
    {
        "password_actual": "MiContraseñaVieja123",
        "password_nuevo": "MiNuevaContraseña456"
    }
    ```

    ---
    
    🔹 **Códigos de Respuesta:**  
    ✅ **200 OK** → Contraseña cambiada con éxito.  
    ❌ **401 Unauthorized** → Contraseña actual incorrecta.  
    ❌ **404 Not Found** → Usuario no encontrado.  
    ❌ **500 Internal Server Error** → Error interno en el servidor.  

    ---
    
    🔹 **Ejemplo de Respuestas:**  

    **✅ Contraseña cambiada (200 OK):**  
    ```json
    {
        "message": "Contraseña actualizada correctamente",
        "code": 200
    }
    ```

    **🚫 Contraseña incorrecta (401 Unauthorized):**  
    ```json
    {
        "message": "La contraseña actual es incorrecta",
        "code": 401
    }
    ```

    **🚫 Usuario no encontrado (404 Not Found):**  
    ```json
    {
        "message": "Usuario no encontrado",
        "code": 404
    }
    ```

    **❌ Error interno (500 Internal Server Error):**  
    ```json
    {
        "message": "Error interno al cambiar la contraseña",
        "code": 500
    }
    ```
    """

    resultado = await Usuario.cambiar_password_usuario(id_usuario, request.password_actual, request.password_nuevo)

    if resultado["code"] == 404:
        raise HTTPException(status_code=404, detail=resultado["message"])
    if resultado["code"] == 401:
        raise HTTPException(status_code=401, detail=resultado["message"])
    if resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado
##########################    🔐 **Resetear la contraseña de un usuario (solo admin)** ############################################

@router.put("/usuarios/{id_usuario}/resetear-password")
async def resetear_password_admin(id_usuario: int):
    """
    🔐 **Resetear la contraseña de un usuario (solo admin)**  
    📌 Permite a un administrador generar una nueva contraseña aleatoria para un usuario y enviarla a su correo.  

    ---
    
    🔹 **Parámetros:**  
    - `id_usuario` (int): ID del usuario cuya contraseña será reseteada.  

    ---
    
    🔹 **Códigos de Respuesta:**  
    ✅ **200 OK** → Contraseña reseteada y enviada por correo.  
    ❌ **404 Not Found** → Usuario no encontrado.  
    ❌ **500 Internal Server Error** → Error interno en el servidor.  

    ---
    
    🔹 **Ejemplo de Respuestas:**  

    **✅ Contraseña reseteada (200 OK):**  
    ```json
    {
        "message": "Contraseña reseteada y enviada por correo",
        "code": 200
    }
    ```

    **🚫 Usuario no encontrado (404 Not Found):**  
    ```json
    {
        "message": "Usuario no encontrado",
        "code": 404
    }
    ```

    **❌ Error interno (500 Internal Server Error):**  
    ```json
    {
        "message": "Error interno al resetear la contraseña",
        "code": 500
    }
    ```
    """

    resultado = await Usuario.resetear_password_admin(id_usuario)

    if resultado["code"] == 404:
        raise HTTPException(status_code=404, detail=resultado["message"])
    if resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado
######################################################################

@router.get("/usuarios/{id_usuario}/historial_logins")
async def obtener_historial_logins(id_usuario: int):
    """
    📝 **Obtener historial de inicio de sesión de un usuario**  
    📌 Este endpoint devuelve el historial de intentos de login de un usuario por su `id_usuario`.  

    ---
    
    🔹 **Parámetro:**  
    - `id_usuario` (int): ID del usuario a consultar.  

    ---
    
    🔹 **Ejemplo de respuesta:**  
    ✅ **200 OK** → Historial obtenido exitosamente.  
    ```json
    {
        "message": "Historial obtenido exitosamente",
        "code": 200,
        "historial": [
            {
                "id_usuario": 5,
                "fecha_logins": "2024-02-12 14:30:45",
                "ip_origen": "192.168.1.100",
                "exito": true,
                "motivo_fallo": null
            },
            {
                "id_usuario": 5,
                "fecha_logins": "2024-02-10 18:12:30",
                "ip_origen": "192.168.1.105",
                "exito": false,
                "motivo_fallo": "Contraseña incorrecta"
            }
        ]
    }
    ```

    ---
    
    🔹 **Códigos de Respuesta:**  
    ✅ **200 OK** → Historial obtenido exitosamente.  
    ✅ **204 No Content** → No hay registros de inicio de sesión para este usuario.  
    ✅ **404 Not Found** → Usuario no encontrado en la base de datos.  
    ✅ **500 Internal Server Error** → Error interno al procesar la solicitud.  
    """
    resultado = await Usuario.obtener_historial_logins(id_usuario)

    # Manejo de respuestas con códigos HTTP adecuados
    if resultado["code"] == 404:
        raise HTTPException(status_code=404, detail=resultado["message"])
    if resultado["code"] == 204:
        raise HTTPException(status_code=204, detail=resultado["message"])
    if resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado


########################Perfiles########################################


@router.get("/perfiles")
async def listar_perfiles(estado: bool = Query(..., description="Estado del perfil (true: activo, false: inactivo)")):
    """
    📝 **Obtener todos los perfiles filtrando por estado (`true` o `false`)**  
    📌 Este endpoint permite obtener una lista de perfiles según su estado.

    ---
    
    🔹 **Parámetros:**  
    - `estado` (bool, requerido): `true` para obtener perfiles activos, `false` para inactivos.  

    ---
    
    🔹 **Códigos de respuesta:**  
    ✅ **200 OK** → Lista de perfiles obtenida correctamente.  
    ✅ **204 No Content** → No hay perfiles con el estado solicitado.  
    ✅ **500 Internal Server Error** → Error en el servidor.  

    ---
    
    🔹 **Ejemplo de Respuesta (`200 OK`)**  
    ```json
    {
        "message": "Perfiles obtenidos exitosamente",
        "code": 200,
        "perfiles": [
            {
                "id_perfil": 1,
                "nombre": "Administrador",
                "descripcion": "Acceso total al sistema",
                "estado": true,
                "fecha_creacion": "2024-02-12T12:00:00"
            }
        ]
    }
    ```
    """
    resultado = await Perfil.listar_perfiles(estado)

    if resultado["code"] == 204:
        raise HTTPException(status_code=204, detail=resultado["message"])
    if resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado

@router.post("/perfiles")
async def crear_perfil(request: PerfilRequest):
    """
    📝 **Crear un nuevo perfil en el sistema**  
    📌 Este endpoint permite registrar un nuevo perfil con su nombre y descripción.

    ---
    
    🔹 **Parámetros (Body JSON):**  
    ```json
    {
        "nombre": "Operador de Stock",
        "descripcion": "Gestión de inventario y reportes de stock."
    }
    ```

    ---
    
    🔹 **Códigos de respuesta:**  
    ✅ **201 Created** → Perfil creado exitosamente.  
    ✅ **409 Conflict** → El perfil ya existe.  
    ✅ **500 Internal Server Error** → Error en el servidor.  

    ---
    
    🔹 **Ejemplo de Respuesta (`201 Created`)**  
    ```json
    {
        "message": "Perfil creado exitosamente",
        "code": 201,
        "id_perfil": 3
    }
    ```
    """
    resultado = await Perfil.crear_perfil(request.nombre, request.descripcion)

    if resultado["code"] == 409:
        raise HTTPException(status_code=409, detail=resultado["message"])
    if resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado

@router.put("/perfiles/{id_perfil}")
async def modificar_perfil(id_perfil: int, request: PerfilRequest):
    """
    📝 **Modificar un perfil existente**  
    📌 Este endpoint permite actualizar el nombre y descripción de un perfil.

    ---
    
    🔹 **Parámetros:**  
    - `id_perfil` (int, requerido): ID del perfil a modificar.  

    🔹 **Body JSON:**  
    ```json
    {
        "nombre": "Gestor de Stock",
        "descripcion": "Responsable de la gestión del stock y reportes."
    }
    ```

    ---
    
    🔹 **Códigos de respuesta:**  
    ✅ **200 OK** → Perfil actualizado correctamente.  
    ✅ **304 Not Modified** → No se detectaron cambios.  
    ✅ **404 Not Found** → Perfil no encontrado.  
    ✅ **500 Internal Server Error** → Error en el servidor.  

    ---
    
    🔹 **Ejemplo de Respuesta (`200 OK`)**  
    ```json
    {
        "message": "Perfil actualizado correctamente",
        "code": 200
    }
    ```
    """
    resultado = await Perfil.modificar_perfil(id_perfil, request.nombre, request.descripcion)

    if resultado["code"] == 404:
        raise HTTPException(status_code=404, detail=resultado["message"])
    if resultado["code"] == 304:
        raise HTTPException(status_code=304, detail=resultado["message"])
    if resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado

@router.put("/perfiles/{id_perfil}/estado")
async def cambiar_estado_perfil(id_perfil: int, estado: bool):
    """
    📝 **Habilitar o deshabilitar un perfil**  
    📌 Este endpoint permite activar (`true`) o desactivar (`false`) un perfil.

    ---
    
    🔹 **Parámetros:**  
    - `id_perfil` (int, requerido): ID del perfil a modificar.  
    - `estado` (bool, requerido): `true` para habilitar, `false` para deshabilitar.  

    ---
    
    🔹 **Códigos de respuesta:**  
    ✅ **200 OK** → Estado del perfil actualizado correctamente.  
    ✅ **404 Not Found** → Perfil no encontrado.  
    ✅ **500 Internal Server Error** → Error en el servidor.  

    ---
    
    🔹 **Ejemplo de solicitud (`PUT /perfiles/3/estado?estado=false`)**  
    ```
    PUT /perfiles/3/estado?estado=false
    ```

    🔹 **Ejemplo de Respuesta (`200 OK`)**  
    ```json
    {
        "message": "Perfil deshabilitado correctamente",
        "code": 200
    }
    ```
    """
    resultado = await Perfil.cambiar_estado_perfil(id_perfil, estado)

    if resultado["code"] == 404:
        raise HTTPException(status_code=404, detail=resultado["message"])
    if resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado



@router.post("/perfiles/{id_perfil}/usuarios/{id_usuario}")
async def asignar_usuario_a_perfil(id_usuario: int, id_perfil: int):
    """
    📝 **Asignar un usuario activo a un perfil**  
    📌 Solo se pueden asignar **usuarios activos (`estado=true`)**.  
    📌 Si el usuario ya tenía un perfil y estaba deshabilitado, lo reactivará.  

    ---
    
    🔹 **Parámetros:**  
    - `id_usuario` (int): ID del usuario a asignar.  
    - `id_perfil` (int): ID del perfil donde se asignará el usuario.  

    ---
    
    🔹 **Códigos de respuesta:**  
    ✅ **201 Created** → Usuario asignado correctamente.  
    ✅ **403 Forbidden** → El usuario no está activo.  
    ✅ **404 Not Found** → Usuario o perfil no encontrados.  
    ✅ **409 Conflict** → El usuario ya tiene un perfil asignado.  
    ✅ **500 Internal Server Error** → Error interno.  
    """
    resultado = await Perfil.asignar_usuario_a_perfil(id_usuario, id_perfil)

    if resultado["code"] == 403:
        raise HTTPException(status_code=403, detail=resultado["message"])
    if resultado["code"] == 404:
        raise HTTPException(status_code=404, detail=resultado["message"])
    if resultado["code"] == 409:
        raise HTTPException(status_code=409, detail=resultado["message"])
    if resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado



@router.get("/perfiles/{id_perfil}/usuarios")
async def obtener_usuarios_por_perfil(
    id_perfil: int,
    estado: bool = Query(None, description="Estado de la asignación (true=activos, false=inactivos, None=todos)")
):
    """
    📝 **Obtener usuarios dentro de un perfil con opción de filtrar por estado**  
    📌 Este endpoint permite listar los usuarios asignados a un perfil y filtrar por estado (`true`=activos, `false`=inactivos).  

    ---
    
    🔹 **Parámetros:**  
    - `id_perfil` (int): ID del perfil para obtener los usuarios asignados.  
    - `estado` (bool, opcional): `true` para ver activos, `false` para inactivos, `None` para todos.  

    ---
    
    🔹 **Códigos de respuesta:**  
    ✅ **200 OK** → Usuarios obtenidos exitosamente.  
    ✅ **204 No Content** → No hay usuarios con el estado solicitado.  
    ✅ **404 Not Found** → Perfil no encontrado.  
    ✅ **500 Internal Server Error** → Error interno en el servidor.  

    ---
    
    🔹 **Ejemplo de Respuesta (`200 OK`)**  
    ```json
    {
        "message": "Usuarios obtenidos exitosamente",
        "code": 200,
        "usuarios": [
            {
                "id_usuario": 5,
                "nombre": "Juan",
                "apellido": "Pérez",
                "email": "juan.perez@example.com",
                "usuario": "juanperez",
                "estado": true
            },
            {
                "id_usuario": 7,
                "nombre": "Ana",
                "apellido": "García",
                "email": "ana.garcia@example.com",
                "usuario": "anagarcia",
                "estado": false
            }
        ]
    }
    ```
    """
    resultado = await Perfil.obtener_usuarios_por_perfil(id_perfil, estado)

    if resultado["code"] == 204:
        raise HTTPException(status_code=204, detail=resultado["message"])
    if resultado["code"] == 404:
        raise HTTPException(status_code=404, detail=resultado["message"])
    if resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado





@router.get("/perfiles/{id_perfil}/funciones")
async def obtener_funciones_por_perfil(id_perfil: int):
        """
        📝 **Obtener todas las funciones asignadas a un perfil con permisos de lectura/escritura**  
        📌 Devuelve la lista de funciones asignadas a un perfil y sus permisos.

        ---
        
        🔹 **Códigos de respuesta:**  
        ✅ **200 OK** → Funciones obtenidas exitosamente.  
        ✅ **204 No Content** → No hay funciones asignadas.  
        ✅ **404 Not Found** → Perfil no encontrado.  
        ✅ **500 Internal Server Error** → Error en el servidor.  

        ---
        
        🔹 **Ejemplo de Respuesta (`200 OK`)**  
        ```json
        {
            "message": "Funciones obtenidas exitosamente",
            "code": 200,
            "funciones": [
                {
                    "id_funcion": 1,
                    "nombre": "ver_productos",
                    "descripcion": "Permite ver la lista de productos",
                    "lectura": true,
                    "escritura": false
                },
                {
                    "id_funcion": 2,
                    "nombre": "gestionar_productos",
                    "descripcion": "Permite agregar, editar o eliminar productos",
                    "lectura": true,
                    "escritura": true
                }
            ]
        }
        ```
        """
        resultado = await Perfil.obtener_funciones_por_perfil(id_perfil)

        if resultado["code"] == 204:
            raise HTTPException(status_code=204, detail=resultado["message"])
        if resultado["code"] == 404:
            raise HTTPException(status_code=404, detail=resultado["message"])
        if resultado["code"] == 500:
            raise HTTPException(status_code=500, detail=resultado["message"])

        return resultado


@router.post("/perfiles/{id_perfil}/funciones/{id_funcion}")
async def agregar_funcion_a_perfil(id_perfil: int, id_funcion: int, escritura: bool = False):
    """
    📝 **Asignar una función a un perfil con permisos de escritura**  
    📌 `lectura` siempre será `TRUE`, pero `escritura` se puede definir.

    ---
    
    🔹 **Parámetros:**  
    - `id_perfil` (int): ID del perfil.  
    - `id_funcion` (int): ID de la función.  
    - `escritura` (bool, opcional): `true` para permitir modificar, `false` solo lectura.  

    ---
    
    🔹 **Ejemplo de Llamada (`POST /perfiles/1/funciones/2`)**
    ```json
    {
        "escritura": true
    }
    ```
    """
    resultado = await Perfil.agregar_funcion_a_perfil(id_perfil, id_funcion, escritura)

    if resultado["code"] == 404:
        raise HTTPException(status_code=404, detail=resultado["message"])
    if resultado["code"] == 409:
        raise HTTPException(status_code=409, detail=resultado["message"])
    if resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado


@router.delete("/perfiles/{id_perfil}/funciones/{id_funcion}")
async def eliminar_funcion_de_perfil(id_perfil: int, id_funcion: int):
    """
    📝 **Eliminar una función de un perfil**
    📌 Remueve una función específica de un perfil.

    🔹 **Códigos de respuesta:**  
    ✅ **200 OK** → Función eliminada del perfil.  
    ✅ **404 Not Found** → La función no estaba asignada.  
    ✅ **500 Internal Server Error** → Error en el servidor.  
    """
    resultado = await Perfil.eliminar_funcion_de_perfil(id_perfil, id_funcion)

    if resultado["code"] == 404:
        raise HTTPException(status_code=404, detail=resultado["message"])
    if resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado




@router.get("/funciones")
async def listar_funciones():
    """
    📝 **Obtener todas las funciones del sistema (LA CARGA DE FUNCIONES ESTARA HARDCODEADA bylulohack)**  
    📌 Devuelve la lista de funciones disponibles.

    ---
    
    🔹 **Códigos de respuesta:**  
    ✅ **200 OK** → Funciones obtenidas exitosamente.  
    ✅ **204 No Content** → No hay funciones registradas.  
    ✅ **500 Internal Server Error** → Error en el servidor.  

    ---
    
    🔹 **Ejemplo de Respuesta (`200 OK`)**  
    ```json
    {
        "message": "Funciones obtenidas exitosamente",
        "code": 200,
        "funciones": [
            {
                "id_funcion": 1,
                "nombre": "ver_productos",
                "descripcion": "Permite ver la lista de productos"
            },
            {
                "id_funcion": 2,
                "nombre": "gestionar_productos",
                "descripcion": "Permite agregar, editar o eliminar productos"
            }
        ]
    }
    ```
    """
    resultado = await Perfil.listar_funciones()

    if resultado["code"] == 204:
        raise HTTPException(status_code=204, detail=resultado["message"])
    if resultado["code"] == 500:
        raise HTTPException(status_code=500, detail=resultado["message"])

    return resultado






