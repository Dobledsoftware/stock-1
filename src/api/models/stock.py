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
            # Paso A: Obtener el nuevo identificador_evento desde la base de datos funciona aunque el valor sea null la primera ves que se inicialice el software.
            sql_obtener_identificador_evento = """
                SELECT COALESCE(MAX(identificador_evento), 0) + 1 AS nuevo_identificador_evento 
                FROM stock_movimientos;
            """
            cursor.execute(sql_obtener_identificador_evento)
            identificador_evento = cursor.fetchone()["nuevo_identificador_evento"]

            # Paso B: Registrar cada producto en el movimiento
            sql_registrar_movimiento = """
                INSERT INTO stock_movimientos (
                    id_stock, cantidad, fecha_movimiento, id_usuario, 
                    id_proveedor, descripcion, id_tipo_movimiento, identificador_evento
                )
                VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s);
            """

            id_tipo_movimiento = 1 if operacion == "incrementar" else 2  # 1: ingreso, 2: salida
            cursor.execute(
                sql_registrar_movimiento,
                (id_stock, cantidad, id_usuario, id_proveedor, descripcion, id_tipo_movimiento, identificador_evento)
            )

            # Guardar los cambios
            conexion.commit()
            return {"id_producto": id_producto, "stock_actualizado": nuevo_stock if stock_data else cantidad}

        except Exception as e:
            conexion.rollback()
            raise HTTPException(status_code=500, detail=f"Error al ajustar stock: {str(e)}")
        finally:
            conexion.close()

###############################obtener_movimientos########################################################


    async def obtener_stock(self, id_producto=None, id_almacen=None, estado=None):
        """
        Consulta la tabla 'stock' con filtros opcionales. Si no se pasan filtros, se devuelven todos los registros.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql_query = """SELECT 
            s.id_stock,
            s.id_producto,
            p.nombre as nombre_producto,
            p.descripcion as descripcion_producto,
            s.stock_actual,
            s.stock_minimo,
            s.stock_maximo,
            s.id_almacen,
            s.id_proveedor,
            prov.nombre as nombre_proveedor,
            a.descripcion as almacen_descripcion,
            s.id_estante,
            e.descripcion as descripcion_estante  
            FROM 
            stock s 
            left join 
            productos p on p.id_producto = s.id_producto
            left join 
            proveedores prov on s.id_proveedor = prov.id_proveedor 
            left join 
            almacen a on a.id_almacen = s.id_almacen
            left join 
            almacen_estante e on e.id_estante = s.id_estante
            WHERE 1=1"""  # Comienza con una consulta general
            params = []        

            cursor.execute(sql_query, params)
            resultados = cursor.fetchall()

            if not resultados:
                raise HTTPException(status_code=404, detail="No se encontraron registros en 'stock'.")

            return [dict(row) for row in resultados]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al consultar la tabla 'stock': {str(e)}")
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
            sql_query = """SELECT
            
            sm.id_stock_movimiento,
            sm.cantidad,
            sm.descripcion,
            sm.fecha_movimiento as fecha_movimiento,
            stm.descripcion as tipo_movimiento,
            p.nombre as nombre_producto,
            p.descripcion as descripcion_producto, 
            producto_marca.descripcion as marca_producto



            FROM stock_movimientos sm

            left join 
            stock s on s.id_stock = sm.id_stock
            left join 
            stock_tipo_movimiento stm on stm.id_tipo_movimiento = sm.id_tipo_movimiento
            left join 
            productos p on p.id_producto = s.id_producto 
            left join producto_marca on producto_marca.id_marca = p.id_marca
                  
            WHERE 1=1"""
            params = []


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

############################salidaStock####################################################################

async def salidaStock(self, id_producto, cantidad, id_usuario, id_proveedor, descripcion):
    """
    Realiza la salida de stock y registra el movimiento correspondiente.
    """
    conexion = self.conectar()
    try:
        cursor = conexion.cursor(cursor_factory=DictCursor)
        print("entra a la función salidaStock")
        
        # 1. Verificar si el producto existe
        sql_verificar_producto = "SELECT id_producto FROM productos WHERE id_producto = %s;"
        cursor.execute(sql_verificar_producto, (id_producto,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Producto con ID {id_producto} no encontrado.")
        
        # 2. Verificar si existe un registro de stock
        sql_obtener_stock = "SELECT id_stock, stock_actual FROM stock WHERE id_producto = %s;"
        cursor.execute(sql_obtener_stock, (id_producto,))
        stock_data = cursor.fetchone()
        
        if not stock_data:
            raise HTTPException(status_code=404, detail="No existe stock registrado para el producto.")
        
        # Si existe el stock, obtener los datos
        id_stock = stock_data["id_stock"]
        stock_actual = stock_data["stock_actual"]
        
        # 3. Verificar y calcular el nuevo stock
        if stock_actual < cantidad:
            raise HTTPException(status_code=400, detail="Stock insuficiente para realizar la salida.")
        
        nuevo_stock = stock_actual - cantidad
        
        # 4. Actualizar el stock
        sql_actualizar_stock = "UPDATE stock SET stock_actual = %s WHERE id_stock = %s;"
        cursor.execute(sql_actualizar_stock, (nuevo_stock, id_stock))
        
        # 5. Registrar el movimiento
        sql_registrar_movimiento = """
            INSERT INTO stock_movimientos (
                id_stock, cantidad, fecha_movimiento, id_usuario, 
                id_proveedor, descripcion, id_tipo_movimiento
            )
            VALUES (%s, %s, NOW(), %s, %s, %s, %s);
        """
        id_tipo_movimiento = 2  # 2: salida
        cursor.execute(sql_registrar_movimiento, (id_stock, cantidad, id_usuario, id_proveedor, descripcion, id_tipo_movimiento))
        
        # Guardar los cambios
        conexion.commit()
        return {"id_producto": id_producto, "stock_actualizado": nuevo_stock}

    except Exception as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al realizar salida de stock: {str(e)}")
    finally:
        conexion.close()