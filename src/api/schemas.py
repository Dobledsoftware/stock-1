from pydantic import BaseModel,EmailStr, validator,Field,root_validator
from typing import List, Optional
from enum import Enum
from datetime import datetime



#valido datos de entrada*****************************************************************
class Producto_request(BaseModel):
    accion: str
    id_producto: Optional[int] = None
    id_marca: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_venta_ars: Optional[float] = None  
    precio_venta_usd: Optional[float] = None 
    aplicar_incremento_automatico_ars: Optional[bool] = False 
    aplicar_incremento_automatico_usd: Optional[bool] = False 
    es_dolar: Optional[bool] = False 
    estado:Optional[bool] = True 
    codigo_barras: Optional[str] = None
    forceAdd: Optional[bool] = False  # Si el usuario desea agregar el producto aunque ya exista
    imagen_producto: Optional[str] = None  # URL de la imagen del producto
    id_categoria: Optional[int] = None
    id_usuario: Optional[int] = None

    
class TodosLosRecibos_response(BaseModel):
    id_recibo:str
    periodo:str  
    fecha_subida:str
    descripcion_archivo:str
    estado:str
class TodosLosRecibos_request(BaseModel):
    cuil: str
    

class GetRol_request(BaseModel):
    token: str    
class Download_Request(BaseModel):
    id_recibo: str
class Recibo_request(BaseModel):
    accion: str
    id_recibo: str



class Download_response(BaseModel):
    id_recibo:str
    path: str
    filename: str
    media_type: str
    # Definir un Enum para limitar las opciones válidas

class validateTockenApi(BaseModel):
    token:str
    id_usuario:str


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
    usuario: str
    password: str

class TodosLosUsuarios_request(BaseModel):
    usuario: str

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
    
# Definir el modelo para el movimiento de stock
class Movimiento(BaseModel):
    id_producto: int
    cantidad: int
    id_tipo_movimiento: int  # Ahora aceptamos el ID del tipo de movimiento
    id_usuario: int
    id_proveedor: int
    id_almacen: int
    id_estante: int
    precio_costo_ars: float
    precio_costo_usd: float
    descripcion: str

# Modelo de la solicitud
class movimientoStockRequest(BaseModel):
    movimientos: List[Movimiento]


    
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
# Modelo para modificar usuario

class UsuarioEditRequest(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    usuario: str

# Modelo para deshabilitar usuario
class UsuarioDeshabilitarRequest(BaseModel):
    id_usuario: int


class PerfilRequest(BaseModel):
    nombre: str
    descripcion: str

class UsuarioResponse(BaseModel):
    id_usuario: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    cuil: Optional[str] = None
    email: Optional[str] = None
    fecha_creacion: Optional[datetime] = None  # Cambié esto a datetime
    estado: Optional[str] = None

    class Config:
        orm_mode = True




class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    usuario: str
    password: str

class UsuarioResponse(BaseModel):
    message: str
    id_usuario: int
    code: int       