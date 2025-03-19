from fastapi import Body,APIRouter, HTTPException, UploadFile, File, Form, Query  # Importa APIRouter para crear grupos de rutas y HTTPException para manejar errores.
from fastapi.responses import JSONResponse, Response  # Importa JSONResponse para devolver respuestas JSON personalizadas.
from pydantic import BaseModel  # Importa BaseModel para definir esquemas de solicitudes y respuestas.
#importa las clases
from models.todosLosUsuarios import TodosLosUsuarios
from models.usuario import Usuario  # Importar tu clase Usuario
#from .usuario import Usuario # Importa Clase Recibo
from models.login import Login # Importa Clase Recibo
from models.getRol import GetRol  # Importa la clase 
from models.validateTokenApi import Token
from models.perfil import Perfil
from models.stock import Stock
from models.ventas import Ventas

from models.rol import validar_token_con_roles
from typing import List,Dict,Optional

#importa los schemas
from schemas import   PerfilRequest,UsuarioEditRequest,UsuarioLogin_request,GetRol_request,TodosLosRecibos_request,TodosLosRecibos_response,Usuario_request,Download_Request,Download_response,validateTockenApi
import logging

import aiohttp

logger = logging.getLogger(__name__)
# Crea un enrutador para agrupar las rutas relacionadas con recibos.
router = APIRouter()


##################################validar_stock######################################
router = APIRouter(tags=["Ventas"])

router = APIRouter(tags=["Ventas"])
ventas = Ventas()  # Instancia de la clase Ventas

@router.get("/validar_stock")
async def validar_stock(
    id_producto: Optional[int] = Query(None, description="ID del producto a validar"),
    codigo_barras: Optional[str] = Query(None, description="Código de barras del producto a validar"),
    cantidad: int = Query(1, description="Cantidad deseada para la venta"),
    id_proveedor: Optional[int] = Query(None, description="Filtrar por proveedor (opcional)"),
    id_almacen: Optional[int] = Query(None, description="Filtrar por almacén (opcional)")
):
    """
    ✅ **Endpoint que valida si hay stock suficiente antes de realizar una venta.**
    📌 Solo llama a `Ventas.validar_stock()`.
    """
    return await ventas.validar_stock(id_producto, codigo_barras, cantidad, id_proveedor, id_almacen)

#############################ventas###########################################


@router.post("/ventas")
async def registrar_venta(
    id_usuario: int = Body(..., description="ID del usuario que realiza la venta"),
    productos: List[Dict] = Body(..., description="Lista de productos vendidos (id_producto, cantidad)")
):
    """
    ✅ **Registra una venta y descuenta el stock.**  
    📌 Ahora valida el stock dentro del backend ANTES de registrar la venta.
    
    **Ejemplo de Request Body:**  
    ```json
    {
        "id_usuario": 2,
        "productos": [
            {"id_producto": 1, "cantidad": 3},
            {"id_producto": 2, "cantidad": 2}
        ]
    }
    ```
    """
    return await ventas.registrar_venta(id_usuario, productos)





@router.get("/ventas/{id_venta}/ticket", tags=["Ventas"])
async def obtener_ticket_venta(id_venta: int):
    """
    ✅ **Obtiene los detalles de una venta y genera un ticket de comprobante.**
    
    **Ejemplo de respuesta:**  
    ```json
    {
        "id_venta": 1,
        "id_usuario": 1,
        "fecha": "2024-03-10T14:00:00",
        "total_venta": 3500,
        "productos": [
            {"id_producto": 1, "nombre": "Zapatillas Air Max", "cantidad": 3, "precio_unitario": 115},
            {"id_producto": 2, "nombre": "Camiseta Nike", "cantidad": 2, "precio_unitario": 50}
        ]
    }
    ```
    """
    stock = Stock()
    conexion = stock.conectar()
    cursor = conexion.cursor()
    
    try:
        sql_venta = "SELECT id_usuario, total_venta, fecha FROM ventas WHERE id_venta = %s;"
        cursor.execute(sql_venta, (id_venta,))
        venta = cursor.fetchone()

        if not venta:
            raise HTTPException(status_code=404, detail="Venta no encontrada")

        id_usuario, total_venta, fecha = venta

        sql_detalles = """
            SELECT v.id_producto, p.nombre, v.cantidad, v.precio_unitario
            FROM ventas_detalles v
            JOIN productos p ON p.id_producto = v.id_producto
            WHERE id_venta = %s;
        """
        cursor.execute(sql_detalles, (id_venta,))
        productos = cursor.fetchall()

        return {
            "id_venta": id_venta,
            "id_usuario": id_usuario,
            "fecha": fecha.isoformat(),
            "total_venta": total_venta,
            "productos": [{"id_producto": p[0], "nombre": p[1], "cantidad": p[2], "precio_unitario": p[3]} for p in productos]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el ticket: {str(e)}")
    finally:
        conexion.close()