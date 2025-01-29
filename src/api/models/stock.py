from routers import conexion
from fastapi import HTTPException
from psycopg2.extras import DictCursor
from typing import Optional
from datetime import datetime


class Stock(conexion.Conexion):
    async def entradaStock(self, productos, id_usuario, id_proveedor, id_almacen, id_estante, descripcion, operacion, identificador_evento):
        """
        Ajusta el stock en la tabla 'stock' y registra el movimiento.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)

            # Si no se ha recibido un identificador de evento, lo generamos
            if identificador_evento is None:
                sql_obtener_identificador_evento = """
                    SELECT COALESCE(MAX(identificador_evento), 0) + 1 AS nuevo_identificador_evento 
                    FROM stock_movimientos;
                """
                cursor.execute(sql_obtener_identificador_evento)
                identificador_evento = cursor.fetchone()["nuevo_identificador_evento"]

            print(f"Identificador de evento global: {identificador_evento}")  # Debugging

            for producto in productos:
                id_producto = producto["id_producto"]
                cantidad = producto["cantidad"]

                # Verificar si el producto existe
                sql_verificar_producto = "SELECT id_producto FROM productos WHERE id_producto = %s;"
                cursor.execute(sql_verificar_producto, (id_producto,))
                if not cursor.fetchone():
                    raise HTTPException(status_code=404, detail=f"Producto con ID {id_producto} no encontrado.")

                # Verificar si existe un registro de stock
                sql_obtener_stock = "SELECT id_stock, stock_actual FROM stock WHERE id_producto = %s;"
                cursor.execute(sql_obtener_stock, (id_producto,))
                stock_data = cursor.fetchone()

                if stock_data:
                    id_stock = stock_data["id_stock"]
                    stock_actual = stock_data["stock_actual"]

                    # Determinar el nuevo stock
                    if operacion == "incrementar":
                        nuevo_stock = stock_actual + cantidad
                    elif operacion == "disminuir":
                        if stock_actual < cantidad:
                            raise HTTPException(status_code=400, detail="Stock insuficiente.")
                        nuevo_stock = stock_actual - cantidad
                    else:
                        raise HTTPException(status_code=400, detail="Operación no válida.")

                    # Actualizar el stock
                    sql_actualizar_stock = "UPDATE stock SET stock_actual = %s WHERE id_stock = %s;"
                    cursor.execute(sql_actualizar_stock, (nuevo_stock, id_stock))
                else:
                    # Crear el registro de stock
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

                # Registrar el movimiento
                sql_registrar_movimiento = """
                    INSERT INTO stock_movimientos (
                        id_stock, cantidad, fecha_movimiento, id_usuario, 
                        id_proveedor, descripcion, id_tipo_movimiento, identificador_evento
                    )
                    VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s);
                """
                id_tipo_movimiento = 1 if operacion == "incrementar" else 2
                cursor.execute(
                    sql_registrar_movimiento,
                    (id_stock, cantidad, id_usuario, id_proveedor, descripcion, id_tipo_movimiento, identificador_evento)
                )

            conexion.commit()
            return {"status": "success", "mensaje": "Operación completada.", "identificador_evento": identificador_evento}

        except Exception as e:
            conexion.rollback()
            raise HTTPException(status_code=500, detail=f"Error al ajustar stock: {str(e)}")
        finally:
            conexion.close()
###############################obtener_movimientos########################################################


    async def obtener_stock(
        self, 
        id_producto=None, 
        id_almacen=None, 
        estado=None, 
        codigo_barras=None, 
        nombre=None
    ):
        """
        Consulta la tabla 'stock' con filtros opcionales. Si no se pasan filtros, se devuelven todos los registros.
        Si no se encuentra un producto, se muestra "Producto sin stock".
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql_query = """
            SELECT 
                s.id_stock,
                s.id_producto,
                p.nombre AS nombre_producto,
                p.descripcion AS descripcion_producto,
                p.codigo_barras,
                s.stock_actual,
                s.stock_minimo,
                s.stock_maximo,
                s.id_almacen,
                s.id_proveedor,
                prov.nombre AS nombre_proveedor,
                a.descripcion AS almacen_descripcion,
                s.id_estante,
                e.descripcion AS descripcion_estante  
            FROM 
                stock s
            LEFT JOIN 
                productos p ON p.id_producto = s.id_producto
            LEFT JOIN 
                proveedores prov ON s.id_proveedor = prov.id_proveedor 
            LEFT JOIN 
                almacen a ON a.id_almacen = s.id_almacen
            LEFT JOIN 
                almacen_estante e ON e.id_estante = s.id_estante
            WHERE 1=1
            """
            params = []

            # Filtros dinámicos
            if id_producto:
                sql_query += " AND s.id_producto = %s"
                params.append(id_producto)
            if id_almacen:
                sql_query += " AND s.id_almacen = %s"
                params.append(id_almacen)
            if estado:
                sql_query += " AND s.estado = %s"
                params.append(estado)
            if codigo_barras:
                sql_query += " AND p.codigo_barras = %s"
                params.append(codigo_barras)
            if nombre:
                sql_query += " AND p.nombre ILIKE %s"
                params.append(f"%{nombre}%")  # Usamos ILIKE para una búsqueda insensible a mayúsculas

            cursor.execute(sql_query, params)
            resultados = cursor.fetchall()

            # Si no hay resultados, devolvemos "Producto sin stock"
            if not resultados:
                return [{"nombre_producto": "Producto sin stock"}]

            return [dict(row) for row in resultados]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al consultar la tabla 'stock': {str(e)}")
        finally:
            conexion.close()


    ###############################obtener_stock########################################################

    async def obtener_movimientos(self, id_producto=None, id_usuario=None, fecha_inicio=None, fecha_fin=None, id_tipo_movimiento=None):
        """
        Consulta la tabla 'stock_movimientos' con filtros opcionales, agrupados por evento.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql_query = """
            SELECT
                sm.identificador_evento,
                sm.id_stock_movimiento,
                sm.cantidad,
                sm.descripcion,
                sm.fecha_movimiento AS fecha_movimiento,
                stm.descripcion AS tipo_movimiento,
                p.nombre AS nombre_producto,
                p.descripcion AS descripcion_producto, 
                producto_marca.descripcion AS marca_producto
            FROM 
                stock_movimientos sm
            LEFT JOIN 
                stock s ON s.id_stock = sm.id_stock
            LEFT JOIN 
                stock_tipo_movimiento stm ON stm.id_tipo_movimiento = sm.id_tipo_movimiento
            LEFT JOIN 
                productos p ON p.id_producto = s.id_producto 
            LEFT JOIN 
                producto_marca ON producto_marca.id_marca = p.id_marca
            WHERE 1=1
            """

            params = []

            # Filtros dinámicos
            if id_producto:
                sql_query += " AND p.id_producto = %s"
                params.append(id_producto)
            if id_usuario:
                sql_query += " AND sm.id_usuario = %s"
                params.append(id_usuario)
            if fecha_inicio:
                sql_query += " AND sm.fecha_movimiento >= %s"
                params.append(fecha_inicio)
            if fecha_fin:
                sql_query += " AND sm.fecha_movimiento <= %s"
                params.append(fecha_fin)
            if id_tipo_movimiento:
                sql_query += " AND sm.id_tipo_movimiento = %s"
                params.append(id_tipo_movimiento)

            # Ejecutar la consulta con los parámetros
            cursor.execute(sql_query, params)
            resultados = cursor.fetchall()

            if not resultados:
                raise HTTPException(status_code=404, detail="No se encontraron registros en 'stock_movimientos'.")

            # Agrupar por identificador_evento
            movimientos_por_evento = {}
            for row in resultados:
                evento_id = row["identificador_evento"]
                if evento_id not in movimientos_por_evento:
                    movimientos_por_evento[evento_id] = {
                        "identificador_evento": evento_id,
                        "movimientos": []
                    }
                movimientos_por_evento[evento_id]["movimientos"].append({
                    **dict(row),  # Devolver todas las columnas
                    "fecha_movimiento": row["fecha_movimiento"].isoformat() if isinstance(row["fecha_movimiento"], datetime) else row["fecha_movimiento"]
                })

            # Convertir el diccionario en una lista para devolver
            return list(movimientos_por_evento.values())

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