import { actividades } from "./actividades.js";

const tablaPortada = document.getElementById("tabla");
const actividadesParaPortada = actividades.slice(0, 5);

actividadesParaPortada.forEach((actividad) => {
  const fila = tablaPortada.insertRow();

  fila.insertCell().textContent = actividad.diaHoraInicio || "N/A";
  fila.insertCell().textContent = actividad.diaHoraTermino || "N/A";
  fila.insertCell().textContent = actividad.comuna || "N/A";
  fila.insertCell().textContent = actividad.sector || "N/A";

  fila.insertCell().textContent =
    actividad.nombreActividad ||
    (actividad.temas && actividad.temas.length > 0
      ? actividad.temas[0]
      : "N/A");

  const celdaImagen = fila.insertCell();
  if (actividad.fotos && actividad.fotos.length > 0) {
    celdaImagen.innerHTML = `<img src="${actividad.fotos[0]}" alt="Foto de ${
      actividad.nombreActividad || "actividad"
    }" style="width: 100px; height: auto; object-fit: cover;">`;
  } else {
    celdaImagen.textContent = "Sin foto";
  }
});
