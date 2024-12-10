from fastapi.responses import JSONResponse
from routers import conexion
from typing import Optional
from .emailService import EmailService
class Usuario(conexion.Conexion):
    def __init__(self, id_usuario: Optional[str] = None):
        self.id_usuario = id_usuario
        self._habilitado = None
        self._nombre = None
        self._apellido = None
        self._cuil = None
        self._legajo = None
        self._email = None
        self.proceso_cambio_pass = None
        self.validacionCorreo = None


    @property
    def habilitado(self):
        return self._habilitado

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellido(self):
        return self._apellido

    @property
    def cuil(self):
        return self._cuil

    @property
    def legajo(self):
        return self._legajo

    @property
    def email(self):
        return self._email 

  
    
    ################################################################

    ###CARGA LOS DATOS DEL OBJETO DE LA BASE DE DATOS :)

    async def cargar_usuario(self):
        """Método para cargar los datos del usuario desde la base de datos."""
        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql = "SELECT nombre, apellido, cuil, legajo, email, habilitado, proceso_cambio_pass,validacionCorreo FROM usuarios WHERE id_usuario = %s"
            cursor.execute(sql, (self.id_usuario,))
            result = cursor.fetchone()
            if result:
                self._nombre, self._apellido, self._cuil, self._legajo, self._email, self._habilitado, self.proceso_cambio_pass,self.validacionCorreo  = result
            else:
                raise ValueError(f"Usuario con id {self.id_usuario} no encontrado.")
        finally:
            conexion.close()

################################################################################################

    async def cambiar_estado(self, nuevo_estado):
        """Método para activar o desactivar un usuario."""
        if nuevo_estado not in [True, False]:
            raise ValueError("El habilitado debe ser habilitado (1) o deshabilitado (0).")

        conexion = self.conectar()
        try:
            cursor = conexion.cursor()
            sql_update = """
            UPDATE usuarios
            SET estado = %s
            WHERE id_usuario = %s
            """
            cursor.execute(sql_update, (nuevo_estado, self.id_usuario))
            conexion.commit()

            # Verifica si realmente se cambió el estado
            sql_select = "SELECT habilitado FROM usuarios WHERE id_usuario = %s"
            cursor.execute(sql_select, (self.id_usuario,))
            result = cursor.fetchone()

            if result and result[0] == nuevo_estado:
                self._estado = nuevo_estado
                return {"status": "success", "estado": nuevo_estado, "id_usuario": self.id_usuario}
            else:
                return {"status": "error", "message": "Error al actualizar el estado.s"}
        finally:
            conexion.close()

################################################################################################


    async def update(self, nombre=None, apellido=None, cuil=None, legajo=None, email=None):
        print("entro a update")
        """Método para modificar los datos del usuario."""
        conexion = self.conectar()
        usuario = Usuario(id_usuario=self.id_usuario)
        await usuario.cargar_usuario()

    # Validación de si no se han registrado cambios
        if (usuario.email == email and usuario.cuil == cuil and
            usuario.legajo == legajo and usuario.nombre == nombre and usuario.apellido == apellido):
            return {"status": "error", "message": "No se registraron cambios."}

        # Verificar si ya existe otro usuario con el mismo CUIL, legajo o email
        try:            
            # Verificar si ya existe otro usuario con el mismo CUIL, legajo o email
            print(nombre, apellido, cuil, legajo, email)
            resultado_validacion = await self.validarCuilEmailLegajo(cuil, legajo, email,self.id_usuario)
            if resultado_validacion:
                return resultado_validacion          

            # Actualizar datos si no hay duplicados
            cursor = conexion.cursor()
            sql_update = """
            UPDATE usuarios
            SET nombre = %s, apellido = %s, cuil = %s, legajo = %s, email = %s
            WHERE id_usuario = %s
            """
            cursor.execute(sql_update, (nombre, apellido, cuil, legajo, email, self.id_usuario))
            conexion.commit()

            # Cargar los nuevos datos del usuario después de la actualización
            await self.cargar_usuario()  # Actualiza el objeto con los nuevos valores
            return {"status": "success", "message": "Usuario modificado con éxito."}

        finally:
            conexion.close()


################################################################################################



    async def insert(self, nombre, apellido, cuil, legajo, email, habilitado=1):
        conexion = self.conectar()
        email_service = EmailService("reciboshnap@hospitalposadas.gob.ar", "Hn4pr3cib0s")
        try:
            cursor = conexion.cursor()    
            # Generar una contraseña provisoria
            contrasena_provisoria = email_service.generar_contrasena_provisoria()   
             # Verificar si ya existe otro usuario con el mismo CUIL, legajo o email
            resultado_validacion = await self.validarCuilEmailLegajo(cuil, legajo, email)
            if resultado_validacion:
                return resultado_validacion    

            # Insertar el nuevo usuario
            sql_insert = """
            INSERT INTO usuarios (nombre, apellido, cuil, legajo, email, habilitado, pass)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (nombre, apellido, cuil, legajo, email, habilitado, contrasena_provisoria))
            conexion.commit()

            # Obtener el id del nuevo usuario
            self.id_usuario = cursor.lastrowid

            # Enviar el correo con la contraseña provisoria
            asunto = "Bienvenido a la plataforma"
            cuerpo = f"""
            Hola {nombre} {apellido},

            Te damos la bienvenida a nuestra plataforma.

            Tu contraseña provisoria es: {contrasena_provisoria}

            Te recomendamos cambiarla lo antes posible.

            Saludos cordiales,
            El equipo.
            """
            email_service.enviar_correo(email, asunto, cuerpo)

            # Cargar los datos del nuevo usuario en el objeto
            await self.cargar_usuario()

            return {"status": "success", "message": "Usuario creado con éxito y correo enviado.", "id_usuario": self.id_usuario}
        finally:
            conexion.close()

################################################################################################


    async def validarCuilEmailLegajo(self, cuil, legajo, email,id_usuario=None):  
             
        """Método para validar si el CUIL, legajo o email ya están en uso por otro usuario."""
        try:                
            conexion = self.conectar()            
            cursor = conexion.cursor()
                # Verificar duplicado de CUIL
            if id_usuario is None:
                # Caso para insertar (nuevo usuario)
                sql_cuil = "SELECT * FROM usuarios WHERE cuil = %s"
                cursor.execute(sql_cuil, (cuil,))
            else:
                # Caso para actualizar (excluir el mismo id_usuario)
                sql_cuil = "SELECT * FROM usuarios WHERE cuil = %s AND id_usuario != %s"
                cursor.execute(sql_cuil, (cuil, id_usuario))

            result_cuil = cursor.fetchone()
            if result_cuil:
                return {"status": "error", "message": "El CUIL ya está en uso por otro usuario."}

             # Verificar duplicado de LEGAJO
            if id_usuario is None:
                # Caso para insertar (nuevo usuario)
                sql_cuil = "SELECT * FROM usuarios WHERE legajo = %s"
                cursor.execute(sql_cuil, (legajo,))
            else:
                # Caso para actualizar (excluir el mismo id_usuario)
                sql_cuil = "SELECT * FROM usuarios WHERE legajo = %s AND id_usuario != %s"
                cursor.execute(sql_cuil, (legajo, id_usuario))

            result_legajo = cursor.fetchone()
            print (result_legajo)
            if result_legajo:
                return {"status": "error", "message": "El legajo ya está en uso por otro usuario."}

                # Verificar duplicado de EMAL
            if id_usuario is None:
                # Caso para insertar (nuevo usuario)
                sql_cuil = "SELECT * FROM usuarios WHERE email = %s"
                cursor.execute(sql_cuil, (email,))
            else:
                # Caso para actualizar (excluir el mismo id_usuario)
                sql_cuil = "SELECT * FROM usuarios WHERE email = %s AND id_usuario != %s"
                cursor.execute(sql_cuil, (email, id_usuario))
            result_email = cursor.fetchone()
            print (result_email)
            if result_email:
                return {"status": "error", "message": "El email ya está en uso por otro usuario."}
            
            return None  # No hay duplicados, retornar None
        except Exception as e:
            return {"status": "error", "message": f"Error en la validación: {str(e)}"}


################################################################################################

    async def resetPassword(self):
            email_service = EmailService("reciboshnap@hospitalposadas.gob.ar", "Hn4pr3cib0s")
            conexion = self.conectar()
            usuario = Usuario(id_usuario=self.id_usuario)           
            await usuario.cargar_usuario() 
            print("paso por aca : ",usuario.email)
                ####// Evaluar el valor de proceso_cambio_pass y validacionCorreo
            if usuario.proceso_cambio_pass =='1':
                ###proceso de cambio de contraseña en proceso
                return {"status": "Error", "message": "Usuario con proceso de cambio de contraseña en proceso.", "id_usuario": self.id_usuario}
            if usuario.validacionCorreo==0:
               ##//correo electronico no validado 
                return {"status": "Error", "message": "Usuario con correo electronico no validado .", "id_usuario": self.id_usuario}
            if  (usuario.email == None) or (usuario.email ==''):               

                return {"status": "Error", "message": "El usuario no posee correoe electronico. Ingrese uno.", "id_usuario": self.id_usuario}
            try:  
                proceso_cambio_pass= 1
                contrasena_provisoria = email_service.generar_contrasena_provisoria()   
                # Actualizar datos si no hay duplicados
                cursor = conexion.cursor()
                sql_update = """
                UPDATE usuarios
                SET pass = %s ,proceso_cambio_pass =  %s
                WHERE id_usuario = %s
                """
                cursor.execute(sql_update, (contrasena_provisoria,proceso_cambio_pass, usuario.id_usuario))
                conexion.commit()
                    # Obtener el id del nuevo usuario
                self.id_usuario = cursor.lastrowid

                # Enviar el correo con la contraseña provisoria
                asunto = "Bienvenido a la plataforma"
                cuerpo = f"""
                Hola {usuario.nombre} {usuario.apellido},

                Queremos informarte que la contraseña del sistema de recibos de sueldo fue restablecida con éxito.

                Tu contraseña provisoria es: {contrasena_provisoria}

                Te recomendamos cambiarla lo antes posible.

                Saludos cordiales,
                El equipo.
                """
                email_service.enviar_correo(usuario.email, asunto, cuerpo)
                # Cargar los datos del nuevo usuario en el objeto

                return {"status": "success", "message": "Contraseña restablecida con éxito y correo enviado.", "id_usuario": usuario.id_usuario}
            finally:
                conexion.close()


################################################################################################
 
    async def newPassword(self, password, password1):
        conexion = self.conectar()
        usuario = Usuario(id_usuario=self.id_usuario)
        await usuario.cargar_usuario()
        print("a ver que tiene el objeto",usuario.nombre)
        # Evaluar el valor de proceso_cambio_pass y validacionCorreo
        if usuario.proceso_cambio_pass == 1:
            if usuario.validacionCorreo == 0:
                return {"status": "Error", "message": "Usuario con correo aun no validado, debe validarlo.", "id_usuario": usuario.id_usuario}            
            if password == password1:
                try:
                    proceso_cambio_pass = 0
                    # Actualizar datos si no hay duplicados
                    cursor = conexion.cursor()
                    sql_update = """
                    UPDATE usuarios
                    SET pass = %s, proceso_cambio_pass = %s
                    WHERE id_usuario = %s
                    """
                    cursor.execute(sql_update, (password, proceso_cambio_pass, usuario.id_usuario))
                    conexion.commit()
                    # Obtener el id del nuevo usuario
                    self.id_usuario = cursor.lastrowid
                    return {"status": "success", "message": "Su nueva contraseña fue guardada con éxito.", "id_usuario": usuario.id_usuario}
                finally:
                    conexion.close()
            else:  # Aquí, si las contraseñas no coinciden
                return {"status": "Error", "message": "Las contraseñas ingresadas no coinciden.", "id_usuario": self.id_usuario}
        else:  # Si proceso_cambio_pass no es '1'
            return {"status": "Error", "message": "No tiene un proceso de cambio de contraseña activo.", "id_usuario": usuario.id_usuario}

  
################################################################################################


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
