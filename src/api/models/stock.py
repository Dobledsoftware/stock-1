from routers import conexion
from fastapi import HTTPException
from psycopg2.extras import DictCursor
from typing import Optional


class Stock(conexion.Conexion):
    async def entradaStock(self, id_producto: int, cantidad: int, operacion: str, id_usuario: int, observaciones: Optional[str]):
        """
        Ajusta el stock en la tabla 'stock' y registra el movimiento.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)

            # 1. Verificar si el producto existe
            sql_verificar_producto = "SELECT id_producto FROM productos WHERE id_producto = %s;"
            cursor.execute(sql_verificar_producto, (id_producto,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail=f"Producto con ID {id_producto} no encontrado.")

            # 2. Obtener stock actual
            sql_obtener_stock = "SELECT stock_actual FROM stock WHERE id_producto = %s;"
            cursor.execute(sql_obtener_stock, (id_producto,))
            stock_data = cursor.fetchone()
            if not stock_data:
                raise HTTPException(status_code=404, detail=f"No existe registro de stock para el producto {id_producto}.")

            stock_actual = stock_data["stock_actual"]

            # 3. Determinar nuevo stock
            if operacion == "incrementar":
                nuevo_stock = stock_actual + cantidad
            elif operacion == "disminuir":
                if stock_actual < cantidad:
                    raise HTTPException(status_code=400, detail="Stock insuficiente para realizar la disminución.")
                nuevo_stock = stock_actual - cantidad
            else:
                raise HTTPException(status_code=400, detail="Operación no válida.")

            # 4. Actualizar el stock
            sql_actualizar_stock = "UPDATE stock SET stock_actual = %s WHERE id_producto = %s;"
            cursor.execute(sql_actualizar_stock, (nuevo_stock, id_producto))

            # 5. Registrar el movimiento
            sql_registrar_movimiento = """
                INSERT INTO movimientos_stock (id_producto, cantidad, operacion, id_usuario, fecha_movimiento, observaciones)
                VALUES (%s, %s, %s, %s, NOW(), %s);
            """
            cursor.execute(sql_registrar_movimiento, (id_producto, cantidad, operacion, id_usuario, observaciones))

            # Guardar los cambios
            conexion.commit()

            return {"stock_actualizado": nuevo_stock}

        except Exception as e:
            conexion.rollback()
            raise HTTPException(status_code=500, detail=f"Error al ajustar stock: {str(e)}")
        finally:
            conexion.close()
