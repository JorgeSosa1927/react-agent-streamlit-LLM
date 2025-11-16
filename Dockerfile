# Usa una imagen oficial de Python ligera
FROM python:3.11-slim

# Instala herramientas necesarias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia todo el código del proyecto al contenedor
COPY . .

# Instala dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto de Streamlit
EXPOSE 8501

# Comando para lanzar la app
CMD ["streamlit", "run", "app.py", "--server.port=${PORT}", "--server.address=0.0.0.0"]


