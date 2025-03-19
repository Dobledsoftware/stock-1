# Recibos developer

# Back

1- crear el achivo .env para las variables de entorno. Dejo un ejemplo del la coneccion a db de test

```
DATABASE_USER="postgres"
DATABASE_PASS="DarioDavid-bd-UBU-1"
DATABASE_HOST="92.112.176.191"
DATABASE_PORT=5432
DATABASE="stock_TEST"
VITE_API_BASE_URL=http://92.112.176.191:8085
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
