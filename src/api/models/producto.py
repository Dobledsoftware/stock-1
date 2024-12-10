#from fastapi.responses import JSONResponse
from routers import conexion
from typing import Optional
from psycopg2.extras import DictCursor
from fastapi import HTTPException



class Producto(conexion.Conexion):
    def __init__(self, id_producto=None):
        #self._id_producto = producto        
        self._estado = None  # Inicialmente no conocemos el estado
        

    @property
    def estado(self):
        return self._estado
        
################################# CARGA DATOS DEL OBJETO ############################################################
    async def cargar_estado(self):
        """Método para cargar el estado actual del proveedor desde la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "SELECT estado FROM productos WHERE id_producto = %s"
            cursor.execute(sql, (self._id_producto,))
            result = cursor.fetchone()
            print ("muestro el objeti cargado",self._id_producto)
            if result:
                self._estado = result[0]
            else:
                raise ValueError(f"Recibo con id {self._id_producto} no encontrado.")
        finally:
            conexion.close()
##################################### CAMBIA ESTADO AL OBJETO #################################################
    async def cambiar_estado(self, nuevo_estado):
        """Método para cambiar el estado del producto."""
        if nuevo_estado not in ['Activo', 'Inactivo']:
            raise ValueError("El estado debe ser 'Activo' o 'Inactivo'.")

        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            # Actualiza el estado del producto
            sql_update = """
            UPDATE productos
            SET estado = %s
            WHERE id_producto = %s
            """
            cursor.execute(sql_update, (nuevo_estado, self._id_producto))
            conexion.commit()

            # Verifica si realmente se cambió el estado
            sql_select = "SELECT estado FROM productos WHERE id_producto = %s"
            cursor.execute(sql_select, (self._id_producto,))
            result = cursor.fetchone()

            if result and result[0] == nuevo_estado:
                self._estado = nuevo_estado
                return {"status": "success", "estado": nuevo_estado, "id_producto": self._id_producto}
            else:
                # Si no coincide el nuevo estado, se devuelve un error
                return {"status": "error", "message": f"Error al actualizar el estado a {nuevo_estado}."}
        finally:
            conexion.close()

################################################################################################
    async def download(self):
        """Método para obtener la URL (ruta relativa) del archivo del producto a partir de su ID."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()

            # Verifica que el ID del producto sea correcto (tipo y contenido)
            print(f"Valor de id_producto en la consulta: {self._id_producto} (tipo: {type(self._id_producto)})")

            # Corregir la consulta SQL para que seleccione el archivo donde id_producto coincida
            sql = "SELECT archivo FROM productos WHERE id_producto= %s and estado='Activo'"
            cursor.execute(sql, (self._id_producto,))

            # Depurar el resultado de la consulta
            result = cursor.fetchone()
            if result:
                return result[0]  # Retornar la ruta relativa del archivo
            else:
                # Lanzar excepción si no se encuentra el registro
                raise ValueError(f"Recibo con id_producto='{self._id_producto}' no encontrado.")
        finally:
            conexion.close()
   

################################################################################################


    async def verTodosLosProductos(self, estado):
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
                pr.id AS proveedor_id, 
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
                p.proveedor_id = pr.id
            WHERE 
                p.estado = %s
            ORDER BY 
                p.nombre ASC;
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

#################################################################################
    
   

    async def agregar_producto(self, marca, nombre, descripcion, precio, stock_actual, stock_minimo, stock_maximo, proveedor_id, codigo_barras, forceAdd: Optional[bool] = False, accion_stock: Optional[str] = None):
        """
        Agrega un producto (variante) a la base de datos, verificando si ya existe un producto con el mismo código de barras.
        Opción A: Permite elegir incrementar o disminuir el stock de un producto repetido.
        Opción B: Si forceAdd es True, se fuerza la adición del producto y se incrementa el stock.
        """
        conexion = self.conectar()
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
            if productos_existentes and not forceAdd:
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
                if accion_stock:
                    id_producto = productos_existentes[0][0]
                    stock_actual_existente = productos_existentes[0][4]

                    # Obtener los valores de stock mínimo y máximo para la validación
                    sql_validar_stock = """
                    SELECT stock_minimo, stock_maximo FROM stock WHERE id_producto = %s;
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

                    elif accion_stock == "disminuir":
                        nuevo_stock = stock_actual_existente - stock_actual

                        # Validar que el nuevo stock no sea menor que el mínimo
                        if nuevo_stock < stock_minimo:
                            return {
                                "status": "error",
                                "message": f"No se puede disminuir el stock del producto '{nombre}' por debajo del stock mínimo ({stock_minimo}).",
                            }

                        # Validar que el nuevo stock no sea negativo
                        if nuevo_stock < 0:
                            return {
                                "status": "error",
                                "message": f"No se puede disminuir el stock del producto '{nombre}' por debajo de 0.",
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
                            "message": f"Stock del producto '{nombre}' disminuido exitosamente. Nuevo stock: {nuevo_stock}.",
                        }
                    else:
                        return {
                            "status": "error",
                            "message": "Acción de stock no válida. Debe ser 'incrementar' o 'disminuir'."
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
            elif  productos_existentes and forceAdd:
                print("entra a add")
                # Insertar nuevo producto
                sql_producto = """
                INSERT INTO productos (marca, nombre, descripcion, precio, codigo_barras, proveedor_id, estado, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING id_producto;
                """
                cursor.execute(
                    sql_producto,
                    (marca, nombre, descripcion, precio, codigo_barras, proveedor_id, estado),
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
                    "message": f"Producto '{nombre}' agregado exitosamente.",
                }

            # Si el producto no existe y no se está forzando la adición, no hacer nada
            elif not productos_existentes and not forceAdd:
                 # Insertar nuevo producto
                sql_producto = """
                INSERT INTO productos (marca, nombre, descripcion, precio, codigo_barras, proveedor_id, estado, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING id_producto;
                """
                cursor.execute(
                    sql_producto,
                    (marca, nombre, descripcion, precio, codigo_barras, proveedor_id, estado),
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
                    "message": f"Producto '{nombre}' agregado exitosamente.",
                }
        except Exception as e:
            conexion.rollback()
            raise HTTPException(status_code=500, detail=f"Error al agregar el producto: {str(e)}")

        finally:
            conexion.close()
######################################################################################################
            

    async def eliminar_producto(self, producto_id):
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
########################################################################################


    async def buscar_variantes_por_codigo(self, codigo_barras):
        """
        Busca todas las variantes asociadas a un código de barras.
        """
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            SELECT p.id_producto, p.nombre, p.descripcion, p.precio, s.stock_actual, s.stock_minimo, s.stock_maximo
            FROM productos p
            JOIN stock s ON p.id_producto = s.id_producto
            WHERE p.codigo_barras = %s;
            """
            cursor.execute(sql, (codigo_barras,))
            variantes = cursor.fetchall()

            if not variantes:
                return {"status": "error", "message": "No se encontraron productos con este código de barras."}

            return {
                "status": "success",
                "variantes": [
                    {
                        "id_producto": var[0],
                        "nombre": var[1],
                        "descripcion": var[2],
                        "precio": var[3],
                        "stock_actual": var[4],
                        "stock_minimo": var[5],
                        "stock_maximo": var[6]
                    }
                    for var in variantes
                ]
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

        finally:
            conexion.close()



########################################################################################

