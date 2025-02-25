
from fastapi import Header, HTTPException, Depends
from typing import List
from models.validateTokenApi import Token
from models.getRol import GetRol

def validar_token_con_roles(roles_permitidos: List[int]):
    async def validar_token(authorization: str = Header(None)):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="El token debe incluir el prefijo 'Bearer'.")
        
        # Extraer el token sin el prefijo 'Bearer'
        token = authorization.split(" ")[1]
        resultado = await Token.checkTokenGeneral(token)  # Validar el token
                #consultar el rol en get rol si es ldap        

        if resultado.get("validate"):
            # Extraer el rol del token
            rol = resultado.get("data", {}).get("rol")
        elif resultado.get("valid"):
            #logica para consultar el rol
            getRol= GetRol()
            resultado = await getRol.get_rol_function(token)
            # Extraer el rol del token
            rol = resultado.get("rol")       

        # Convertir el rol a entero si es necesario
        try:
            rol = int(rol)
        except ValueError:
            raise HTTPException(status_code=400, detail="El rol no es válido.")

        # Verificar si el rol está permitido
        if rol not in roles_permitidos:
            raise HTTPException(status_code=403, detail="Acceso denegado. Rol no autorizado.")

        return True  # Devuelve True si el token y el rol son válidos
    
    return validar_token  # Retorna la función que FastAPI usará como `Depends()`
    return True
