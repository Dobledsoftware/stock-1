from routers import conexion
from fastapi.responses import JSONResponse

class DesactivaRecibos(conexion.Conexion):  
    async def desactivar_recibos(self, id_recibo):
        conexion = self.conectar() 
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE recibos
            SET estado = 'Desactivado'
            WHERE id_recibo = %s
            """            
            # Imprimir consulta y parámetros            
            # Ejecuta la consulta con el parámetro correspondiente
            cursor.execute(sql, (id_recibo,))
            conexion.commit()  # Asegura que los cambios se confirmen en la base de datos                        
            if cursor.rowcount == 1:
                # Retornar un JSON con el estado de éxito y el ID desactivado
                return JSONResponse(content={
                    "status": "success",
                    "message": "Recibo desactivado correctamente",
                    "data": {
                        "id_recibo": id_recibo
                    }
                })
            else:
                # Manejo en caso de que no se desactive ningún recibo
                return JSONResponse(content={
                    "status": "error",
                    "message": "No se pudo desactivar el recibo. Puede que ya esté desactivado o no exista.",
                    "data": {
                        "id_recibo": id_recibo
                    }
                }, status_code=400)
            
        finally:
            conexion.close()
