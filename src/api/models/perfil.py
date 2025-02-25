from routers import conexion

class Perfil(conexion.Conexion):

    @staticmethod
    async def listar_perfiles(estado: bool):  # 🔹 Agregamos el parámetro `estado`
        """Obtener todos los perfiles filtrados por estado"""
        conexion = Perfil().conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_perfil, nombre, descripcion, estado, fecha_creacion FROM perfiles WHERE estado = %s", (estado,))
            perfiles = cursor.fetchall()

            if not perfiles:
                return {"message": "No hay perfiles disponibles en el estado solicitado", "code": 204}

            perfiles_list = [
                {
                    "id_perfil": row[0],
                    "nombre": row[1],
                    "descripcion": row[2],
                    "estado": row[3],
                    "fecha_creacion": row[4]
                }
                for row in perfiles
            ]

            return {"message": "Perfiles obtenidos exitosamente", "code": 200, "perfiles": perfiles_list}

        except Exception as e:
            print(f"Error al listar perfiles: {e}")
            return {"message": "Error interno al obtener perfiles", "code": 500}
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    async def crear_perfil(nombre: str, descripcion: str):
        """Crear un nuevo perfil"""
        conexion = Perfil().conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_perfil FROM perfiles WHERE nombre = %s", (nombre,))
            if cursor.fetchone():
                return {"message": "El perfil ya existe", "code": 409}

            cursor.execute("INSERT INTO perfiles (nombre, descripcion) VALUES (%s, %s) RETURNING id_perfil", (nombre, descripcion))
            conexion.commit()
            id_perfil = cursor.fetchone()[0]

            return {"message": "Perfil creado exitosamente", "code": 201, "id_perfil": id_perfil}

        except Exception as e:
            print(f"Error al crear perfil: {e}")
            return {"message": "Error interno al crear perfil", "code": 500}
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    async def modificar_perfil(id_perfil: int, nombre: str, descripcion: str):
        """Modificar un perfil existente"""
        conexion = Perfil().conectar()
        try:
            cursor = conexion.cursor()

            cursor.execute("SELECT nombre, descripcion FROM perfiles WHERE id_perfil = %s", (id_perfil,))
            datos_actuales = cursor.fetchone()
            if not datos_actuales:
                return {"message": "Perfil no encontrado", "code": 404}

            nuevos_datos = (nombre.strip(), descripcion.strip())
            datos_actuales = (datos_actuales[0].strip(), datos_actuales[1].strip())

            if datos_actuales == nuevos_datos:
                return {"message": "No se detectaron cambios en los datos del perfil", "code": 304}

            cursor.execute("UPDATE perfiles SET nombre = %s, descripcion = %s WHERE id_perfil = %s",
                           (nombre.strip(), descripcion.strip(), id_perfil))
            conexion.commit()

            return {"message": "Perfil actualizado correctamente", "code": 200}

        except Exception as e:
            print(f"Error al modificar perfil: {e}")
            return {"message": "Error interno al modificar perfil", "code": 500}
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    async def cambiar_estado_perfil(id_perfil: int, estado: bool):
        """Habilitar o deshabilitar un perfil"""
        conexion = Perfil().conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_perfil FROM perfiles WHERE id_perfil = %s", (id_perfil,))
            if not cursor.fetchone():
                return {"message": "Perfil no encontrado", "code": 404}

            cursor.execute("UPDATE perfiles SET estado = %s WHERE id_perfil = %s", (estado, id_perfil))
            conexion.commit()

            return {"message": f"Perfil {'habilitado' if estado else 'deshabilitado'} correctamente", "code": 200}

        except Exception as e:
            print(f"Error al cambiar estado del perfil: {e}")
            return {"message": "Error interno al cambiar estado del perfil", "code": 500}
        finally:
            cursor.close()
            conexion.close()
                
            
    async def asignar_usuario_a_perfil(id_usuario: int, id_perfil: int):
        """Asigna un usuario activo a un perfil con fecha de alta y estado"""
        conexion = Perfil().conectar()
        try:
            cursor = conexion.cursor()

            # Verificar si el usuario existe y está activo
            cursor.execute("SELECT estado FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            usuario = cursor.fetchone()
            if not usuario:
                return {"message": "Usuario no encontrado", "code": 404}
            if not usuario[0]:  
                return {"message": "El usuario no está activo", "code": 403}

            # Verificar si el perfil existe
            cursor.execute("SELECT id_perfil FROM perfiles WHERE id_perfil = %s", (id_perfil,))
            if not cursor.fetchone():
                return {"message": "Perfil no encontrado", "code": 404}

            # Verificar si el usuario ya tiene un perfil asignado
            cursor.execute("SELECT id_asignacion, estado FROM usuarios_perfiles WHERE id_usuario = %s", (id_usuario,))
            asignacion = cursor.fetchone()
            if asignacion:
                if asignacion[1]:  
                    return {"message": "El usuario ya tiene un perfil asignado", "code": 409}
                else:
                    # Reactivar la relación si estaba deshabilitada
                    cursor.execute("UPDATE usuarios_perfiles SET estado = TRUE, fecha_alta = NOW() WHERE id_usuario = %s",
                                (id_usuario,))
                    conexion.commit()
                    return {"message": "Usuario reasignado al perfil correctamente", "code": 200}

            # Insertar nueva asignación
            cursor.execute("INSERT INTO usuarios_perfiles (id_usuario, id_perfil, fecha_alta, estado) VALUES (%s, %s, NOW(), TRUE)",
                        (id_usuario, id_perfil))
            conexion.commit()

            return {"message": "Usuario asignado al perfil correctamente", "code": 201}

        except Exception as e:
            print(f"Error al asignar usuario a perfil: {e}")
            return {"message": "Error interno al asignar usuario al perfil", "code": 500}
        finally:
            cursor.close()
            conexion.close()




    @staticmethod
    async def obtener_usuarios_por_perfil(id_perfil: int, estado: bool = None):
        """Obtiene los usuarios de un perfil filtrados por estado (activos/inactivos)"""
        conexion = Perfil().conectar()
        try:
            cursor = conexion.cursor()

            # Verificar si el perfil existe
            cursor.execute("SELECT id_perfil FROM perfiles WHERE id_perfil = %s", (id_perfil,))
            if not cursor.fetchone():
                return {"message": "Perfil no encontrado", "code": 404}

            # Construir la consulta según el estado solicitado
            sql = """
                SELECT u.id_usuario, u.nombre, u.apellido, u.email, u.usuario, up.estado
                FROM usuarios u
                JOIN usuarios_perfiles up ON u.id_usuario = up.id_usuario
                WHERE up.id_perfil = %s
            """
            valores = [id_perfil]

            if estado is not None:  # Si se especificó estado, filtrar por él
                sql += " AND up.estado = %s"
                valores.append(estado)

            cursor.execute(sql, tuple(valores))
            usuarios = cursor.fetchall()

            if not usuarios:
                return {"message": "No hay usuarios con el estado solicitado en este perfil", "code": 204}

            usuarios_list = [
                {
                    "id_usuario": row[0],
                    "nombre": row[1],
                    "apellido": row[2],
                    "email": row[3],
                    "usuario": row[4],
                    "estado": row[5]  # Incluye el estado de la relación
                }
                for row in usuarios
            ]

            return {"message": "Usuarios obtenidos exitosamente", "code": 200, "usuarios": usuarios_list}

        except Exception as e:
            print(f"Error al obtener usuarios por perfil: {e}")
            return {"message": "Error interno al obtener usuarios por perfil", "code": 500}
        finally:
            cursor.close()
            conexion.close()



    @staticmethod
    async def obtener_funciones_por_perfil(id_perfil: int):
        """Obtiene todas las funciones asignadas a un perfil con sus permisos"""
        conexion = Perfil().conectar()
        try:
            cursor = conexion.cursor()

            # Verificar si el perfil existe
            cursor.execute("SELECT id_perfil FROM perfiles WHERE id_perfil = %s", (id_perfil,))
            if not cursor.fetchone():
                return {"message": "Perfil no encontrado", "code": 404}

            # Obtener funciones y permisos asignados al perfil
            sql = """
                SELECT f.id_funcion, f.nombre, f.descripcion, pf.lectura, pf.escritura
                FROM funciones f
                JOIN perfil_funcion pf ON f.id_funcion = pf.id_funcion
                WHERE pf.id_perfil = %s
            """
            cursor.execute(sql, (id_perfil,))
            funciones = cursor.fetchall()

            if not funciones:
                return {"message": "No hay funciones asignadas a este perfil", "code": 204}

            funciones_list = [
                {
                    "id_funcion": row[0],
                    "nombre": row[1],
                    "descripcion": row[2],
                    "lectura": row[3],
                    "escritura": row[4]
                }
                for row in funciones
            ]

            return {"message": "Funciones obtenidas exitosamente", "code": 200, "funciones": funciones_list}

        except Exception as e:
            print(f"Error al obtener funciones por perfil: {e}")
            return {"message": "Error interno al obtener funciones del perfil", "code": 500}
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    async def agregar_funcion_a_perfil(id_perfil: int, id_funcion: int, escritura: bool):
        """Asigna una función a un perfil con `lectura = TRUE` por defecto"""
        conexion = Perfil().conectar()
        try:
            cursor = conexion.cursor()

            # Verificar si el perfil existe
            cursor.execute("SELECT id_perfil FROM perfiles WHERE id_perfil = %s", (id_perfil,))
            if not cursor.fetchone():
                return {"message": "Perfil no encontrado", "code": 404}

            # Verificar si la función existe
            cursor.execute("SELECT id_funcion FROM funciones WHERE id_funcion = %s", (id_funcion,))
            if not cursor.fetchone():
                return {"message": "Función no encontrada", "code": 404}

            # Verificar si ya está asignada
            cursor.execute("SELECT id_funcion FROM perfil_funcion WHERE id_perfil = %s AND id_funcion = %s", (id_perfil, id_funcion))
            if cursor.fetchone():
                return {"message": "La función ya está asignada a este perfil", "code": 409}

            # Asignar la función al perfil con lectura = TRUE y escritura = parámetro
            cursor.execute("INSERT INTO perfil_funcion (id_perfil, id_funcion, lectura, escritura) VALUES (%s, %s, TRUE, %s)",
                        (id_perfil, id_funcion, escritura))
            conexion.commit()

            return {"message": "Función asignada correctamente al perfil", "code": 201}

        except Exception as e:
            print(f"Error al asignar función al perfil: {e}")
            return {"message": "Error interno al asignar función al perfil", "code": 500}
        finally:
            cursor.close()
            conexion.close()


    @staticmethod
    async def eliminar_funcion_de_perfil(id_perfil: int, id_funcion: int):
        """Elimina una función de un perfil"""
        conexion = Perfil().conectar()
        try:
            cursor = conexion.cursor()

            # Verificar si la función está asignada al perfil
            cursor.execute("SELECT id_funcion FROM perfil_funcion WHERE id_perfil = %s AND id_funcion = %s", (id_perfil, id_funcion))
            if not cursor.fetchone():
                return {"message": "La función no está asignada a este perfil", "code": 404}

            # Eliminar la función del perfil
            cursor.execute("DELETE FROM perfil_funcion WHERE id_perfil = %s AND id_funcion = %s", (id_perfil, id_funcion))
            conexion.commit()

            return {"message": "Función eliminada del perfil correctamente", "code": 200}

        except Exception as e:
            print(f"Error al eliminar función del perfil: {e}")
            return {"message": "Error interno al eliminar función del perfil", "code": 500}
        finally:
            cursor.close()
            conexion.close()


    async def listar_funciones():
        """Obtiene todas las funciones disponibles en el sistema"""
        conexion = Perfil().conectar()
        try:
            cursor = conexion.cursor()

            # Obtener todas las funciones
            sql = "SELECT id_funcion, nombre, descripcion FROM funciones ORDER BY id_funcion"
            cursor.execute(sql)
            funciones = cursor.fetchall()

            if not funciones:
                return {"message": "No hay funciones registradas", "code": 204}

            funciones_list = [
                {
                    "id_funcion": row[0],
                    "nombre": row[1],
                    "descripcion": row[2]
                }
                for row in funciones
            ]

            return {"message": "Funciones obtenidas exitosamente", "code": 200, "funciones": funciones_list}

        except Exception as e:
            print(f"Error al obtener funciones: {e}")
            return {"message": "Error interno al obtener funciones", "code": 500}
        finally:
            cursor.close()
            conexion.close()




            