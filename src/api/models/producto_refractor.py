from routers import conexion
from typing import Optional
import json
import decimal

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
        """Obtiene todos los productos con su último precio de costo desde stock."""
        conexion = self.conectar()
        try:
            # Usa DictCursor para resultados como diccionario
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql = """
            SELECT 
                p.id_producto AS producto_id, 
                pm.descripcion AS producto_marca,
                p.nombre AS producto_nombre, 
                p.descripcion AS producto_descripcion, 
                COALESCE(
                    (SELECT s.precio_costo_ars 
                    FROM stock s 
                    WHERE s.id_producto = p.id_producto 
                    ORDER BY s.fecha_ingreso DESC 
                    LIMIT 1), 
                    0
                ) AS precio_costo_ars,  -- Último precio de costo desde stock
                p.precio_venta_ars,
                COALESCE(
                    (SELECT s.precio_costo_usd
                    FROM stock s 
                    WHERE s.id_producto = p.id_producto 
                    ORDER BY s.fecha_ingreso DESC 
                    LIMIT 1), 
                    0
                ) AS precio_costo_usd,  -- Último precio de costo en usd desde stock
                p.precio_venta_usd,
                p.fecha_alta AS producto_alta,
                p.fecha_ultima_modificacion AS producto_fecha_modificacion,
                p.estado AS producto_estado,
                p.codigo_barras AS producto_codigo_barras                
            FROM 
                productos p
            LEFT JOIN producto_marca as pm ON pm.id_marca = p.id_marca                
            WHERE 
                p.estado = %s
            ORDER BY 
                p.nombre ASC
            LIMIT 10000;
            """
            # Ejecutar la consulta
            cursor.execute(sql, (estado,))  # estado puede ser True o False
            data = cursor.fetchall()
            # Convertir a lista de diccionarios (opcional si ya es DictCursor)
            return [dict(row) for row in data]
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return {"error": str(e)}
        finally:
            conexion.close()
########################buscarPorCodigoDeBarras###################################################

    async def buscarPorCodigoDeBarras(self, codigo_barras,estado):
        """
        Busca un producto por su código de barras y devuelve toda la información disponible, 
        incluyendo los mismos datos que la búsqueda normal.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)  # Usar DictCursor para obtener resultados como diccionarios
            sql = """
            SELECT 
                p.id_producto AS producto_id, 
                pm.descripcion AS producto_marca,
                p.nombre AS producto_nombre, 
                p.descripcion AS producto_descripcion, 
                p.precio_venta_ars AS precio_venta_ars, 
                p.precio_venta_usd AS precio_venta_usd, 
                p.fecha_alta AS producto_alta,
                p.fecha_ultima_modificacion AS producto_fecha_modificacion,
                p.estado AS producto_estado,
                p.codigo_barras AS producto_codigo_barras
            FROM 
                productos p
            LEFT JOIN producto_marca pm
                ON pm.id_marca = p.id_marca
            WHERE 
                p.codigo_barras = %s
                AND p.estado = %s
                
            ORDER BY 
                p.nombre ASC;
            """
            # Ejecutar la consulta
            cursor.execute(sql, (codigo_barras,estado))
            productos = cursor.fetchall()

            if not productos:
                return {
                    "status": "error",
                    "message": "No se encontraron productos con este código de barras."
                }

            # Convertir los resultados a una lista de diccionarios
            return {
                "status": "success",
                "productos": [dict(producto) for producto in productos]
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

        finally:
            conexion.close()


######################################################################################################
    async def agregar_producto(self, id_marca, nombre, descripcion, precio_venta_ars,precio_venta_usd, codigo_barras,id_categoria, imagen_producto=None, force_add=False):
        """
        Agrega un producto (variante) a la base de datos, verificando si ya existe un producto con el mismo código de barras.
        Si force_add es True, permite duplicar el producto aunque tenga el mismo código de barras.
        """
        conexion = self.conectar()

        try:
            cursor = conexion.cursor()
            estado = "Activo"

            # Verificar si el código de barras ya existe
            sql_verificar = """
            SELECT p.id_producto, p.id_marca as marca, p.nombre, p.descripcion,p.codigo_barras
            FROM productos p
            left join producto_marca pm 
            on pm.id_marca = p.id_marca
            WHERE codigo_barras = %s;
            """
            cursor.execute(sql_verificar, (codigo_barras,))
            productos_existentes = cursor.fetchall()

            # Si el producto ya existe y no se forza la adición, retornar advertencia
            if productos_existentes and not force_add:
                productos_repetidos = [
                    {
                        "id_producto": producto[0],
                        "id_marca": producto[1],
                        "nombre": producto[2],
                        "descripcion": producto[3],
                        "codigo_barras": producto[4],
                    }
                    for producto in productos_existentes
                ]
                return {
                    "status": "warning",
                    "message": f"Ya existe(n) producto(s) con el código de barras '{codigo_barras}'.",
                    "productos_repetidos": productos_repetidos,
                }
            
            # Insertar el nuevo producto (aunque ya exista uno con el mismo código de barras, si force_add es True)
            sql_producto = """
            INSERT INTO productos (id_marca, nombre, descripcion, precio_venta_ars,precio_venta_usd, codigo_barras, estado, fecha_alta, imagen_producto,id_categoria)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s,%s)
            RETURNING id_producto;
            """
            cursor.execute(
                sql_producto,
                (id_marca, nombre, descripcion, precio_venta_ars,precio_venta_usd, codigo_barras, estado, imagen_producto,id_categoria),
            )
            id_producto = cursor.fetchone()[0]
            conexion.commit()

            return {
                "status": "success",
                "id_producto": id_producto,
                "message": f"Producto '{nombre}' agregado exitosamente.",
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





################################buscarProductoPorId#######################################################

##NO tiene endpont es un metodo interno
    async def buscarProductoPorID(self, id_producto):        
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT p.id_producto, p.id_marca, p.nombre, p.descripcion, p.precio_venta_ars,p.precio_venta_usd, 
                p.codigo_barras, p.id_categoria, p.imagen_producto
            FROM productos p
            WHERE p.id_producto = %s;
            """
            cursor.execute(sql, (id_producto,))
            producto = cursor.fetchone()

            if not producto:
                return {"status": "error", "message": "No se encontró un producto con este ID."}

            return {
                "status": "success",
                "producto": {
                    "id_producto": producto[0],
                    "id_marca": producto[1],
                    "nombre": producto[2],
                    "descripcion": producto[3],
                    "precio_venta_ars": producto[4],
                    "precio_venta_usd": producto[5],
                    "codigo_barras": producto[6],
                    "id_categoria": producto[7],
                    "imagen_producto": producto[8]
                }
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

        finally:
            conexion.close()


########################editarProveedor###################################################


    async def editarProducto(
        self,
        id_producto: int,
        id_marca: int = None,
        nombre: str = None,
        descripcion: str = None,
        precio_venta_ars: float = None,
        precio_venta_usd: float = None,
        codigo_barras: str = None,
        id_categoria: int = None,        
        id_usuario: str = None,  # Usuario que realiza la modificación
        imagen_producto: str = None,
    ):
        """Método para editar un producto en la base de datos y registrar el historial."""
        # Buscar el producto por su ID
        resultado = await self.buscarProductoPorID(id_producto)
        if resultado["status"] != "success":
            print("Producto no encontrado.")
            return HTTPException(status_code=404, detail="Producto no encontrado.")
        
        # Obtener datos actuales del producto
        bd_producto = resultado["producto"]
        # Inicializar cambios
        cambios_realizados = False
        datos_previos = {}
        datos_nuevos = {}
        # Comparar y registrar los cambios
        if id_marca is not None and id_marca != bd_producto["id_marca"]:
            datos_previos["id_marca"] = bd_producto["id_marca"]
            datos_nuevos["id_marca"] = id_marca
            bd_producto["id_marca"] = id_marca
            cambios_realizados = True

        if nombre and nombre != bd_producto["nombre"]:
            datos_previos["nombre"] = bd_producto["nombre"]
            datos_nuevos["nombre"] = nombre
            bd_producto["nombre"] = nombre
            cambios_realizados = True    

        if descripcion and descripcion != bd_producto["descripcion"]:
            datos_previos["descripcion"] = bd_producto["descripcion"]
            datos_nuevos["descripcion"] = descripcion
            bd_producto["descripcion"] = descripcion
            cambios_realizados = True

        if precio_venta_ars is not None:
            precio_actual_ars = float(bd_producto["precio_venta_ars"]) if isinstance(bd_producto["precio_venta_ars"], decimal.Decimal) else bd_producto["precio_venta_ars"]
            precio_nuevo_ars = float(precio_venta_ars) if isinstance(precio_venta_ars, decimal.Decimal) else precio_venta_ars

            if precio_nuevo_ars != precio_actual_ars:
                datos_previos["precio_venta_ars"] = precio_actual_ars
                datos_nuevos["precio_venta_ars"] = precio_nuevo_ars
                bd_producto["precio_venta_ars"] = precio_nuevo_ars
                cambios_realizados = True

        if precio_venta_usd is not None:
            precio_actual_usd = float(bd_producto["precio_venta_usd"]) if isinstance(bd_producto["precio_venta_usd"], decimal.Decimal) else bd_producto["precio_venta_usd"]
            precio_nuevo_usd = float(precio_venta_usd) if isinstance(precio_venta_usd, decimal.Decimal) else precio_venta_usd

            if precio_nuevo_usd != precio_actual_usd:
                datos_previos["precio_venta_usd"] = precio_actual_usd
                datos_nuevos["precio_venta_usd"] = precio_nuevo_usd
                bd_producto["precio_venta_usd"] = precio_nuevo_usd
                cambios_realizados = True

        if codigo_barras and codigo_barras != bd_producto["codigo_barras"]:
            datos_previos["codigo_barras"] = bd_producto["codigo_barras"]
            datos_nuevos["codigo_barras"] = codigo_barras
            bd_producto["codigo_barras"] = codigo_barras
            cambios_realizados = True

        if id_categoria is not None and id_categoria != bd_producto["id_categoria"]:
            datos_previos["id_categoria"] = bd_producto["id_categoria"]
            datos_nuevos["id_categoria"] = id_categoria
            bd_producto["id_categoria"] = id_categoria
            cambios_realizados = True

        if imagen_producto and imagen_producto != bd_producto["imagen_producto"]:
            datos_previos["imagen_producto"] = bd_producto["imagen_producto"]
            datos_nuevos["imagen_producto"] = imagen_producto
            bd_producto["imagen_producto"] = imagen_producto
            cambios_realizados = True
        # Si no hay cambios, no actualizar
        if not cambios_realizados:

            return {
                "status": "warning",
                "message": "No se realizaron cambios, ya que los valores proporcionados son los mismos."
            }

        # Guardar cambios en la base de datos
        conexion = self.conectar()
        try:
            print(bd_producto["precio_venta_usd"])

            cursor = conexion.cursor()
            sql_update = """
            UPDATE productos
            SET id_marca = %s, nombre = %s, descripcion = %s, precio_venta_ars = %s,  precio_venta_usd = %s, 
                codigo_barras = %s, id_categoria = %s, imagen_producto = %s, 
                fecha_ultima_modificacion = CURRENT_TIMESTAMP
            WHERE id_producto = %s
            """

            # Ejecutar la actualización
            cursor.execute(sql_update, (
                bd_producto["id_marca"],
                bd_producto["nombre"],
                bd_producto["descripcion"],
                bd_producto["precio_venta_ars"],
                bd_producto["precio_venta_usd"],
                bd_producto["codigo_barras"],
                bd_producto["id_categoria"],
                bd_producto["imagen_producto"],
                id_producto
            ))
            
            # Insertar en el historial de cambios
            sql_insert_history = """
            INSERT INTO productos_historial (
                id_producto, id_usuario, accion, datos_previos, datos_nuevos
            ) VALUES (
                %s, %s, %s, %s::jsonb, %s::jsonb
            )
            """
            cursor.execute(sql_insert_history, (
                id_producto,
                id_usuario,
                "UPDATE",
                json.dumps(datos_previos, default=str),  # Convertir datos_previos a JSON
                json.dumps(datos_nuevos, default=str)   # Convertir datos_nuevos a JSON
            ))

            conexion.commit()

            # Verificar si realmente se actualizó el producto
            if cursor.rowcount > 0:
                return {
                    "status": "success",
                    "id_producto": id_producto,
                    "message": "Producto actualizado exitosamente."
                }
            else:
                return {
                    "status": "error",
                    "message": "No se pudo actualizar el producto. Verifique el ID."
                }
        except Exception as e:
            print(f"Error al editar el producto: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()



############################consultarHistorialProducto#####################################################


    async def consultarHistorialProducto(self, id_producto: int = None):
        """
        Consulta el historial de modificaciones de productos.
        Si se proporciona un id_producto, filtra el historial por ese producto.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()

            # Construir la consulta SQL
            if id_producto:
                sql_query = """
                SELECT *
                FROM productos_historial
                WHERE id_producto = %s
                ORDER BY fecha_modificacion DESC
                """
                # Ejecutar la consulta pasando el parámetro correctamente
                cursor.execute(sql_query, (id_producto,))

            else:
                # Si no se pasa un id_producto, se obtiene todo el historial
                sql_query = """
                SELECT *
                FROM productos_historial
                ORDER BY fecha_modificacion DESC
                """
                cursor.execute(sql_query)

            # Obtener los resultados
            resultados = cursor.fetchall()

            # Retornar el historial en formato JSON (diccionario)
            return {
                "status": "success",
                "data": resultados,
                "message": "Historial obtenido exitosamente." if resultados else "No se encontraron registros."
            }

        except Exception as e:
            print(f"Error al consultar el historial: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
        finally:
            conexion.close()




############################obtener_configuracion#####################################################

    async def obtener_configuracion(self):
        """Obtiene la configuración de precios actual."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM configuracion_precios WHERE id_configuracion_precios = 1;")
            config = cursor.fetchone()
            return {
                "permitir_precio_menor_costo_ars": config[1],
                "permitir_precio_menor_costo_usd": config[2],
                "ajuste_precio_porcentaje_ars": config[3],
                "ajuste_precio_porcentaje_usd": config[4],
                "valor_dolar": config[5]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()


############################actualizar_configuracion#####################################################

    async def actualizar_configuracion(self, permitir_precio_menor_costo_ars: bool, permitir_precio_menor_costo_usd: bool,
                                   ajuste_precio_porcentaje_ars: float, ajuste_precio_porcentaje_usd: float, valor_dolar: float):
        """Actualiza la configuración de precios en la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE configuracion_precios
            SET permitir_precio_menor_costo_ars = %s,
                permitir_precio_menor_costo_usd = %s,
                ajuste_precio_porcentaje_ars = %s,
                ajuste_precio_porcentaje_usd = %s,
                valor_dolar = %s
            WHERE id_configuracion_precios = 1;
            """
            cursor.execute(sql, (permitir_precio_menor_costo_ars, permitir_precio_menor_costo_usd,
                                ajuste_precio_porcentaje_ars, ajuste_precio_porcentaje_usd, valor_dolar))
            conexion.commit()
            return {"status": "success", "message": "Configuración actualizada correctamente."}
        except Exception as e:
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()

############################convertir_precios_dolares#####################################################

    async def convertir_precios_dolares(self):
        """Convierte los productos en dólares a pesos según el tipo de cambio configurado."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            # Obtener el valor del dólar desde la configuración
            cursor.execute("SELECT valor_dolar FROM configuracion_precios WHERE id_configuracion_precios = 1;")
            valor_dolar = cursor.fetchone()[0]
            sql = """
            UPDATE productos
            SET precio_venta_ars = precio_venta_ars * %s
            WHERE es_dolar = TRUE;
            """
            cursor.execute(sql, (valor_dolar,))
            conexion.commit()
            return {"status": "success", "message": "Precios con costos en dólares convertidos a pesos."}
        except Exception as e:
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()
