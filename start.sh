#!/bin/bash

# Salir inmediatamente si un comando falla
set -e

# Iniciar la API de Flask en segundo plano
echo "Iniciando API de Flask con Waitress en el puerto 5000..."
waitress-serve --host=0.0.0.0 --port=5000 iris_app.api.app:app &

# Iniciar el frontend de Streamlit en primer plano
echo "Iniciando frontend de Streamlit en el puerto 8501..."
streamlit run iris_app/frontend/frontend.py --server.port=8501 --server.address=0.0.0.0