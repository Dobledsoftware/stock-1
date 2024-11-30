from pydantic import BaseModel,EmailStr, validator,Field,root_validator
from typing import Optional


#valido datos de entrada*****************************************************************

class Producto_request(BaseModel):
    accion: str
    id_producto: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock_actual: Optional[int] = None
    proveedor_id: Optional[int] = None
    estado: Optional[str] = None
    
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
    
#valido datos de salida*********************************************************************

class Producto_response(BaseModel):
    estado: str
    id_productto: str


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
