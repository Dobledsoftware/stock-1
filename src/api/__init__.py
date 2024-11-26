from fastapi import FastAPI
from .routers import end_point_tabla_recibos
from .routers import end_point_desactiva_recibos
app = FastAPI()

# Incluye el enrutador de recibos
app.include_router(end_point_tabla_recibos.router)
app.include_router(end_point_desactiva_recibos.router)