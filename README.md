# API de Gestión y Validación de Documentos

Prueba Tecnica Backend desarrollado en Python utilizando Django y Django REST Framework

# Instrucciones para Ejecutar el Proyecto

Sigue estos pasos

1. Clonar el repositorio y entrar

   git clone <url-del-repositorio>
   cd <nombre-del-proyecto>
   
3. Crear y activar el entorno virtual
  python -m venv venv
  # En Windows:
  venv\Scripts\activate
  # En macOS/Linux:
  source venv/binExplic/activate

3. Instalar dependencias
   pip install -r requirements.txt
   
4. Configurar las variables de entorno (.env)

6. Aplicar las migraciones de la base de datos

    python manage.py makemigrations
    python manage.py migrate

7. Crear un superusuario
   python manage.py createsuperuser
   
8. Ejecutar el servidor de desarrollo (En 8000)
   python manage.py runserver

# Instrucciones para ejecutar las pruebas
1. Ejecutar el código de las pruebas
   python manage.py test

# Documentación básica de endpoints
1. Tener el servidor ejecutando
   python manage.py runserver

2. Desde el navegador ingresar a la url
   localhost:8000/api/docs/

# Link video
https://drive.google.com/file/d/12J98pcfeLOm8d6thYrlj-KilWRfZ37Y3/view?usp=drivesdk
https://drive.google.com/file/d/1xXT2doGCrSNPl1biBHa9kMR_mvM_bZBt/view?usp=drivesdk

#