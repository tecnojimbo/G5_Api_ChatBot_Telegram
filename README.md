# G5_Api_ChatBot_Telegram
Practica 1 Tratamiento de Datos

Parte 1 – Construcción del API (app.py)
El núcleo del sistema es una API desarrollada en Python 3.10 con el framework Flask.
Funcionalidades y Endpoints:
Persistencia: Manejo de base de datos local en formato datos.json.
GET /api/productos/<cat>: Recupera productos filtrados por categoría (Laptops, Mouse, Audio, etc.).
POST /api/comprar/<int:id_p>: Procesa la compra disminuyendo el stock en tiempo real. Incluye validación de existencia de ID y disponibilidad de inventario.
Creatividad (Extra): Integración de un Bot de Telegram (tecjims_bot.py) que consume estos endpoints para ofrecer una interfaz de compra interactiva.
Se ejecuta localmente archivos app.py y tecjims_bot.py 

![Ejecucion app.py](img/image-4.png)    ![Ejecucion tecjims_bot.py.py](img/image-1.png)
 
