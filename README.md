# Recibos developer

# Back

1-  Crear el achivo .env para las variables de entorno. Dejo un ejemplo del la coneccion a db de test. Tener en cuenta los puertos ya que la comunicacion es interna y los puetos de la api son los configurados en el servicio, no en el docker-compose.

```
DATABASE_USER="pablo",
DATABASE_PASS="P4bl0",
DATABASE_HOST="10.5.0.124",
DATABASE_PORT=3306
DATABASE="recibosdb"
VITE_API_BASE_URL=http://recibos_api:8000
VITE_LDAP_API=http://10.5.0.124:8000
```

# Front

1- Instalar dependencias en src/front 
```bash
npm install
```

2- Levantar el servicio con 
```bash
docker-compose up
```
