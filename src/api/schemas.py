from pydantic import BaseModel,EmailStr, validator,Field,root_validator
from typing import Optional


#valido datos de entrada*****************************************************************
class Tabla_recibos_request(BaseModel):
    cuil: str
    periodo: str

class TodosLosRecibos_request(BaseModel):
    cuil: str
    
class DesactivaRecibos_request(BaseModel):
    id_recibo: str

class ActivaRecibos_request(BaseModel):
    id_recibo: str


class GetRol_request(BaseModel):
    token: str

class Recibo_request(BaseModel):
    accion: str
    id_recibo: str

class UsuarioLogin_request(BaseModel):
    cuil: str
    password: str

class TodosLosUsuarios_request(BaseModel):
    cuil: str

class Usuario_request(BaseModel):
    accion: str = Field(..., description="Acción a realizar", pattern='^(new|update|insert|habilitar|deshabilitar|resetPassword|newPassword)$')
    id_usuario: Optional[str] = None  # Opcional para crear un nuevo usuario
    cuil: Optional[str] = None  # Hacerlo opcional
    nombre: Optional[str] = None  # Hacerlo opcional
    apellido: Optional[str] = None  # Hacerlo opcional
    legajo: Optional[str] = None  # Hacerlo opcional
    password: Optional[str] = None  # Hacerlo opcional
    password1: Optional[str] = None  # Hacerlo opcional
    email: Optional[EmailStr] = None  # Hacerlo opcional   
    habilitado: int = 1  # Por defecto, habilitado es 1

    @validator('accion')
    def validar_accion(cls, v):
        if v not in ['new', 'update', 'insert', 'habilitar', 'deshabilitar', 'resetPassword', 'newPassword']:
            raise ValueError("La acción debe ser 'insert', 'update', 'resetPassword', 'habilitar' o 'deshabilitar', 'newPassword'.")
        return v  

    @root_validator(pre=True)
    def validar_datos_condicionales(cls, values):
        accion = values.get('accion')
        if accion == 'resetPassword':
            # Si es 'resetPassword', los campos pueden ser None
            values['email'] = None
            values['cuil'] = None
            values['nombre'] = None
            values['apellido'] = None
            values['legajo'] = None            
            values['password'] = None
            values['password1'] = None
            if accion == 'newPassword':
            # Si es 'resetPassword', los campos pueden ser None
                values['email'] = None
                values['cuil'] = None
                values['nombre'] = None
                values['apellido'] = None
                values['legajo'] = None
            else:
                # En otras acciones, el email es obligatorio
                if not values.get('email'):
                    raise ValueError("El email es obligatorio para esta acción.")
        return values  
    
class Download_Request(BaseModel):
    id_recibo: str

#valido datos de salida*********************************************************************

    
class TablaRecibos_response(BaseModel):
    descripcion_archivo: str
    periodo:str

         
class TodosLosRecibos_response(BaseModel):
    id_recibo:str
    periodo:str  
    fecha_subida:str
    descripcion_archivo:str
    estado:str
    
class ActivaRecibos_response(BaseModel):
    estado: str

class DesactivaRecibos_response(BaseModel):
    estado: str

# class GetRol_response(BaseModel):
#     cuil: str
#     rol: str
#     auth_token: str
#     nombre: str
#     apellido: str
#     legajo: str
#     email: str
#     token: str  # Campo 'token' requerido

class Recibo_response(BaseModel):
    estado: str
    id_recibo: str


class Usuario_response(BaseModel):
    rol: str
    cuil:str
    token: str
    nombre: str
    apellido:str
    legajo:str
    email:str
    recibos:str

class TodosLosUsuarios_response(BaseModel):
    id_usuario:str
    nombre: str
    apellido:str
    legajo:str
    email:str
    cuil:str 


class Download_response(BaseModel):
    id_recibo:str
    path: str
    filename: str
    media_type: str