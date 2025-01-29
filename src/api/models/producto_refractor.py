from routers import conexion
from typing import Optional
import json
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
        """Obtiene todos los productos según su estado (TRUE o FALSE)."""
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
                p.precio AS producto_precio, 
                p.fecha_alta AS producto_alta,
                p.fecha_ultima_modificacion AS producto_fecha_modificacion,
                p.estado AS producto_estado,
                p.codigo_barras AS producto_codigo_barras                
            FROM 
                productos p
            LEFT JOIN producto_marca as pm
                on pm.id_marca = p.id_marca                
            
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
                p.precio AS producto_precio, 
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
    async def agregar_producto(self, id_marca, nombre, descripcion, precio, codigo_barras,id_categoria, imagen_producto=None, force_add=False):
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
            INSERT INTO productos (id_marca, nombre, descripcion, precio, codigo_barras, estado, fecha_alta, imagen_producto,id_categoria)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s,%s)
            RETURNING id_producto;
            """
            cursor.execute(
                sql_producto,
                (id_marca, nombre, descripcion, precio, codigo_barras, estado, imagen_producto,id_categoria),
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

##NO tiene end pint es un metodo interno
    async def buscarProductoPorId(self, id_producto):
        """
        Busca todas las variantes asociadas a un código de barras.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT p.id_producto,p.id_marca,p.nombre,p.descripcion,p.precio,p.codigo_barras,p.id_categoria,p.imagen_producto
            FROM productos p
            WHERE p.id_producto = %s;
            """
            cursor.execute(sql, (id_producto,))
            variantes = cursor.fetchall()

            if not variantes:
                return {"status": "error", "message": "No se encontraron productos con este id_producto."}

            return {
                "status": "success",
                "variantes": [
                    {
                        "id_producto": var[0],
                        "id_marca": var[1],
                        "nombre": var[2],
                        "descripcion": var[3],
                        "precio": var[4],
                        "codigo_barras": var[5],
                        "id_categoria": var[6],
                        "imagen_producto":var[7]
                    }
                    for var in variantes
                ]
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
        precio: float = None,
        codigo_barras: str = None,
        id_categoria: int = None,
        imagen_producto: str = None,
        id_usuario: str = "admin"  # Usuario que realiza la modificación
        ):
        """Método para editar un producto en la base de datos y registrar el historial."""
        # Buscar el producto por su ID

        producto = await self.buscarProductoPorId(id_producto)

        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado.")
        
        # Verificar si al menos uno de los parámetros es diferente
        cambios_realizados = False
        datos_previos = {}
        datos_nuevos = {}
        # Comparar y registrar los cambios
        print("aver......"+str(producto))
        print("aver......"+str(id_marca))

        if not producto['variantes'] or len(producto['variantes']) == 0:
            raise HTTPException(status_code=404, detail="No se encontraron variantes para el producto.")

        variante = producto['variantes'][0]

        # Comparar y registrar los cambios
        if id_marca is not None and id_marca != variante["id_marca"]:
            datos_previos['id_marca'] = variante["id_marca"]
            datos_nuevos['id_marca'] = id_marca
            variante["id_marca"] = id_marca
            cambios_realizados = True
        if nombre and nombre != variante["nombre"]:
            datos_previos['nombre'] = variante["nombre"]
            datos_nuevos['nombre'] = nombre
            variante["nombre"] = nombre
            cambios_realizados = True
        if descripcion and descripcion != variante["descripcion"]:
            datos_previos['descripcion'] = variante["descripcion"]
            datos_nuevos['descripcion'] = descripcion
            variante["descripcion"] = descripcion
            cambios_realizados = True
        if precio is not None and precio != variante["precio"]:
            datos_previos['precio'] = variante["precio"]
            datos_nuevos['precio'] = precio
            variante["precio"] = precio
            cambios_realizados = True
        if codigo_barras and codigo_barras != variante["codigo_barras"]:
            datos_previos['codigo_barras'] = variante["codigo_barras"]
            datos_nuevos['codigo_barras'] = codigo_barras
            variante["codigo_barras"] = codigo_barras
            cambios_realizados = True
        if id_categoria is not None and id_categoria != variante["id_categoria"]:
            datos_previos['id_categoria'] = variante["id_categoria"]
            datos_nuevos['id_categoria'] = id_categoria
            variante["id_categoria"] = id_categoria
            cambios_realizados = True
        if imagen_producto and imagen_producto != variante["imagen_producto"]:
            datos_previos['imagen_producto'] = variante["imagen_producto"]
            datos_nuevos['imagen_producto'] = imagen_producto
            variante["imagen_producto"] = imagen_producto
            cambios_realizados = True
        # Si no se realizaron cambios, devolver un mensaje
        if not cambios_realizados:
            return {
                "status": "warning",
                "message": "No se realizaron cambios, ya que los valores proporcionados son los mismos."
            }

        # Guardar los cambios en la base de datos y registrar el historial
        conexion = self.conectar()
        print("no entra")
        try:
            print("entra a updatear")
            cursor = conexion.cursor()
            sql_update = """
            UPDATE productos
            SET id_marca = %s, nombre = %s, descripcion = %s, precio = %s, 
                codigo_barras = %s, id_categoria = %s, imagen_producto = %s, fecha_ultima_modifica = CURRENT_TIMESTAMP
            WHERE id_producto = %s
            """
            
            # Ejecutar la actualización
            cursor.execute(sql_update, (
                producto["id_marca"],
                producto["nombre"],
                producto["descripcion"],
                producto["precio"],
                producto["codigo_barras"],
                producto["id_categoria"],
                producto["imagen_producto"],
                id_producto
            ))

            # Insertar en producto_history
            sql_insert_history = """
            INSERT INTO productos_historisl (
                id_producto, fecha_modificacion, id_usuario, accion, datos_previos, datos_nuevos
            ) VALUES (
                %s, CURRENT_TIMESTAMP, %s, %s, %s::jsonb, %s::jsonb
            )
            """
            cursor.execute(sql_insert_history, (
                id_producto,
                id_usuario,
                "UPDATE",
                json.dumps(datos_previos),  # Convertir datos_previos a JSON
                json.dumps(datos_nuevos)   # Convertir datos_nuevos a JSON
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
                SELECT id_history, id_producto, fecha_modificacion, id_usuario, accion, datos_previos, datos_nuevos
                FROM producto_history
                WHERE id_producto = %s
                ORDER BY fecha_modificacion DESC
                """
                cursor.execute(sql_query, (id_producto,))
            else:
                sql_query = """
                SELECT id_history, id_producto, fecha_modificacion, id_usuario, accion, datos_previos, datos_nuevos
                FROM producto_history
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
