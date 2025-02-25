#from fastapi.responses import JSONResponse
from routers import conexion
from psycopg2.extras import DictCursor
from fastapi import HTTPException



class Almacen(conexion.Conexion):
    def __init__(self, id_almacen=None):
        self._id_almacen = id_almacen
        self._descripcion = None
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
    def descripcion(self):
        return self._descripcion
    ################################# CARGA DATOS DEL OBJETO ############################################################
    async def cargar_estado(self):
        """Método para cargar el estado actual del almacen desde la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "SELECT estado FROM almacen WHERE id_almacen = %s"
            cursor.execute(sql, (self._id_almacen,))
            result = cursor.fetchone()
            if result:
                self.estado = result[0]  # Convierte automáticamente a booleano
            else:
                raise ValueError(f"Almacen con id {self._id_almacen} no encontrado.")
        finally:
            conexion.close()

    ##################################### CAMBIA ESTADO AL OBJETO #################################################
    async def cambiar_estado(self, nuevo_estado):
        """Método para cambiar el estado del almacen."""
        if not isinstance(nuevo_estado, bool):
            raise ValueError("El estado debe ser un valor booleano (True/False).")

        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            # Actualiza el estado del almacen
            sql_update = """
            UPDATE almacen
            SET estado = %s
            WHERE id_almacen = %s
            """
            cursor.execute(sql_update, (nuevo_estado, self._id_almacen))
            conexion.commit()

            # Verifica si realmente se cambió el estado
            sql_select = "SELECT estado FROM almacen WHERE id_almacen = %s"
            cursor.execute(sql_select, (self._id_almacen,))
            result = cursor.fetchone()

            if result and result[0] == nuevo_estado:
                self._estado = nuevo_estado
                return {"status": "success", "estado": nuevo_estado, "id_almacen": self._id_almacen}
            else:
                return {"status": "error", "message": f"Error al actualizar el estado a {nuevo_estado}."}
        finally:
            conexion.close()
   
   

############################verTodosLosalmacenes####################################################################


    async def verTodosLosAlmacenes(self, estado):##FUNCIONA OK
        """Obtiene todos los almacens según su estado."""
        conexion = self.conectar()

        try:
            # Usa DictCursor para resultados como diccionario
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql = f"SELECT * FROM almacen WHERE estado = {str(estado).upper()} ORDER BY id_almacen ASC;"

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

#############################agregaralmacen####################################################
            

    async def agregarAlmacen(self, descripcion, estado=True):
        """Método para agregar un nuevo almacen a la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            INSERT INTO almacen (descripcion, estado)
            VALUES ( %s, %s)
            RETURNING id_almacen;
            """
            cursor.execute(sql, (descripcion,  estado))
            id_almacen = cursor.fetchone()[0]
            conexion.commit()

            return {
                "status": "success",
                "id_almacen": id_almacen,
                "message": f"almacen '{descripcion}' agregado exitosamente."
            }
        except Exception as e:
            print(f"Error al agregar el almacen: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()


###############################eliminaralmacen#######################################################################
            

    async def eliminarAlmacen(self, id_almacen):
        """Método para eliminar un almacen de la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM almacen WHERE id_almacen = %s;"
            cursor.execute(sql, (id_almacen,))
            conexion.commit()

            if cursor.rowcount > 0:
                return {
                    "status": "success",
                    "message": f"almacen con ID {id_almacen} eliminado exitosamente."
                }
            else:
                return {
                    "status": "error",
                    "message": f"No se encontró ningún almacen con ID {id_almacen}."
                }
        except Exception as e:
            print(f"Error al eliminar el almacen: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()

##############################editaralmacen########################################################################

    async def editaralmacen(self, id_almacen, descripcion):
        """Método para editar un almacen en la base de datos."""
        # Buscar el almacen por su ID
        almacen = await self.buscaralmacenPorId(id_almacen)
        if not almacen:
            raise HTTPException(status_code=404, detail="almacen no encontrado.")
        
        # Verificar si al menos uno de los parámetros es diferente
        cambios_realizados = False

        # Actualizar los campos solo si se proporcionan
        if descripcion and descripcion != almacen.descripcion:
            almacen._descripcion = descripcion
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
            UPDATE almacen
            SET descripcion = %s
            WHERE id_almacen = %s
            """
            
            # Ejecutar la actualización
            cursor.execute(sql_update, (almacen._descripcion, id_almacen))
            conexion.commit()

            # Verificar si realmente se actualizó el almacen
            if cursor.rowcount > 0:
                return {
                    "status": "success",
                    "id_almacen": id_almacen,
                    "message": "almacen actualizado exitosamente."
                }
            else:
                return {
                    "status": "error",
                    "message": "No se pudo actualizar el almacen. Verifique el ID."
                }
        except Exception as e:
            print(f"Error al editar el almacen: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()

##############################buscaralmacenPorId########################################################################


    async def buscaralmacenPorId(self, id_almacen):
        """Método para buscar un almacen por su ID en la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql = "SELECT * FROM almacen WHERE id_almacen = %s"
            cursor.execute(sql, (id_almacen,))
            result = cursor.fetchone()
            if result:
                # Crear el objeto almacen con los datos obtenidos
                almacen = Almacen(id_almacen)
                almacen._descripcion = result['descripcion']
                almacen._estado = result['estado']
                return almacen
            else:
                return None
        except Exception as e:
            print(f"Error al buscar el almacen: {e}")
            return None
        finally:
            conexion.close()

