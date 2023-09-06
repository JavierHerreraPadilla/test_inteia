# Utiliza una imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requerimientos (requirements.txt) e instala las dependencias
COPY requirements.txt .

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el resto de los archivos de tu aplicación al contenedor
COPY . .

# Expone el puerto en el que se ejecutará tu aplicación FastAPI
EXPOSE 8000

# Comando para ejecutar tu aplicación FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
