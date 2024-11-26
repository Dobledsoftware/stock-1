from fastapi.responses import JSONResponse
from routers import conexion

class Recibo(conexion.Conexion):
    def __init__(self, id_recibo=None):
        self._id_recibo = id_recibo
        self._estado = None  # Inicialmente no conocemos el estado

    @property
    def estado(self):
        return self._estado
################################# CARGA DATOS DEL OBJETO ############################################################
    async def cargar_estado(self):
        """Método para cargar el estado actual del recibo desde la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "SELECT estado FROM recibos WHERE id_recibo = %s"
            cursor.execute(sql, (self._id_recibo,))
            result = cursor.fetchone()
            print ("muestro el objeti cargado",self._id_recibo)
            if result:
                self._estado = result[0]
            else:
                raise ValueError(f"Recibo con id {self._id_recibo} no encontrado.")
        finally:
            conexion.close()
##################################### CAMBIA ESTADO AL OBJETO #################################################
    async def cambiar_estado(self, nuevo_estado):
        """Método para cambiar el estado del recibo."""
        if nuevo_estado not in ['Activado', 'Desactivado']:
            raise ValueError("El estado debe ser 'Activado' o 'Desactivado'.")

        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            # Actualiza el estado del recibo
            sql_update = """
            UPDATE recibos
            SET estado = %s
            WHERE id_recibo = %s
            """
            cursor.execute(sql_update, (nuevo_estado, self._id_recibo))
            conexion.commit()

            # Verifica si realmente se cambió el estado
            sql_select = "SELECT estado FROM recibos WHERE id_recibo = %s"
            cursor.execute(sql_select, (self._id_recibo,))
            result = cursor.fetchone()

            if result and result[0] == nuevo_estado:
                self._estado = nuevo_estado
                return {"status": "success", "estado": nuevo_estado, "id_recibo": self._id_recibo}
            else:
                # Si no coincide el nuevo estado, se devuelve un error
                return {"status": "error", "message": f"Error al actualizar el estado a {nuevo_estado}."}
        finally:
            conexion.close()

################################################################################################
    async def download(self):
        """Método para obtener la URL (ruta relativa) del archivo del recibo a partir de su ID."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()

            # Verifica que el ID del recibo sea correcto (tipo y contenido)
            print(f"Valor de id_recibo en la consulta: {self._id_recibo} (tipo: {type(self._id_recibo)})")

            # Corregir la consulta SQL para que seleccione el archivo donde id_recibo coincida
            sql = "SELECT archivo FROM recibos WHERE id_recibo = %s and estado='Activado'"
            cursor.execute(sql, (self._id_recibo,))

            # Depurar el resultado de la consulta
            result = cursor.fetchone()
            if result:
                return result[0]  # Retornar la ruta relativa del archivo
            else:
                # Lanzar excepción si no se encuentra el registro
                raise ValueError(f"Recibo con id_reciboxxxxx='{self._id_recibo}' no encontrado.")
        finally:
            conexion.close()
   

################################################################################################


    async def todosLosRecibos(self, cuil):
        conexion = self.conectar()
        print("ENTRO A TODOS LOS RECIBOS")
        try:
            if conexion is None:
                print("Error: No se pudo establecer la conexión a la base de datos.")
                return {"error": "No se pudo establecer la conexión a la base de datos."}
            
            cursor = conexion.cursor(dictionary=True)
            sql = """
            SELECT
                r.id_recibo,
                rp.periodo,
                r.fecha_subida,
                r.descripcion_archivo,
                r.estado
            FROM
                recibos r
                 LEFT JOIN recibos_periodos rp ON rp.id_periodo = r.id_periodo
            WHERE
             r.cuil = %s
            ORDER BY
                r.fecha_subida ASC
            """
            #print(sql)  # Imprimir la consulta para depuración
            cursor.execute(sql, (cuil,))  
            data = cursor.fetchall()            
            return data
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            import traceback
            traceback.print_exc()  # Imprimir la traza del error
            return {"error": str(e)}
        finally:
            if conexion:
                conexion.close()
