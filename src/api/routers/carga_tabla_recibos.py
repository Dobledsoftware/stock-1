from routers import conexion

class CargaTablaRecibos(conexion.Conexion):  
    async def carga_tabla_recibos(self, cuil, periodo):
        conexion = self.conectar()
        

        try:
            cursor = conexion.cursor(dictionary=True)
            sql = """
            SELECT recibos.descripcion_archivo, recibos_periodos.periodo, recibos.id_recibo 
            FROM recibos_periodos
            JOIN recibos ON recibos.id_periodo = recibos_periodos.id_periodo 
            WHERE recibos_periodos.estado = 'Activado'
            AND recibos_periodos.periodo = %s 
            AND recibos.cuil = %s 
            ORDER BY recibos.fecha_correspondencia ASC
            """
            cursor.execute(sql, (periodo, cuil))
            data = cursor.fetchall()            
            # Devolver los datos tal cual para que FastAPI los convierta a JSON automáticamente            
            return data
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return {"error": str(e)}

        finally:
            conexion.close()
