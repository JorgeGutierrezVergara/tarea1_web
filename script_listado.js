import { actividades } from "./actividades.js";

const contenedor = document.getElementById("recentactivities");

const cargar_actividades = () => {
  console.log(actividades);
  actividades.forEach((item) => {
    let tdisplay = 0;
    let imgExpanded = 0;
    const contenedor_actividad = document.createElement("div");
    contenedor_actividad.style.paddingBottom = "30px";

    const elementoLista = document.createElement("li");
    const boton = document.createElement("button");
    boton.innerHTML = `mostrar info`;
    elementoLista.textContent = item[4];

    const tabla = document.createElement("table");
    const thead = document.createElement("thead");
    thead.innerHTML = `
      <tr>
        <th>inicio</th>
        <th>termino</th>
        <th>comuna</th>
        <th>sector</th>
        <th>tema</th>
        <th>organizador</th>
        <th>fotos</th>
      </tr>
    `;

    const tbody = document.createElement("tbody");
    const img = document.createElement("img");
    img.src = item[6];
    img.style.width = "320px";
    img.style.height = "240px";
    img.style.cursor = "pointer";

    const toggleImagen = () => {
      imgExpanded = !imgExpanded;
      img.style.width = imgExpanded ? "800px" : "320px";
      img.style.height = imgExpanded ? "600px" : "240px";
    };

    img.addEventListener("click", toggleImagen);

    tbody.innerHTML = `
      <tr>
        <td>${item[0]}</td>
        <td>${item[1]}</td>
        <td>${item[2]}</td>
        <td>${item[3]}</td>
        <td>${item[4]}</td>
        <td>${item[5]}</td> 
        <td></td>
      </tr>
    `;
    tbody.rows[0].cells[6].appendChild(img);

    tabla.appendChild(thead);
    tabla.appendChild(tbody);
    tabla.style.display = "none";

    const toggleTabla = () => {
      if (tdisplay == 1) {
        tdisplay = 0;
        tabla.style.display = "none";
        boton.innerHTML = `mostrar info`;
      } else {
        tdisplay = 1;
        tabla.style.display = "table";
        boton.innerHTML = `esconder info`;
      }
    };

    boton.addEventListener("click", toggleTabla);

    contenedor_actividad.appendChild(elementoLista);
    contenedor_actividad.appendChild(boton);
    contenedor_actividad.appendChild(tabla);
    contenedor.appendChild(contenedor_actividad);
  });
};

window.onload = () => {
  cargar_actividades();
};
