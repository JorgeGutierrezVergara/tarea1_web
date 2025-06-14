# tarea3_web

tarea3_web

Cómo ejecutar la tarea:

1. Abrir una terminal en la raíz de la misma y ejecutar:
   > python -m venv venv
2. Instalar las dependencias con:
   > .\venv\Scripts\activate
3. Una vez creado el ambiente y estando en éste, cargar y poblar la base de datos con:
   > python .\setup_db.py
4. Correr el servidor:
   > python app.py
5. Dirigirse al enlace que entrega la consola

- Se corrigió lo que pude notar que falló en la Tarea 2.
- Se añadieron las funcionalidades de comentarios en posts.
- Se añadieron los gráficos dinámicos de estadísticas.
- Se incluyó un script que ejecuta los scripts .sql en el orden necesario -> crear la base de datos tarea2, poblar las tablas region y comuna, crear tabla-comentario y un script adicional para poblar las tablas con ejemplos.
- Se hicieron ajustes visuales
