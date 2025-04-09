# tarea1_web

tarea1_web

Para ejecutar esta tarea hay que abrir una terminal en la raíz de la misma y ejecutar:
python -m http.server 8000
una vez hecho esto, dirigirse a http://localhost:8000/index.html

- El título de la página y los nombres de las secciones son clickeables para navegar en la aplicación
- En la landing page se pueden ver las últimas cinco actividades creadas
- En agregar actividad se encuentra el form para verificación. No se implementó la verificación de las fechas
  porque la librería que intenté usar me estaba dando fallos. La imagen no pude solucionarlo. Tampoco se implementó que al seleccionar "otro" en "Contacto" o "Tema" se despliegue el input para escribir. Tampoco la confirmación final para enviar el form. El form sí es capaz de verificar los otros campos e informar al usuario de cuáles de ellos presentan errores y de no haberlos, nmuestra un mensaje de éxito.
- En "Ver otras actividades" se implementó una lista con las actividades y botones que despliegan u ocultan sus respectivas tablas con información. No se implementó ver imágenes múltiples, pero la mostrada es clickeable y se agranda o reduce.
- En estaídisticas se colocaron los gráficos, estos fueron hechos en python con matplotlib y numpy.
