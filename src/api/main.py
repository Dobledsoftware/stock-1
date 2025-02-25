from fastapi import FastAPI
from routers import stockEndPoint
from routers import usuariosEP

from fastapi.middleware.cors import CORSMiddleware #libreria para mejorar seguridad CORS
app = FastAPI()
app.include_router(stockEndPoint.router)
app.include_router(usuariosEP.router)

#app.include_router(recibos.router)
#app.include_router(recibos.router)
# Solo importa la aplicación desde el paquete api
# Prueba para estas cosas!
# Lista de orígenes permitidos
origins = [
    "*"
]

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)
