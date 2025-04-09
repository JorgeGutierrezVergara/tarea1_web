import { actividades } from "./actividades.js";
// Index
const tabla = document.getElementById("tabla");
actividades.forEach((el) => {
  const fila = tabla.insertRow();

  fila.insertCell().textContent = el[0];
  fila.insertCell().textContent = el[1];
  fila.insertCell().textContent = el[2];
  fila.insertCell().textContent = el[3];
  fila.insertCell().textContent = el[4];

  const celdaImagen = fila.insertCell();
  celdaImagen.innerHTML = `<img src="${el[6]}" alt="Imagen" style="width: 100px; height: auto;">`;
});
