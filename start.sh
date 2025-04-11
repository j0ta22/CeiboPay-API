#!/bin/bash

# Crear y activar el entorno virtual si no existe
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

# Activar el entorno virtual
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones de la base de datos
alembic upgrade head

# Iniciar el servidor
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
