# 1. Usamos una imagen base estable de Python
FROM python:3.10-slim

# 2. Evitamos que Python genere archivos .pyc y forzamos logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establecemos el directorio de trabajo
WORKDIR /app

# 4. REFUERZO DE SEGURIDAD: Actualizamos el sistema operativo base 
# Esto corrige las "vulnerabilidades críticas" que detectó VS Code
RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# 5. Copiamos e instalamos las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el resto de tu código (app.py, tecjims_bot.py, datos.json)
COPY . .

# 7. Exponemos el puerto de la API Flask
EXPOSE 5000

# 8. Comando por defecto (será sobrescrito por el docker-compose si es necesario)
CMD ["python", "app.py"]