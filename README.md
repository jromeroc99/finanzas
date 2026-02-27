# backend-FastApi

Plantilla para backend genérico en FastAPI. Usando ORM SQLModel como base de datos. Incluye configuración para Docker Compose y manejo de migraciones con Alembic.

## Instalación y Setup

1. **Clona el repositorio:**
```bash
git clone git@github.com:jromeroc99/backend-FastApi.git
cd backend-FastApi
```


3. **Configura el backend:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
   El backend se ejecutará en el puerto por defecto (8000).

4. **Ejecuta las migraciones de base de datos:**
   ```bash
   cd backend
   alembic upgrade head
   ```
   Esto aplicará todas las migraciones pendientes a la base de datos MySQL.

## Migraciones de Base de Datos

El proyecto utiliza **Alembic** para manejar las migraciones de base de datos.

### Crear una nueva migración:
Cuando cambies los modelos de SQLModel, crea una nueva migración:
```bash
cd backend
alembic revision --autogenerate -m "descripción del cambio"
```

### Aplicar migraciones:
```bash
cd backend
alembic upgrade head
```

### Ver estado de migraciones:
```bash
cd backend
alembic current  # Muestra la migración actual
alembic history  # Muestra el historial de migraciones
```

### Revertir migraciones (si es necesario):
```bash
cd backend
alembic downgrade -1  # Revierte la última migración
```
