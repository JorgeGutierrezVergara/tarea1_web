document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("modal_imagen_grande");
  const imgGrande = document.getElementById("imagen_grande_src");

  window.abrirModalConImagen = function (urlDeLaImagen) {
    modal.style.display = "flex";
    imgGrande.src = urlDeLaImagen;
  };

  document.getElementById("btn_cerrar_img_grande").onclick = function () {
    modal.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };

  const listadoDiv = document.getElementById("comentarios-listado");
  const mensajeDiv = document.getElementById("comentarios-mensaje");

  const actividadId = listadoDiv.dataset.actividadId;

  fetch(`/api/actividad/${actividadId}/comentarios`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("La respuesta de la red no fue exitosa.");
      }
      return response.json();
    })
    .then((comentarios) => {
      mensajeDiv.remove();

      if (comentarios.length === 0) {
        const noComentarios = document.createElement("p");
        noComentarios.textContent =
          "Aún no hay comentarios para esta actividad. ¡Sé el primero!";
        listadoDiv.appendChild(noComentarios);
      } else {
        comentarios.forEach((comentario) => {
          const comentarioDiv = document.createElement("div");
          comentarioDiv.className = "comentario-item";

          const textoP = document.createElement("p");
          textoP.className = "comentario-texto";
          textoP.textContent = comentario.texto;

          const autorP = document.createElement("p");
          autorP.className = "comentario-autor";
          autorP.innerHTML = `<strong>${comentario.nombre}</strong> (${comentario.fecha}):`;

          comentarioDiv.appendChild(autorP);
          comentarioDiv.appendChild(textoP);

          listadoDiv.appendChild(comentarioDiv);
        });
      }
    })
    .catch((error) => {
      console.error("Error al cargar los comentarios:", error);
      mensajeDiv.textContent =
        "Error al cargar los comentarios. Por favor, intente de nuevo más tarde.";
      mensajeDiv.style.color = "red";
    });

  const formComentario = document.getElementById("form-agregar-comentario");
  const erroresDiv = document.getElementById("comentario-errores");

  if (formComentario) {
    formComentario.addEventListener("submit", function (event) {
      event.preventDefault();

      const nombreInput = document.getElementById("nombre-comentario");
      const textoInput = document.getElementById("texto-comentario");
      let errores = [];

      if (nombreInput.value.trim().length < 3) {
        errores.push("El nombre debe tener al menos 3 caracteres.");
      }
      if (nombreInput.value.trim().length > 80) {
        errores.push("El nombre no puede exceder los 80 caracteres.");
      }
      if (textoInput.value.trim().length < 5) {
        errores.push("El comentario debe tener al menos 5 caracteres.");
      }

      if (errores.length > 0) {
        erroresDiv.innerHTML = errores.join("<br>");
        erroresDiv.style.display = "block";
        return;
      }

      erroresDiv.style.display = "none";
      const formData = new FormData(formComentario);

      fetch(`/api/actividad/${actividadId}/comentarios`, {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            erroresDiv.innerHTML = data.error;
            erroresDiv.style.display = "block";
          } else {
            agregarComentarioAlDOM(data);
            formComentario.reset();
          }
        })
        .catch((error) => {
          console.error("Error al enviar el comentario:", error);
          erroresDiv.innerHTML = "Ocurrió un error de red. Inténtalo de nuevo.";
          erroresDiv.style.display = "block";
        });
    });
  }

  function agregarComentarioAlDOM(comentario) {
    const mensajeSinComentarios = document.getElementById(
      "comentarios-mensaje"
    );

    if (mensajeSinComentarios) {
      mensajeSinComentarios.remove();
    }

    const comentarioDiv = document.createElement("div");
    comentarioDiv.className = "comentario-item";

    const autorP = document.createElement("p");
    autorP.className = "comentario-autor";
    autorP.innerHTML = `<strong>${comentario.nombre}</strong> (${comentario.fecha}):`;

    const textoP = document.createElement("p");
    textoP.className = "comentario-texto";
    textoP.textContent = comentario.texto;

    comentarioDiv.appendChild(autorP);
    comentarioDiv.appendChild(textoP);
    listadoDiv.prepend(comentarioDiv);
  }
});
