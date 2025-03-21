import jwt
import datetime
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = "STOCK"  # Cambia esto por una clave secreta segura

class token:
    @staticmethod    
    def create_jwt_token(id_usuario,rol,cuil):
        payload = {
            "user_id": id_usuario,
            "rol": rol,
            "cuil": cuil,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)  # El token expira en 10 minutos
        }    
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token 

    @staticmethod
    def check_token(token: str) -> dict:
        """
        Decodifica y valida un token JWT.
        """
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise ValueError("El token ha expirado.")
        except InvalidTokenError:
            raise ValueError("El token no es válido.")