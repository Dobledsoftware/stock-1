from routers import conexion
import aiohttp
import asyncio
from .recibo import Recibo # Importa Clase Recibo

from fastapi.responses import JSONResponse

class GetRol(conexion.Conexion):  
    async def get_rol_function(self, token):        
        conexion = self.conectar()         
        url = "http://10.5.0.124:8000/check/validatetoken"  # URL del servicio

        # Crea los headers para la solicitud, incluyendo el token en el encabezado Authorization
        headers = {'Authorization': f'Bearer {token}'}
        async with aiohttp.ClientSession() as session:
            # Realiza la solicitud GET incluyendo los headers
            async with session.get(url, headers=headers) as response:
                data = await response.json() 
                if response.status == 200:
                    if "detail" in data:                        
                        return None  # O lanza una excepción según tu manejo de errores                    
                    elif "samaccountname" in data:                        
                        cursor = conexion.cursor()  # Usa self.conexion si es el atributo de tu clase base
                        sql = """
                            SELECT rol, cuil
                            FROM usuarios
                            WHERE cuil LIKE %s
                        """
                        # Agregar los caracteres '%' alrededor del valor que se busca
                        cursor.execute(sql, ('%' + data['samaccountname'] + '%',))  # Ejecuta la consulta con el valor del samaccountname
                        result = cursor.fetchone()  # Usa fetchone para obtener una fila
                        
                        if result:
                            rol, cuil = result  # Desempaqueta los valores de la tupla   
                            
                            # Actualizar el samaccountname en la base de datos
                            sql_update = """
                                UPDATE usuarios
                                SET samaccountname = %s
                                WHERE cuil = %s
                            """
                            cursor.execute(sql_update, (data['samaccountname'], cuil))

                            # Obtener el resto de los datos que necesitas
                            sql_full_data = """
                                SELECT id_usuario, rol, cuil, nombre, apellido, legajo, email
                                FROM usuarios
                                WHERE cuil = %s
                            """
                            cursor.execute(sql_full_data, (cuil,))
                            full_data = cursor.fetchone()  # Obtener la fila completa
                            
                            if full_data:
                                # Asumiendo que el orden de los datos en full_data corresponde a los nombres de columna
                                id_usuario, rol, cuil, nombre, apellido, legajo, email = full_data

                                # Genera el token y recibos como en tu lógica anterior
                                #auth_token = "tu_token_aqui"  # Reemplaza por la lógica para generar el token
                                #response_recibo = "tus_recibos_aqui"  # Reemplaza por la lógica para obtener los recibos
                                recibos = Recibo()  # Crea una instancia de la clase TodosLosRecibos.
                                response_recibo = await recibos.todosLosRecibos(cuil)
                                return {
                                    "cuil": cuil,
                                    "id_usuario": id_usuario,
                                    "rol": rol,
                                    "cuil": cuil,
                                    "nombre": nombre,
                                    "apellido": apellido,
                                    "legajo": legajo,
                                    "email": email,
                                    "auth_token": token,
                                    #"recibos": response_recibo 
                                    "recibos": response_recibo
                                }  # Devuelve los resultados como un diccionario
                            

                      
                        
                        self.conexion.close()  # Cierra la conexión a la base de datos                        
  
                     
                
                    
                    