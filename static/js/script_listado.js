import { actividades } from "./actividades.js";

const contenedorTabla = document.getElementById("recentactivities");
let contenedorDetalle = document.getElementById("detalle_actividad_vista");

const crearTablaResumen = () => {
  const titulo = contenedorTabla.querySelector("h3");
  contenedorTabla.innerHTML = "";
  if (titulo) {
    contenedorTabla.appendChild(titulo); // Vuelve a poner el título
  }

  const tabla = document.createElement("table");
  tabla.id = "tabla_resumen_actividades";

  const thead = tabla.createTHead();
  const filaEncabezado = thead.insertRow();
  const columnasEncabezado = [
    "Inicio",
    "Término",
    "Comuna",
    "Sector",
    "Tema(s)",
    "Organizador",
    "Total Fotos",
  ];
  columnasEncabezado.forEach((textoColumna) => {
    const th = document.createElement("th");
    th.textContent = textoColumna;
    filaEncabezado.appendChild(th);
  });

  const tbody = tabla.createTBody();
  const actividadesAMostrar = actividades.slice(0, 5);

  actividadesAMostrar.forEach((actividad) => {
    const fila = tbody.insertRow();

    fila.dataset.actividadId = actividad.id; //guardamos el id de la actividad

    fila.insertCell().textContent = actividad.diaHoraInicio || "N/A";
    fila.insertCell().textContent = actividad.diaHoraTermino || "N/A";
    fila.insertCell().textContent = actividad.comuna || "N/A";
    fila.insertCell().textContent = actividad.sector || "N/A";

    const temasTexto =
      Array.isArray(actividad.temas) && actividad.temas.length > 0
        ? actividad.temas.join(", ")
        : actividad.nombreActividad || "N/A";
    fila.insertCell().textContent = temasTexto;

    fila.insertCell().textContent = actividad.nombreOrganizador || "N/A";

    const totalFotos = Array.isArray(actividad.fotos)
      ? actividad.fotos.length
      : 0;
    fila.insertCell().textContent = totalFotos;

    fila.style.cursor = "pointer";
    fila.addEventListener("click", function () {
      const idClickeado = this.dataset.actividadId;
      contenedorDetalle.innerHTML = "";
      mostrarDetalleActividad(idClickeado);

      const actividadSeleccionada = actividades.find(
        (act) => act.id === parseInt(idClickeado)
      );

      if (actividadSeleccionada) {
        console.log(
          "Descripción de la actividad seleccionada:",
          actividadSeleccionada.descripcionActividad ||
            "No hay descripción disponible."
        );
      } else {
        console.log("No se encontró la actividad con ID:", idClickeado);
      }
    });
  });

  contenedorTabla.appendChild(tabla);
};

const mostrarDetalleActividad = (actividadId) => {
  const tablaPrincipal = document.getElementById("tabla_resumen_actividades");

  if (tablaPrincipal) {
    tablaPrincipal.style.display = "none";
  }

  const actividad = actividades.find((act) => act.id === parseInt(actividadId));
  console.log("actividad = " + actividad.descripcionActividad);
  contenedorDetalle.style.display = "block";

  const listaDetalles = document.createElement("ul");
  listaDetalles.className = "lista-detalles-actividad";

  const contactos = (listacontactos) => {
    let res = "";
    listacontactos.forEach((contacto) => {
      res += contacto.tipo;
      res += ": ";
      res += contacto.valor;
      res += " | ";
    });
    return res;
  };

  const temas = (listatemas) => {
    let res = "";
    listatemas.forEach((tema) => {
      res += tema;
      res += " | ";
    });
    return res;
  };

  const addDetalleItem = (etiqueta, valor) => {
    const li = document.createElement("li");
    const valorMostrado = valor;
    li.innerHTML = `${etiqueta}: ${valorMostrado}`;
    listaDetalles.appendChild(li);
  };
  addDetalleItem("Día y Hora de Inicio", actividad.diaHoraInicio);
  addDetalleItem("Día y Hora de Término", actividad.diaHoraTermino);

  addDetalleItem("Región", actividad.region);
  addDetalleItem("Comuna", actividad.comuna);
  addDetalleItem("Sector", actividad.sector);

  addDetalleItem("Organizador", actividad.nombreOrganizador);
  addDetalleItem("Email del Organizador", actividad.emailOrganizador);
  addDetalleItem(
    "Celular del Organizador",
    actividad.celularOrganizador ? actividad.celularOrganizador : "N/A"
  );
  addDetalleItem("Contacto", contactos(actividad.contactarPor));

  addDetalleItem("Descripcion", actividad.descripcionActividad);
  addDetalleItem("Tema", temas(actividad.temas));

  const divFotos = document.createElement("div");

  contenedorDetalle.appendChild(listaDetalles);
  actividad.fotos.forEach((urlFoto) => {
    const imgElement = document.createElement("img");
    imgElement.src = urlFoto;
    imgElement.alt = `Foto de ${actividad.nombreActividad || "la actividad"}`;
    imgElement.style.width = "320px";
    imgElement.style.height = "240px";
    imgElement.style.margin = "5px";
    imgElement.style.objectFit = "cover";
    imgElement.addEventListener("click", function () {
      abrirModalConImagen(urlFoto);
    });
    divFotos.appendChild(imgElement);
  });
  contenedorDetalle.appendChild(divFotos);

  const divBotones = document.createElement("div");
  divBotones.style.marginTop = "20px";

  const btnVolverAlListado = document.createElement("button");
  btnVolverAlListado.textContent = "Volver al Listado";
  btnVolverAlListado.type = "button";
  btnVolverAlListado.style.marginRight = "10px";
  btnVolverAlListado.onclick = function () {
    contenedorDetalle.style.display = "none";
    tablaPrincipal.style.display = "block";
  };
  divBotones.appendChild(btnVolverAlListado);

  const btnVolverAPortada = document.createElement("a");
  btnVolverAPortada.textContent = "Volver a la Portada";
  btnVolverAPortada.href = "index.html";
  btnVolverAPortada.className = "button-link";
  divBotones.appendChild(btnVolverAPortada);

  contenedorDetalle.appendChild(divBotones);
};

const modalImagenGrande = document.getElementById(
  "modal_imagen_grande_listado"
);
const imgGrande = document.getElementById("imagen_grande_src_listado");
const btnCerrarImgGrande = document.getElementById(
  "btn_cerrar_img_grande_listado"
);

btnCerrarImgGrande.onclick = () => {
  modalImagenGrande.style.display = "none";
};
modalImagenGrande.onclick = (event) => {
  if (event.target === modalImagenGrande) {
    modalImagenGrande.style.display = "none";
  }
};

function abrirModalConImagen(urlDeLaImagen) {
  if (imgGrande && modalImagenGrande) {
    imgGrande.src = urlDeLaImagen;
    imgGrande.style.maxWidth = "800px";
    imgGrande.style.maxHeight = "600px";

    modalImagenGrande.style.display = "flex";
    console.log("Modal de imagen abierto con:", urlDeLaImagen);
  } else {
    console.error(
      "El modal de imagen o el elemento <img> grande no están listos."
    );
  }
}
window.onload = () => {
  crearTablaResumen();
};
