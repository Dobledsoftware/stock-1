#from fastapi.responses import JSONResponse
from routers import conexion
from psycopg2.extras import DictCursor
from fastapi import HTTPException



class Proveedor(conexion.Conexion):
    def __init__(self, id_proveedor=None):
        self._id_proveedor = id_proveedor
        self._nombre = None
        self._direccion = None
        self._telefono = None
        self._correo_contacto = None
        self._estado = None  # Estado almacenado como booleano

    # Propiedades
    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        if isinstance(value, bool):
            self._estado = value
        else:
            raise ValueError("El estado debe ser un valor booleano (True o False).")

    @property
    def nombre(self):
        return self._nombre

    @property
    def direccion(self):
        return self._direccion

    @property
    def telefono(self):
        return self._telefono

    @property
    def correo_contacto(self):
        return self._correo_contacto

    ################################# CARGA DATOS DEL OBJETO ############################################################
    async def cargar_estado(self):
        """Método para cargar el estado actual del proveedor desde la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "SELECT estado FROM proveedores WHERE id_proveedor = %s"
            cursor.execute(sql, (self._id_proveedor,))
            result = cursor.fetchone()
            if result:
                self.estado = result[0]  # Convierte automáticamente a booleano
            else:
                raise ValueError(f"Proveedor con id {self._id_proveedor} no encontrado.")
        finally:
            conexion.close()

    ##################################### CAMBIA ESTADO AL OBJETO #################################################
    async def cambiar_estado(self, nuevo_estado):
        """Método para cambiar el estado del proveedor."""
        if not isinstance(nuevo_estado, bool):
            raise ValueError("El estado debe ser un valor booleano (True/False).")

        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            # Actualiza el estado del proveedor
            sql_update = """
            UPDATE proveedores
            SET estado = %s
            WHERE id_proveedor = %s
            """
            cursor.execute(sql_update, (nuevo_estado, self._id_proveedor))
            conexion.commit()

            # Verifica si realmente se cambió el estado
            sql_select = "SELECT estado FROM proveedores WHERE id_proveedor = %s"
            cursor.execute(sql_select, (self._id_proveedor,))
            result = cursor.fetchone()

            if result and result[0] == nuevo_estado:
                self._estado = nuevo_estado
                return {"status": "success", "estado": nuevo_estado, "id_proveedor": self._id_proveedor}
            else:
                return {"status": "error", "message": f"Error al actualizar el estado a {nuevo_estado}."}
        finally:
            conexion.close()
   
   

############################verTodosLosProveedores####################################################################


    async def verTodosLosProveedores(self, estado):##FUNCIONA OK
        """Obtiene todos los proveedors según su estado."""
        conexion = self.conectar()
        try:
            # Usa DictCursor para resultados como diccionario
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql = """
            SELECT 
                *
            FROM 
                proveedores p            
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

#############################agregarProveedor####################################################
            

    async def agregarProveedor(self, nombre, direccion, telefono,correo_contacto, estado=True):
        """Método para agregar un nuevo proveedor a la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            INSERT INTO proveedores (nombre, direccion,telefono , correo_contacto, estado)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_proveedor;
            """
            cursor.execute(sql, (nombre, direccion,  telefono, correo_contacto, estado))
            id_proveedor = cursor.fetchone()[0]
            conexion.commit()

            return {
                "status": "success",
                "id_proveedor": id_proveedor,
                "message": f"Proveedor '{nombre}' agregado exitosamente."
            }
        except Exception as e:
            print(f"Error al agregar el proveedor: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()


###############################eliminarProveedor#######################################################################
            

    async def eliminarProveedor(self, id_proveedor):
        """Método para eliminar un proveedor de la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM proveedores WHERE id_proveedor = %s;"
            cursor.execute(sql, (id_proveedor,))
            conexion.commit()

            if cursor.rowcount > 0:
                return {
                    "status": "success",
                    "message": f"Proveedor con ID {id_proveedor} eliminado exitosamente."
                }
            else:
                return {
                    "status": "error",
                    "message": f"No se encontró ningún proveedor con ID {id_proveedor}."
                }
        except Exception as e:
            print(f"Error al eliminar el proveedor: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()

##############################editarProveedor########################################################################


    async def editarProveedor(self, id_proveedor: int, nombre: str = None, direccion: str = None, telefono: str = None, correo_contacto: str = None):
        """Método para editar un proveedor en la base de datos."""
        # Buscar el proveedor por su ID
        proveedor = await self.buscarProveedorPorId(id_proveedor)
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado.")
        
        # Verificar si al menos uno de los parámetros es diferente
        cambios_realizados = False

        # Actualizar los campos solo si se proporcionan
        if nombre and nombre != proveedor.nombre:
            proveedor._nombre = nombre
            cambios_realizados = True
        if direccion and direccion != proveedor.direccion:
            proveedor._direccion = direccion
            cambios_realizados = True
        if telefono and telefono != proveedor.telefono:
            proveedor._telefono = telefono
            cambios_realizados = True
        if correo_contacto and correo_contacto != proveedor.correo_contacto:
            proveedor._correo_contacto = correo_contacto
            cambios_realizados = True
             # Si no se realizaron cambios, devolver un mensaje
        if not cambios_realizados:
            return {
                "status": "warning",
                "message": "No se realizaron cambios, ya que los valores proporcionados son los mismos."
            }

        
        # Guardar los cambios en la base de datos
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql_update = """
            UPDATE proveedores
            SET nombre = %s, direccion = %s, telefono = %s, correo_contacto = %s
            WHERE id_proveedor = %s
            """
            
            # Ejecutar la actualización
            cursor.execute(sql_update, (proveedor._nombre, proveedor._direccion, proveedor._telefono, proveedor._correo_contacto, id_proveedor))
            conexion.commit()

            # Verificar si realmente se actualizó el proveedor
            if cursor.rowcount > 0:
                return {
                    "status": "success",
                    "id_proveedor": id_proveedor,
                    "message": "Proveedor actualizado exitosamente."
                }
            else:
                return {
                    "status": "error",
                    "message": "No se pudo actualizar el proveedor. Verifique el ID."
                }
        except Exception as e:
            print(f"Error al editar el proveedor: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()


    async def buscarProveedorPorId(self, id_proveedor: int):
        """Método para buscar un proveedor por su ID en la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql = "SELECT * FROM proveedores WHERE id_proveedor = %s"
            cursor.execute(sql, (id_proveedor,))
            result = cursor.fetchone()
            if result:
                # Crear el objeto proveedor con los datos obtenidos
                proveedor = Proveedor(id_proveedor)
                proveedor._nombre = result['nombre']
                proveedor._direccion = result['direccion']
                proveedor._telefono = result['telefono']
                proveedor._correo_contacto = result['correo_contacto']
                proveedor._estado = result['estado']
                return proveedor
            else:
                return None
        except Exception as e:
            print(f"Error al buscar el proveedor: {e}")
            return None
        finally:
            conexion.close()

