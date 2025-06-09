# tarea3_web

tarea3_web

Para ejecutar esta tarea hay que abrir una terminal en la raíz de la misma y ejecutar:
python -m venv venv
y luego instalar las dependencias con:
.\venv\Scripts\activate
Una vez creado el ambiente, ejecutar la siguiente línea para cargar la base de datos:
python ".\setup_db.py"
luego ejecutar:
python "app.py"
y dirigirse al enlace que entrega la consola

- Se corrigió lo que pude notar que falló en la Tarea 2
- Se añadieron las funcionalidades de comentarios en posts
- Se añadieron los gráficos dinámicos de estadísticas
- Se incluyó un script que ejecuta los scripts .sql en el orden necesario -> crear la base de datos tarea2, poblar las tablas region y comuna, crear tabla-comentario y un script adicional para poblar las tablas con ejemplos.
