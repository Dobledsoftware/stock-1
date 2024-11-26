from fastapi import APIRouter, HTTPException, UploadFile, File, Form  # Importa APIRouter para crear grupos de rutas y HTTPException para manejar errores.
from fastapi.responses import JSONResponse, Response  # Importa JSONResponse para devolver respuestas JSON personalizadas.
from pydantic import BaseModel  # Importa BaseModel para definir esquemas de solicitudes y respuestas.
#importa las clases
from .todosLosUsuarios import TodosLosUsuarios
from .recibo import Recibo # Importa Clase Recibo
from .usuario import Usuario  # Importar tu clase Usuario
#from .usuario import Usuario # Importa Clase Recibo
from .login import Login,create_jwt_token # Importa Clase Recibo
from .getRol import GetRol  # Importa la clase 
#importa los schemas
from schemas import TodosLosUsuarios_response,TodosLosUsuarios_request,Recibo_request,  UsuarioLogin_request,GetRol_request,TodosLosRecibos_request,TodosLosRecibos_response,Usuario_request,Download_Request,Download_response
import logging
from .Contador_validador_pdf import  validate_pdf,save_uploaded_file, count_recibos_in_pdf
from .Parcer_recibos_sueldo import main_parcer
import json
import os
import subprocess
import calendar
from datetime import datetime
from fastapi.responses import FileResponse



logger = logging.getLogger(__name__)
# Crea un enrutador para agrupar las rutas relacionadas con recibos.
router = APIRouter()
################################################################################################

# Ruta para obtener todos los recibos
@router.post('/todos_los_recibos', response_model=TodosLosRecibos_response)
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
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")  # Lanza una excepción con el mensaje de error.

################################################################################################

# Ruta para obtener todos los recibos
@router.post('/todosLosUsuarios', response_model=TodosLosUsuarios_response)
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
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")  # Lanza una excepción con el mensaje de error.

################################################################################################


  
@router.post("/recibo")
async def cambiar_estado_recibo(request: Recibo_request):
    """Endpoint para cambiar el estado de un recibo."""
    recibo = Recibo(id_recibo=request.id_recibo)
    
    # Cargar el estado actual del recibo (opcional, dependiendo de tu lógica)
    await recibo.cargar_estado()

    try:
        # Cambiar el estado del recibo
        resultado = await recibo.cambiar_estado(request.accion)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor.")
    
################################################################################################
@router.post("/download")
async def descargar_recibo(request: Download_Request):
    recibo = Recibo(id_recibo=request.id_recibo)
    await recibo.cargar_estado()

    try:
        # Obtener la ruta relativa del archivo desde el método download()
        archivo_relativo = await recibo.download()
        if not archivo_relativo:
            raise HTTPException(status_code=404, detail="Recibo no encontrado")

        # Convertir la ruta relativa en una ruta absoluta
        ruta_base = "/var/apps/pdf/sabana"  # Ruta base de los archivos PDF
        ruta_archivo = os.path.join(ruta_base, archivo_relativo.strip('/'))  # Construir la ruta absoluta

        # Verificar si el archivo existe
        if not os.path.exists(ruta_archivo):
            raise HTTPException(status_code=404, detail="Archivo no encontrado en el servidor")

        # Enviar el archivo como respuesta para descarga usando FileResponse
        return FileResponse(path=ruta_archivo, filename=os.path.basename(ruta_archivo), media_type='application/pdf')

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al descargar el recibo: {str(e)}")

################################################################################################

@router.post("/upload/")
async def upload_pdf(file: UploadFile = File(...),    action: str = Form(...)  # Campo para la acción
):
    
    if action == "validar":

        # Validar que solo se suba un archivo
        if isinstance(file, list) or not file:
            return {"error": "Debes subir un solo archivo."}

        # Validar que el archivo sea un PDF
        if file.content_type != 'application/pdf':
            return {"error": "Solo se permiten archivos PDF."}

        input_file_path = save_uploaded_file(file)  # Guardar archivo

        # Validar el PDF
        if not validate_pdf(input_file_path):
            logger.error("El PDF no es válido.")
            return {"error": "El PDF no es válido."}

        # Contar recibos usando el algoritmo
        count_result = count_recibos_in_pdf(input_file_path)
        count_data = json.loads(count_result)  # Convertir la salida de JSON a un diccionario
         # Diccionario con los nombres de los meses en español
        meses = {
                1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL", 
                5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO", 
                9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
            }

        def convertir_periodo(periodo):
            # Extraer mes y año del periodo
            mes = int(periodo[:2])  # '05' -> 5
            año = periodo[2:]       # '2024'
            # Obtener el nombre del mes en español
            nombre_mes = meses.get(mes, "MES INVÁLIDO")
            
            # Retornar el periodo en formato "MAYO 2024"
            return f"{nombre_mes} {año}"

        # Modificar el mensaje de respuesta
        response_message = {
            "Nombre del archivo ": file.filename,
            "Cantidad de recibos ": count_data.get('count', 0),
            "Periodo ": convertir_periodo(count_data.get('periodo', None))
}
        return response_message

    elif action == "procesar":
        sabana_file = "/var/apps/pdf/sabana/" + file.filename
        response, status_code = main_parcer(sabana_file, "/var/apps/pdf/sabana/")
        return JSONResponse(content=response, status_code=status_code)


################################################################################################



# Ruta para obtener todos los recibos
@router.post('/get_rol')
async def get_rol(request: GetRol_request, response: Response):
    token = request.token  # Obtiene el token de la solicitud.    
    if not token:  # Verifica si el token está presente en la solicitud.
        raise HTTPException(status_code=400, detail="Parámetro 'token' faltante.")  # Lanza una excepción si falta el token.    
    try:
        getRol = GetRol()  # Crea una instancia de la clase GetRol.
        resultado = await getRol.get_rol_function(token)  # Llama al método para obtener el rol con el token.        
        if resultado is None:  # Si la respuesta es None, probablemente la sesión expiró.
            return JSONResponse(content={"detail": "Session expired"}, status_code=400)        
        # Verifica si la respuesta contiene "rol" y "cuil"
        if "rol" in resultado and "cuil" in resultado:  
            #armado de respuesta 
                      
            #id_usuario = resultado["id_usuario"]
            cuil = resultado["cuil"]  # Asegúrate de que el CUIL se esté retornando correctamente
            rol = resultado["rol"]            
            nombre = resultado["nombre"]
            apellido = resultado["apellido"]
            legajo = resultado["legajo"]
            email = resultado["email"]      
            auth_token=resultado["auth_token"]
            # Establece el token como una cookie en la respuesta
            response.set_cookie(key="token",value=auth_token,httponly=True,secure=True,samesite="Lax")
            return {
            "cuil": cuil,
            "rol": rol,
            "auth_token": auth_token,
            "nombre": nombre,
            "apellido":apellido,
            "legajo":legajo,
            "email":email,
            "Recibos":resultado["recibos"] 
        }       
        # Si no se encuentran los valores esperados, devolver un error genérico
        raise HTTPException(status_code=404, detail="Datos del usuario no encontrados.")
    
    except Exception as e:  # Maneja cualquier excepción ocurrida durante el proceso.
        print(f"Error en get_rol: {e}")  # Imprime el error para depuración.
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")  # Lanza una excepción con el mensaje de error.

################################################################################################

@router.post("/login")
async def login(usuario: UsuarioLogin_request, response: Response):
    resultado = await Login.login_usuario(usuario.cuil, usuario.password)    
    # Verificamos si el resultado es un diccionario
    if isinstance(resultado, dict):
        # Manejo de los distintos casos devueltos
        if "code" in resultado:
            if resultado["code"] == 4:
                ###devolver el link para cambair el password
                raise HTTPException(status_code=401, detail="Proceso de cambio de contraseña activo")
            elif resultado["code"] == 2:
                raise HTTPException(status_code=401, detail="Se necesita validación de correo electrónico")
            elif resultado["code"] == 3:
                raise HTTPException(status_code=401, detail="Debe declarar su correo electrónico")
            elif resultado["code"] == 0:
                raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
            elif resultado["code"] == 50:
                raise HTTPException(status_code=403, detail="Usuario deshabilitado")        
        # Autenticación exitosa
        id_usuario = resultado["id_usuario"]
        cuil = resultado["cuil"]  # Asegúrate de que el CUIL se esté retornando correctamente
        rol = resultado["rol"]        
        nombre = resultado["nombre"]
        apellido = resultado["apellido"]
        legajo = resultado["legajo"]
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
            "legajo":legajo,
            "email":email,
            "Recibos":resultado["recibos"] 
        }
    
    # Si el resultado no es un diccionario, lanza un error de servidor
    raise HTTPException(status_code=500, detail="Error en la respuesta del servidor, no se pudo autenticar.")

################################################################################################

router.post("/validateTockenApi")
async def login(usuario: Usuario_request, response: Response):
    resultado = Login.login_usuario(usuario.cuil, usuario.password)
    # Verificamos si el resultado es un diccionario
    if isinstance(resultado, dict):
        # Manejo de los distintos casos devueltos
        if "code" in resultado:
            if resultado["code"] == 4:
                raise HTTPException(status_code=401, detail="Proceso de cambio de contraseña activo")
            elif resultado["code"] == 2:
                raise HTTPException(status_code=401, detail="Se necesita validación de correo electrónico")
            elif resultado["code"] == 3:
                raise HTTPException(status_code=401, detail="Debe declarar su correo electrónico")
            elif resultado["code"] == 0:
                raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
            elif resultado["code"] == 50:
                raise HTTPException(status_code=403, detail="Usuario deshabilitado")        
        # Autenticación exitosa
        id_usuario = resultado["id_usuario"]
        rol = resultado["rol"]
        cuil = resultado["cuil"]  # Asegúrate de que el CUIL se esté retornando correctamente
        auth_token = create_jwt_token(id_usuario, rol, cuil)  # Genera el token con el ID, rol y CUIL del usuario
        
        # Establece el token en la cabecera Set-Cookie
        response.set_cookie(key="auth_token", value=auth_token, httponly=True)  # Cambia httponly=True según tus necesidades

        # Devuelve la respuesta con el CUIL y el auth_token
        return {
            "cuil": cuil,
            "rol": rol,
            "auth_token": auth_token
        }
    
    # Si el resultado no es un diccionario, lanza un error de servidor
    raise HTTPException(status_code=500, detail="Error en la respuesta del servidor, no se pudo autenticar.")

################################################################################################

@router.post("/usuarios", response_model=dict)
async def gestionar_usuario(usuario_data: Usuario_request):
    print ("entro a usuario")
    try:
        if usuario_data.accion == "insert":
            # Acción para crear un nuevo usuario
            usuario = Usuario()  # Crear la instancia de Usuario
            response = await usuario.insert(
                nombre=usuario_data.nombre,
                apellido=usuario_data.apellido,
                cuil=usuario_data.cuil,
                legajo=usuario_data.legajo,
                email=usuario_data.email,
                habilitado=usuario_data.habilitado if usuario_data.habilitado is not None else 1  # Activado por defecto
            )
            return {
                "data": response             # Aquí asignas una clave "data" al valor correspondiente
                }
        
        elif usuario_data.accion == "update":
            
            # Acción para modificar un usuario existente
            if not usuario_data.id_usuario:
                raise HTTPException(status_code=400, detail="Se requiere el ID del usuario para actualizar.")
            usuario = Usuario(id_usuario=usuario_data.id_usuario)  # Cargar la instancia del usuario con su ID
            response = await usuario.update(
                nombre=usuario_data.nombre,
                apellido=usuario_data.apellido,
                cuil=usuario_data.cuil,
                legajo=usuario_data.legajo,
                email=usuario_data.email
            )            
            return {
                "data": response             # Aquí asignas una clave "data" al valor correspondiente
                }
        elif usuario_data.accion == "resetPassword":
            # Acción para modificar un usuario existente
            if not usuario_data.id_usuario:                
                raise HTTPException(status_code=400, detail="Se requiere el ID del usuario para reestablecer la contraseña.")
            usuario = Usuario(id_usuario=usuario_data.id_usuario)  # Cargar la instancia del usuario con su ID
            response = await usuario.resetPassword()  
            return {
                "data": response             # Aquí asignas una clave "data" al valor correspondiente
                }
        elif usuario_data.accion == "newPassword":
            print("entro a newPassword")
            # Acción para modificar un usuario existente
            if not usuario_data.id_usuario:                
                raise HTTPException(status_code=400, detail="Se requiere el ID del usuario para reestablecer la contraseña.")
            password=usuario_data.password
            password1=usuario_data.password1            
            usuario = Usuario(id_usuario=usuario_data.id_usuario)  # Cargar la instancia del usuario con su ID
            response = await usuario.newPassword(password,password1)  
            return {
                "data": response             # Aquí asignas una clave "data" al valor correspondiente
                }
            
        
        # elif usuario_data.accion == "activar":
        #     # Acción para activar un usuario
        #     if not usuario_data.id_usuario:
        #         raise HTTPException(status_code=400, detail="Se requiere el ID del usuario para cambiar el estado.")
        #     usuario = Usuario(id_usuario=usuario_data.id_usuario)  # Cargar la instancia del usuario con su ID
        #     response = await usuario.cambiar_estado(True)  # Activar el usuario (estado = True)
        #     return {"status": "success", "message": "Usuario activado exitosamente.", "data": response}
        
        # elif usuario_data.accion == "desactivar":
        #     # Acción para desactivar un usuario
        #     if not usuario_data.id_usuario:
        #         raise HTTPException(status_code=400, detail="Se requiere el ID del usuario para cambiar el estado.")
        #     usuario = Usuario(id_usuario=usuario_data.id_usuario)  # Cargar la instancia del usuario con su ID
        #     response = await usuario.cambiar_estado(False)  # Desactivar el usuario (estado = False)
        #     return {"status": "success", "message": "Usuario desactivado exitosamente.", "data": response}
        
        else:
            raise HTTPException(status_code=400, detail="Acción no válida. Las acciones permitidas son: 'insert', 'update', 'activar', 'desactivar'.")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
