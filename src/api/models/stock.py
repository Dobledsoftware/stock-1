from routers import conexion
from fastapi import HTTPException
from psycopg2.extras import DictCursor
from typing import Optional
from datetime import datetime



class Stock(conexion.Conexion):
    async def entradaStock(self, id_producto, cantidad, id_usuario, id_proveedor, id_almacen, id_estante, descripcion, operacion):
        """
        Ajusta el stock en la tabla 'stock' y registra el movimiento.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)
            print("entra a la funcion entradaStock")
            
            # 1. Verificar si el producto existe
            sql_verificar_producto = "SELECT id_producto FROM productos WHERE id_producto = %s;"
            cursor.execute(sql_verificar_producto, (id_producto,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail=f"Producto con ID {id_producto} no encontrado.")

            # 2. Verificar si existe un registro de stock
            sql_obtener_stock = "SELECT id_stock, stock_actual FROM stock WHERE id_producto = %s;"
            cursor.execute(sql_obtener_stock, (id_producto,))
            stock_data = cursor.fetchone()

            if stock_data:
                # Si existe el stock, obtener los datos
                id_stock = stock_data["id_stock"]
                stock_actual = stock_data["stock_actual"]

                # 3. Determinar el nuevo stock
                if operacion == "incrementar":
                    nuevo_stock = stock_actual + cantidad
                elif operacion == "disminuir":
                    if stock_actual < cantidad:
                        raise HTTPException(status_code=400, detail="Stock insuficiente para realizar la disminución.")
                    nuevo_stock = stock_actual - cantidad
                else:
                    raise HTTPException(status_code=400, detail="Operación no válida.")

                # 4. Actualizar el stock
                sql_actualizar_stock = "UPDATE stock SET stock_actual = %s WHERE id_stock = %s;"
                cursor.execute(sql_actualizar_stock, (nuevo_stock, id_stock))
            else:
                # Si no existe, crear el registro de stock
                sql_crear_stock = """
                    INSERT INTO stock (
                        id_producto, stock_actual, stock_minimo, stock_maximo, 
                        id_almacen, id_proveedor, id_estante, estado, fecha_alta
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, true, NOW())
                    RETURNING id_stock;
                """
                cursor.execute(sql_crear_stock, (id_producto, cantidad, 0, 0, id_almacen, id_proveedor, id_estante))
                id_stock = cursor.fetchone()["id_stock"]

            # 5. Registrar el movimiento
            sql_registrar_movimiento = """
                INSERT INTO stock_movimientos (
                    id_stock, cantidad, fecha_movimiento, id_usuario, 
                    id_proveedor, descripcion, id_tipo_movimiento
                )
                VALUES (%s, %s, NOW(), %s, %s, %s, %s);
            """
            id_tipo_movimiento = 1 if operacion == "incrementar" else 2  # 1: ingreso, 2: salida
            cursor.execute(sql_registrar_movimiento, (id_stock, cantidad, id_usuario, id_proveedor, descripcion, id_tipo_movimiento))

            # Guardar los cambios
            conexion.commit()
            return {"id_producto": id_producto, "stock_actualizado": nuevo_stock if stock_data else cantidad}

        except Exception as e:
            conexion.rollback()
            raise HTTPException(status_code=500, detail=f"Error al ajustar stock: {str(e)}")
        finally:
            conexion.close()

###############################obtener_movimientos########################################################


    async def obtener_movimientos(self,id_producto=None, id_usuario=None, fecha_inicio=None, fecha_fin=None):
        """
        Consulta la tabla 'stock_movimientos' con filtros opcionales.
        """
        conexion = self.conectar()

        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql_query = """
                SELECT *
                FROM stock_movimientos
                WHERE 1=1
            """
            params = []

            if id_producto is not None:
                sql_query += " AND id_stock IN (SELECT id_stock FROM stock WHERE id_producto = %s)"
                params.append(id_producto)
            if id_usuario is not None:
                sql_query += " AND id_usuario = %s"
                params.append(id_usuario)
            if fecha_inicio is not None and fecha_fin is not None:
                sql_query += " AND fecha_movimiento BETWEEN %s AND %s"
                params.extend([fecha_inicio, fecha_fin])
            elif fecha_inicio is not None:
                sql_query += " AND fecha_movimiento >= %s"
                params.append(fecha_inicio)
            elif fecha_fin is not None:
                sql_query += " AND fecha_movimiento <= %s"
                params.append(fecha_fin)

            cursor.execute(sql_query, params)
            resultados = cursor.fetchall()

            if not resultados:
                raise HTTPException(status_code=404, detail="No se encontraron registros en 'stock_movimientos'.")

            return [dict(row) for row in resultados]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al consultar 'stock_movimientos': {str(e)}")
        finally:
            conexion.close()


    ###############################obtener_stock########################################################

    async def obtener_movimientos(self, id_producto=None, id_usuario=None, fecha_inicio=None, fecha_fin=None):
        """
        Consulta la tabla 'stock_movimientos' con filtros opcionales.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql_query = "SELECT * FROM stock_movimientos WHERE 1=1"
            params = []

            if id_producto is not None:
                sql_query += " AND id_producto = %s"
                params.append(id_producto)
            if id_usuario is not None:
                sql_query += " AND id_usuario = %s"
                params.append(id_usuario)
            if fecha_inicio is not None:
                sql_query += " AND fecha_movimiento >= %s"
                params.append(fecha_inicio)
            if fecha_fin is not None:
                sql_query += " AND fecha_movimiento <= %s"
                params.append(fecha_fin)

            cursor.execute(sql_query, params)
            resultados = cursor.fetchall()

            if not resultados:
                raise HTTPException(status_code=404, detail="No se encontraron registros en 'stock_movimientos'.")

            # Asegúrate de que la fecha se convierte correctamente a string
            return [
                {
                    **dict(row),  # Devolver todas las columnas
                    "fecha_movimiento": row["fecha_movimiento"].isoformat() if isinstance(row["fecha_movimiento"], datetime) else row["fecha_movimiento"]
                }
                for row in resultados
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al consultar la tabla 'stock_movimientos': {str(e)}")
        finally:
            conexion.close()
