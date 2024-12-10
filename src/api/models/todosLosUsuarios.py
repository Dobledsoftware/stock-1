from routers import conexion
class TodosLosUsuarios(conexion.Conexion):  
    async def todosLosUsuarios(self, cuil):
        conexion = self.conectar()

        try:
            if conexion is None:
                print("Error: No se pudo establecer la conexión a la base de datos.")
                return {"error": "No se pudo establecer la conexión a la base de datos."}
            
            
            cursor = conexion.cursor(dictionary=True)
            sql1 = """
            SELECT
            rol
            FROM
            usuarios 
            where cuil =%s
            """
            #print(sql)  # Imprimir la consulta para depuración
            cursor.execute(sql1, (cuil,))             
            data = cursor.fetchall() 
            if data[0]["rol"] =='2':
                 cursor = conexion.cursor(dictionary=True)
                 sql = """
                 SELECT
                   *
                 FROM
                 usuarios 
                 """
                 #print(sql)  # Imprimir la consulta para depuración
                 cursor.execute(sql, (cuil,))  
                 data = cursor.fetchall()   
                 return data
            else:
                return "No tiene permisos"
                #return data
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            import traceback
            traceback.print_exc()  # Imprimir la traza del error
            return {"error": str(e)}
        finally:
            if conexion:
                conexion.close()
