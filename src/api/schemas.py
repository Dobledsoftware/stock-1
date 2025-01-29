from pydantic import BaseModel,EmailStr, validator,Field,root_validator
from typing import List, Optional
from enum import Enum
from datetime import datetime



#valido datos de entrada*****************************************************************
class AccionStock(str, Enum):
    incrementar = "incrementar"
    disminuir = "disminuir"


class Producto_request(BaseModel):
    accion: str
    id_producto: Optional[int] = None
    id_marca: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None  
    estado:Optional[bool] = True 
    codigo_barras: Optional[str] = None
    forceAdd: Optional[bool] = False  # Si el usuario desea agregar el producto aunque ya exista
    accion_stock: Optional[AccionStock] = None  # Opción de incremento/disminución de stock
    imagen_producto: Optional[str] = None  # URL de la imagen del producto
    id_categoria: Optional[int] = None
    id_usuario: Optional[int] = None



    # Definir un Enum para limitar las opciones válidas




class Proveedor_request(BaseModel):
    accion: str
    id_proveedor: Optional[int] = None
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None 
    correo_contacto: Optional[str] = None 
    estado:Optional[bool] = True
    incluir_inactivas:Optional[bool] = True 


class Almacen_request(BaseModel):
    accion: str
    id_almacen: Optional[int] = None
    descripcion: Optional[str] = None
    estado:Optional[bool] = True
    incluir_inactivas:Optional[bool] = True 
    estado:Optional[bool] = True 


class Estante_request(BaseModel):
    accion: str
    id_estante: Optional[int] = None
    id_almacen: Optional[int] = None
    descripcion: Optional[str] = None
    estado:Optional[bool] = True
    incluir_inactivas:Optional[bool] = True 
    estado:Optional[bool] = True 


class Categoria_request(BaseModel):
    accion: str
    id_categoria: Optional[int] = None
    descripcion: Optional[str] = None
    estado:Optional[bool] = True 
    observaciones: Optional[str] = None
    incluir_inactivas:Optional[bool] = True 



class Marca_request(BaseModel):
    accion: str
    id_marca: Optional[int] = None
    descripcion: Optional[str] = None
    estado:Optional[bool] = True 
    observaciones: Optional[str] = None
    incluir_inactivas:Optional[bool] = True 

    
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
    


class MovimientoStock(BaseModel):
    id_stock: Optional[int] = None
    id_producto: int
    cantidad: int
    operacion: str  # Puede ser "incrementar" o "disminuir"
    id_usuario: Optional[int]
    observaciones: Optional[str] = None    
    id_proveedor: int
    id_almacen: int
    id_estante: int
    descripcion: Optional[str]
    stock_actual: Optional[int] = None
    stock_minimo: Optional[int] = None
    stock_maximo: Optional[int] = None
    id_stock_movimiento: Optional[int] = None
    id_tipo_movimiento: Optional[int] = None
    
    
    
    

class Stock_request(BaseModel):
    movimientos: List[MovimientoStock]

    
#valido datos de salida*********************************************************************

class Producto_response(BaseModel):
    estado: str
    id_productto: str

class Proveedor_response(BaseModel):
    estado: str
    id_proveedor: str



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

# Esquema de salida (respuesta)
class Stock_response(BaseModel):
    id_producto: int
    stock_actualizado: int
    accion_realizada: str
    mensaje: str



    # Esquema de consulta de stock (salida)
class StockResponse(BaseModel):
    id_stock: int
    id_producto: int
    nombre_producto: str
    stock_actual: int
    stock_minimo: int
    stock_maximo: int
    id_almacen: int
    id_proveedor: int
    fecha_alta: datetime  # Fecha con tipo datetime
    id_estante: int
    estado: str
    cantidad: Optional[int] = None  # Hacer que 'cantidad' sea opcional

class MovimientoStockResponse(BaseModel):
    id_stock_movimiento: int
    id_stock: int
    cantidad: int
    fecha_movimiento: str  # Esto será una cadena, no un datetime
    id_usuario: int
    id_proveedor: int
    descripcion: str
    id_tipo_movimiento: int
    id_producto: int  # Asegúrate de que esté presente en el modelo
    operacion: str  # Asegúrate de que esté presente en el modelo

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        obj_dict = obj.__dict__
        # Convertir fecha_movimiento a cadena ISO
        if isinstance(obj_dict.get('fecha_movimiento'), datetime):
            obj_dict['fecha_movimiento'] = obj_dict['fecha_movimiento'].isoformat()
        # Asegúrate de que el resto de los campos también se conviertan correctamente
        return super().from_orm(obj)

# Esquema de consulta de movimientos de stock (salida)
class FiltrosStock(BaseModel):
    id_producto: Optional[int] = None
    id_almacen: Optional[int] = None
    estado: Optional[bool]= True
    id_usuario: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
