from routers import conexion
from typing import Optional
from psycopg2.extras import DictCursor
from fastapi import HTTPException



class ProductoRepository(conexion.Conexion):
    def obtener_estado(self, id_producto):
        """Obtiene el estado de un producto por su ID."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "SELECT estado FROM productos WHERE id_producto = %s"
            cursor.execute(sql, (id_producto,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            conexion.close()

    def actualizar_estado(self, id_producto, nuevo_estado):
        """Actualiza el estado de un producto."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE productos
            SET estado = %s
            WHERE id_producto = %s
            """
            cursor.execute(sql, (nuevo_estado, id_producto))
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            conexion.close()

    def obtener_archivo(self, id_producto):
        """Obtiene el archivo asociado a un producto."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "SELECT archivo FROM productos WHERE id_producto = %s AND estado = 'Activo'"
            cursor.execute(sql, (id_producto,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            conexion.close()
######################################################################################################
    async def verTodosLosProductos(self, estado):
        print("pudo entrar a refrtactor")
        """Obtiene todos los productos según su estado."""
        conexion = self.conectar()
        try:
            # Usa DictCursor para resultados como diccionario
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql = """
            SELECT 
                p.id_producto AS producto_id, 
                p.marca AS producto_marca,
                p.nombre AS producto_nombre, 
                p.descripcion AS producto_descripcion, 
                p.precio AS producto_precio, 
                s.stock_actual AS stock_actual,
                s.stock_minimo AS stock_minimo,
                s.stock_maximo AS stock_maximo,
                p.fecha_creacion AS producto_fecha_creacion,
                p.fecha_ultima_modificacion AS producto_fecha_modificacion,
                p.estado AS producto_estado,
                p.codigo_barras AS producto_codigo_barras,
                pr.id_proveedor AS id_proveedor, 
                pr.nombre AS proveedor_nombre, 
                pr.direccion AS proveedor_direccion,
                pr.telefono AS proveedor_telefono,
                pr.correo_contacto AS proveedor_correo
            FROM 
                productos p
                
            LEFT JOIN
                stock s 
            ON
                s.id_producto = p.id_producto
            LEFT JOIN 
                proveedores pr 
            ON 
                p.id_proveedor = pr.id_proveedor
            WHERE 
                p.estado = %s
            ORDER BY 
                p.nombre ASC
                LIMIT 10000;
            """
            # Ejecutar la consulta
            cursor.execute(sql, (estado,))
            data = cursor.fetchall()
            # Convertir a lista de diccionarios (opcional si ya es DictCursor)
            return [dict(row) for row in data]
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return {"error": str(e)}
        finally:
            conexion.close()

######################################################################################################
    async def agregar_producto(self, marca, nombre, descripcion, precio, stock_actual, stock_minimo, stock_maximo, id_proveedor, codigo_barras, forceAdd: Optional[bool] = False, accion_stock: Optional[str] = None, id_producto: Optional[int] = None):
        """
        Agrega un producto (variante) a la base de datos, verificando si ya existe un producto con el mismo código de barras.
        Opción A: Permite elegir incrementar o disminuir el stock de un producto repetido.
        Opción B: Si forceAdd es True, se fuerza la adición del producto y se incrementa el stock.
        """
        conexion = self.conectar()
        print (str(id_producto))
        print (forceAdd)
        print ()
        try:
            cursor = conexion.cursor()
            estado = "Activo"

            # Verificar si el código de barras ya existe
            sql_verificar = """
            SELECT p.id_producto, p.marca, p.nombre, p.descripcion, s.stock_actual
            FROM productos as p
            LEFT JOIN stock as s ON s.id_producto = p.id_producto
            WHERE p.codigo_barras = %s;
            """
            cursor.execute(sql_verificar, (codigo_barras,))
            productos_existentes = cursor.fetchall()
            
            # Opción A: Si el producto existe y no se está forzando la adición, se ofrece elegir entre incrementar o disminuir el stock
            if productos_existentes and forceAdd is False:
                if isinstance(forceAdd, bool):
                    print(forceAdd)

                
                productos_repetidos = []
                for producto in productos_existentes:
                    productos_repetidos.append({
                        "id_producto": producto[0],
                        "marca": producto[1],
                        "nombre": producto[2],
                        "descripcion": producto[3],
                        "stock_actual": producto[4]
                    })
                
                # Si se recibe una acción de stock (incrementar o disminuir), se ejecuta
                if id_producto and accion_stock and forceAdd is True:
                    print ("deberia entrrear")
                    id_producto = productos_existentes[0][0]
                    stock_actual_existente = productos_existentes[0][4]

                    # Obtener los valores de stock mínimo y máximo para la validación
                    sql_validar_stock = """
                    SELECT stock_minimo, stock_maximo FROM stock WHERE id_producto = %i;
                    """
                    cursor.execute(sql_validar_stock, (id_producto,))
                    stock_limits = cursor.fetchone()
                    stock_minimo = stock_limits[0]
                    stock_maximo = stock_limits[1]

                    if accion_stock == "incrementar":
                        nuevo_stock = stock_actual_existente + stock_actual

                        # Validar que el nuevo stock no supere el máximo
                        if nuevo_stock > stock_maximo:
                            return {
                                "status": "error",
                                "message": f"No se puede incrementar el stock del producto '{nombre}' por encima del stock máximo ({stock_maximo}).",
                            }

                        sql_actualizar_stock = """
                        UPDATE stock
                        SET stock_actual = %s
                        WHERE id_producto = %s;
                        """
                        cursor.execute(sql_actualizar_stock, (nuevo_stock, id_producto))
                        conexion.commit()

                        return {
                            "status": "success",
                            "producto_id": id_producto,
                            "message": f"Stock del producto '{nombre}' incrementado exitosamente. Nuevo stock: {nuevo_stock}.",
                        }

                    # elif accion_stock == "disminuir":
                    #     nuevo_stock = stock_actual_existente - stock_actual

                    #     # Validar que el nuevo stock no sea menor que el mínimo
                    #     if nuevo_stock < stock_minimo:
                    #         return {
                    #             "status": "error",
                    #             "message": f"No se puede disminuir el stock del producto '{nombre}' por debajo del stock mínimo ({stock_minimo}).",
                    #         }

                    #     # Validar que el nuevo stock no sea negativo
                    #     if nuevo_stock < 0:
                    #         return {
                    #             "status": "error",
                    #             "message": f"No se puede disminuir el stock del producto '{nombre}' por debajo de 0.",
                    #         }

                    #     sql_actualizar_stock = """
                    #     UPDATE stock
                    #     SET stock_actual = %s
                    #     WHERE id_producto = %s;
                    #     """
                    #     cursor.execute(sql_actualizar_stock, (nuevo_stock, id_producto))
                    #     conexion.commit()

                    #     return {
                    #         "status": "success",
                    #         "producto_id": id_producto,
                    #         "message": f"Stock del producto '{nombre}' disminuido exitosamente. Nuevo stock: {nuevo_stock}.",
                    #     }
                    else:
                        return {
                            "status": "error",
                            "message": "Acción de stock no válida. Debe ser 'incrementar'."
                        }

                # Si no se recibe ninguna acción, retornamos las opciones disponibles
                return {
                    "status": "warning",
                    "message": f"¡Atención! Ya existe(n) producto(s) con el código de barras '{codigo_barras}'.",
                    "productos_repetidos": productos_repetidos,
                    "accion": "Elija una de las siguientes opciones:",
                    "opciones": ["A: Seleccionar un producto y elegir incrementar o disminuir el stock.",
                                "B: Forzar la adición de un nuevo producto.",
                                "C: No hacer nada."]
                }

            # Opción B: Si forceAdd es True, agregar el producto y aumentar el stock sin preguntar
            # elif  productos_existentes and forceAdd is True:
            #     # Insertar nuevo producto
            #     sql_producto = """
            #     INSERT INTO productos (marca, nombre, descripcion, precio, codigo_barras, id_proveedor, estado, fecha_creacion)
            #     VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            #     RETURNING id_producto;
            #     """
            #     cursor.execute(
            #         sql_producto,
            #         (marca, nombre, descripcion, precio, codigo_barras, id_proveedor, estado),
            #     )
            #     id_producto = cursor.fetchone()[0]
            #     # Insertar stock para el nuevo producto
            #     sql_stock = """
            #     INSERT INTO stock (id_producto, stock_actual, stock_minimo, stock_maximo)
            #     VALUES (%s, %s, %s, %s);
            #     """
            #     cursor.execute(sql_stock, (id_producto, stock_actual, stock_minimo, stock_maximo))
            #     conexion.commit()
            #     return {
            #         "status": "success",
            #         "producto_id": id_producto,
            #         "message": f"Producto '{nombre}' agregado exitosamente primero.",
            #     }

            # Si el producto no existe y no se está forzando la adición, no hacer nada
            elif not productos_existentes and not forceAdd and not id_producto:
                 # Insertar nuevo producto
                sql_producto = """
                INSERT INTO productos (marca, nombre, descripcion, precio, codigo_barras, id_proveedor, estado, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING id_producto;
                """
                cursor.execute(
                    sql_producto,
                    (marca, nombre, descripcion, precio, codigo_barras, id_proveedor, estado),
                )
                id_producto = cursor.fetchone()[0]
                # Insertar stock para el nuevo producto
                sql_stock = """
                INSERT INTO stock (id_producto, stock_actual, stock_minimo, stock_maximo)
                VALUES (%s, %s, %s, %s);
                """
                cursor.execute(sql_stock, (id_producto, stock_actual, stock_minimo, stock_maximo))
                conexion.commit()
                return {
                    "status": "success",
                    "producto_id": id_producto,
                    "message": f"Producto '{nombre}' agregado exitosamente ultiomo.",
                }
        except Exception as e:
            conexion.rollback()
            raise HTTPException(status_code=500, detail=f"Error al agregar el producto: {str(e)}")

        finally:
            conexion.close()


#################################eliminar_producto#####################################################################


    async def eliminarProducto(self, producto_id):
        """Método para eliminar un producto de la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM productos WHERE id_producto = %s;"
            cursor.execute(sql, (producto_id,))
            conexion.commit()

            if cursor.rowcount > 0:
                return {
                    "status": "success",
                    "message": f"Producto con ID {producto_id} eliminado exitosamente."
                }
            else:
                return {
                    "status": "error",
                    "message": f"No se encontró ningún producto con ID {producto_id}."
                }
        except Exception as e:
            print(f"Error al eliminar el producto: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()