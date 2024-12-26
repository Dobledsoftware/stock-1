#from fastapi.responses import JSONResponse
from routers import conexion
from psycopg2.extras import DictCursor
from fastapi import HTTPException



class Estante(conexion.Conexion):
    def __init__(self, id_estante=None):
        self._id_estante = id_estante
        self._descripcion = None
        self._estado = None  # Estado estanteado como booleano

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
        """Método para cargar el estado actual del estante desde la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "SELECT estado from almacen_estante WHERE id_estante = %s"
            cursor.execute(sql, (self._id_estante,))
            result = cursor.fetchone()
            if result:
                self.estado = result[0]  # Convierte automáticamente a booleano
            else:
                raise ValueError(f"Estante con id {self._id_estante} no encontrado.")
        finally:
            conexion.close()

    ##################################### CAMBIA ESTADO AL OBJETO #################################################
    async def cambiar_estado(self, nuevo_estado):
        """Método para cambiar el estado del estante."""
        if not isinstance(nuevo_estado, bool):
            raise ValueError("El estado debe ser un valor booleano (True/False).")
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            # Actualiza el estado del estante
            sql_update = """
            UPDATE almacen_estante
            SET estado = %s
            WHERE id_estante = %s
            """
            cursor.execute(sql_update, (nuevo_estado, self._id_estante))
            conexion.commit()

            # Verifica si realmente se cambió el estado
            sql_select = "SELECT estado from almacen_estante WHERE id_estante = %s"
            cursor.execute(sql_select, (self._id_estante,))
            result = cursor.fetchone()

            if result and result[0] == nuevo_estado:
                self._estado = nuevo_estado
                return {"status": "success", "estado": nuevo_estado, "id_estante": self._id_estante}
            else:
                return {"status": "error", "message": f"Error al actualizar el estado a {nuevo_estado}."}
        finally:
            conexion.close()
   
   

############################verTodosLosestantees####################################################################


    async def verTodosLosestantes(self,id_almacen, estado):##FUNCIONA OK
        """Obtiene todos los estantes según su estado."""
        conexion = self.conectar()

        try:
            # Usa DictCursor para resultados como diccionario
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql = """
            SELECT 
                *
            FROM 
                almacen_estante a           
            WHERE 
                a.estado = %s
                and
                a.id_almacen = %s
            ORDER BY 
                a.descripcion ASC;
            """
            # Ejecutar la consulta
            cursor.execute(sql, (estado,id_almacen,))
            data = cursor.fetchall()

            # Convertir a lista de diccionarios (opcional si ya es DictCursor)
            return [dict(row) for row in data]
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return {"error": str(e)}
        finally:
            conexion.close()

#############################agregarestante####################################################
            

    async def agregarEstante(self,id_almacen, descripcion, estado=True):
        """Método para agregar un nuevo estante a la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = """
            INSERT INTO almacen_estante (id_almacen,descripcion, estado)
            VALUES (%s, %s, %s)
            RETURNING id_estante;
            """
            cursor.execute(sql, (id_almacen, descripcion,  estado))
            id_estante = cursor.fetchone()[0]
            conexion.commit()

            return {
                "status": "success",
                "id_estante": id_estante,
                "message": f"estante '{descripcion}' agregado exitosamente."
            }
        except Exception as e:
            print(f"Error al agregar el estante: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()


###############################eliminarestante#######################################################################
            

    async def eliminarestante(self, id_estante):
        """Método para eliminar un estante de la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "DELETE from almacen_estante WHERE id_estante = %s;"
            cursor.execute(sql, (id_estante,))
            conexion.commit()

            if cursor.rowcount > 0:
                return {
                    "status": "success",
                    "message": f"estante con ID {id_estante} eliminado exitosamente."
                }
            else:
                return {
                    "status": "error",
                    "message": f"No se encontró ningún estante con ID {id_estante}."
                }
        except Exception as e:
            print(f"Error al eliminar el estante: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()

##############################editarestante########################################################################


    async def editarestante(self, id_estante: int, descripcion: str = None):
        """Método para editar un estante en la base de datos."""
        # Buscar el estante por su ID
        estante = await self.buscarestantePorId(id_estante)
        if not estante:
            raise HTTPException(status_code=404, detail="estante no encontrado.")
        
        # Verificar si al menos uno de los parámetros es diferente
        cambios_realizados = False

        # Actualizar los campos solo si se proporcionan
        if descripcion and descripcion != estante.descripcion:
            estante._descripcion = descripcion
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
            UPDATE almacen_estante
            SET descripcion = %s
            WHERE id_estante = %s
            """
            
            # Ejecutar la actualización
            cursor.execute(sql_update, estante._descripcion,id_estante)
            conexion.commit()

            # Verificar si realmente se actualizó el estante
            if cursor.rowcount > 0:
                return {
                    "status": "success",
                    "id_estante": id_estante,
                    "message": "estante actualizado exitosamente."
                }
            else:
                return {
                    "status": "error",
                    "message": "No se pudo actualizar el estante. Verifique el ID."
                }
        except Exception as e:
            print(f"Error al editar el estante: {e}")
            conexion.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conexion.close()


    async def buscarestantePorId(self, id_estante: int):
        """Método para buscar un estante por su ID en la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor(cursor_factory=DictCursor)
            sql = "SELECT * from almacen_estante WHERE id_estante = %s"
            cursor.execute(sql, (id_estante,))
            result = cursor.fetchone()
            if result:
                # Crear el objeto estante con los datos obtenidos
                estante = estante(id_estante)
                estante._descripcion = result['descripcion']
                estante._estado = result['estado']
                return estante
            else:
                return None
        except Exception as e:
            print(f"Error al buscar el estante: {e}")
            return None
        finally:
            conexion.close()

