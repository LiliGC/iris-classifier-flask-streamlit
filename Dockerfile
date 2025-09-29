
# Usar una imagen base de Python 3.10
FROM python:3.10-slim-buster

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requisitos e instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --timeout=100

# Copiar el resto del código de la aplicación al directorio de trabajo
COPY . .

# Exponer el puerto para la API Flask (5000) y para el frontend Streamlit (8501)
EXPOSE 5000
EXPOSE 8501

# El comando de inicio (CMD) será proporcionado por docker-compose para cada servicio.
# No se necesita un CMD por defecto aquí.
