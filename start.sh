#!/bin/bash

# Activar el entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Instalar dependencias si no están instaladas
if [ ! -d "venv" ]; then
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Iniciar el servidor
uvicorn app.main:app --host 0.0.0.0 --port 10000 --reload
