from fastapi import HTTPException
import aiohttp
from typing import Optional, List, Dict
from routers import conexion

class Ventas(conexion.Conexion):

    async def validar_stock(self, id_producto: Optional[int], codigo_barras: Optional[str], cantidad: int, id_proveedor: Optional[int], id_almacen: Optional[int]):
        """
        ✅ **Valida si hay stock suficiente antes de realizar una venta.**
        📌 Si el producto no está en `stock`, devuelve `"Producto sin stock"`.
        📌 Maneja casos donde `/inventario` devuelve `"nombre_producto": "Producto sin stock"`.
        """
        if not id_producto and not codigo_barras:
            raise HTTPException(status_code=400, detail="Debe proporcionar 'id_producto' o 'codigo_barras'.")

        try:
            # Construir la URL para consultar /inventario
            url = "http://localhost:8000/inventario?"
            if id_producto:
                url += f"id_producto={id_producto}&"
            if codigo_barras:
                url += f"codigo_barras={codigo_barras}&"

            # Llamar a /inventario
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return {"status": "error", "message": "Producto sin stock"}
                    inventario_data = await response.json()

            # **Caso 1: `/inventario` devuelve "Producto sin stock"**
            if isinstance(inventario_data, list) and len(inventario_data) == 1 and "nombre_producto" in inventario_data[0] and inventario_data[0]["nombre_producto"] == "Producto sin stock":
                return {"status": "error", "message": "Producto sin stock en inventario."}
            # **Caso 2: El producto tiene stock pero hay variantes sin stock**
            inventario_data = [item for item in inventario_data if item.get("stock_actual", 0) > 0]

            # **Caso 3: Aplicar filtros de proveedor o almacén**
            if id_proveedor:
                inventario_data = [item for item in inventario_data if item.get("id_proveedor") == id_proveedor]
            if id_almacen:
                inventario_data = [item for item in inventario_data if item.get("id_almacen") == id_almacen]

            # **Caso 4: Si después del filtrado no hay stock, devolver "Stock insuficiente"**
            if not inventario_data:
                return {"status": "error", "message": "Stock insuficiente o variante no disponible."}

            # **Caso 5: Hay stock disponible**
            stock_disponible = sum(item["stock_actual"] for item in inventario_data)

            if stock_disponible < cantidad:
                return {"status": "error", "message": f"Stock insuficiente. Disponible: {stock_disponible}"}

            return {
                "status": "success",
                "message": "Stock suficiente para la venta.",
                "stock_disponible": stock_disponible,
                "detalles_variantes": inventario_data  # Devuelve solo variantes con stock
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al validar stock desde /inventario: {str(e)}")



    async def registrar_venta(self, id_usuario: int, productos: List[Dict]):
        """ ✅ **Registra una venta solo si hay stock disponible y el usuario existe.** """
        try:
            conexion = self.conectar()
            cursor = conexion.cursor()

            # **Verificar si el usuario existe en la tabla `usuarios`**
            cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s;", (id_usuario,))
            usuario_existente = cursor.fetchone()

            if not usuario_existente:
                raise HTTPException(status_code=400, detail=f"El usuario con ID {id_usuario} no existe en la base de datos.")

            total_venta = 0

            print("entra", productos)  # Log para depuración

            # **Validar stock antes de registrar la venta**
            for producto in productos:
                id_producto = producto.get("id_producto")
                codigo_barras = producto.get("codigo_barras")
                cantidad = producto["cantidad"]

                # **Si no tenemos id_producto, lo buscamos por código de barras en productos**
                if not id_producto and codigo_barras:
                    cursor.execute("SELECT id_producto FROM productos WHERE codigo_barras = %s;", (codigo_barras,))
                    producto_data = cursor.fetchone()
                    if producto_data:
                        id_producto = producto_data[0]
                    else:
                        raise HTTPException(status_code=400, detail=f"Producto con código de barras {codigo_barras} no encontrado.")

                stock_valido = await self.validar_stock(
                    id_producto=id_producto,
                    codigo_barras=None,  # Ya obtenemos id_producto, así que no usamos código de barras en stock
                    cantidad=cantidad,
                    id_proveedor=None,
                    id_almacen=None
                )

                if stock_valido["status"] == "error":
                    raise HTTPException(status_code=400, detail=stock_valido["message"])

            # **Registrar la venta en la base de datos**
            sql_insert_venta = "INSERT INTO ventas (id_usuario, total_venta) VALUES (%s, %s) RETURNING id_venta;"
            cursor.execute(sql_insert_venta, (id_usuario, total_venta))
            id_venta = cursor.fetchone()[0]

            # **Registrar detalles de la venta y descontar stock**
            for producto in productos:
                id_producto = producto.get("id_producto")  
                codigo_barras = producto.get("codigo_barras")
                cantidad = producto["cantidad"]

                # **Si no tenemos id_producto, lo buscamos por código de barras en productos**
                if not id_producto and codigo_barras:
                    cursor.execute("SELECT id_producto FROM productos WHERE codigo_barras = %s;", (codigo_barras,))
                    producto_data = cursor.fetchone()
                    if producto_data:
                        id_producto = producto_data[0]
                    else:
                        raise HTTPException(status_code=400, detail=f"Producto con código de barras {codigo_barras} no encontrado.")

                # **Buscar stock solo por id_producto**
                cursor.execute("""
                    SELECT id_stock, precio_costo_ars FROM stock
                    WHERE id_producto = %s AND stock_actual > 0
                    ORDER BY fecha_ingreso ASC LIMIT 1;
                """, (id_producto,))
                stock_data = cursor.fetchone()

                if not stock_data:
                    raise HTTPException(status_code=400, detail=f"Stock insuficiente para producto {id_producto or codigo_barras}")

                id_stock, precio_costo = stock_data
                cursor.execute("UPDATE stock SET stock_actual = stock_actual - %s WHERE id_stock = %s;", (cantidad, id_stock))

                sql_insert_detalle = """
                    INSERT INTO ventas_detalles (id_venta, id_stock, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s);
                """
                cursor.execute(sql_insert_detalle, (id_venta, id_stock, cantidad, precio_costo))
                total_venta += precio_costo * cantidad

            cursor.execute("UPDATE ventas SET total_venta = %s WHERE id_venta = %s;", (total_venta, id_venta))
            conexion.commit()

            return {"status": "success", "message": "Venta registrada con éxito", "id_venta": id_venta}

        except Exception as e:
            conexion.rollback()
            raise HTTPException(status_code=500, detail=f"Error al registrar la venta: {str(e)}")

        finally:
            cursor.close()
            conexion.close()
