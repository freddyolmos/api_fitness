# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos requeridos
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Comando por defecto para ejecutar el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
