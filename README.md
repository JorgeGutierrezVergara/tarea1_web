# tarea3_web

tarea3_web

Para ejecutar esta tarea hay que abrir una terminal en la raíz de la misma y ejecutar:
python -m venv venv
Una vez creado el ambiente, instalar las dependencias con:
.\venv\Scripts\activate
una vez en el ambiente, ejecutar:
python "app.py"
y dirigirse al enlace que entrega la consola

- Todos los errores de la Tarea 1 fueron corregidos
- Se migró la app estática a flask
- Se cargó la base de datos de forma exitosa
- En el formulario, el selector de región y comuna se cargan dinámicamente con datos de la base de datos
- El formulario es capaz de tomar los datos y enviárselos al backend de flask, pero no se pudo implementar la subida a la base de datos
- Por este último punto, ninguna de las tablas de carga de forma dinámica con la base de datos.
