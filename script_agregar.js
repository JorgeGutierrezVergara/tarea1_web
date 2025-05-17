import { region_comuna } from "./region_comuna.js";

// elementos para la confirmación del formulario:
const modalConfirmacionSubmit = document.getElementById(
  "modal_confirmacion_submit"
);
const btnConfirmarSiSubmit = document.getElementById("btn_confirmar_si_submit");
const btnConfirmarNoSubmit = document.getElementById("btn_confirmar_no_submit");
const mensajeExitoFinal = document.getElementById("mensaje_exito_final");
const botonAgregarActividad = document.getElementById("add");

const configContactos = [
  { chkId: "contactar_chk_whatsapp", inputId: "contactar_valor_whatsapp" },
  { chkId: "contactar_chk_telegram", inputId: "contactar_valor_telegram" },
  { chkId: "contactar_chk_x", inputId: "contactar_valor_x" },
  { chkId: "contactar_chk_instagram", inputId: "contactar_valor_instagram" },
  { chkId: "contactar_chk_tiktok", inputId: "contactar_valor_tiktok" },
  { chkId: "contactar_opcion_otra_checkbox", inputId: "otra_contacto_text" },
];

configContactos.forEach((config) => {
  const checkbox = document.getElementById(config.chkId);
  const textInput = document.getElementById(config.inputId);

  checkbox.addEventListener("change", function () {
    if (this.checked) {
      textInput.style.display = "inline-block";
      textInput.required = true;
    } else {
      textInput.style.display = "none";
      textInput.value = "";
      textInput.required = false;
    }
  });
});

const poblarRegiones = () => {
  let region_select = document.getElementById("region");
  let regiones = region_comuna.regiones;
  for (const region of regiones) {
    let option = document.createElement("option");
    option.value = region.nombre;
    option.text = region.nombre;
    region_select.appendChild(option);
  }
};

const poblarComunas = () => {
  let comuna_select = document.getElementById("comuna");
  comuna_select.innerHTML = '<option value="">Seleccione comuna</option>';
  let region_value = document.getElementById("region").value;
  const comunas = region_comuna.regiones.find(
    (reg) => reg.nombre === region_value
  );
  for (const comuna of comunas.comunas) {
    let option = document.createElement("option");
    option.value = comuna.nombre;
    option.text = comuna.nombre;
    comuna_select.appendChild(option);
  }
};

const defaultTime = (date) => {
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const day = date.getDate().toString().padStart(2, "0");
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");
  return `${year}-${month}-${day}T${hours}:${minutes}`;
};

const prellenarFechas = () => {
  const inputInicio = document.getElementById("inicio");
  const inputFinal = document.getElementById("final");

  if (inputInicio && inputFinal) {
    const ahora = new Date();
    inputInicio.value = defaultTime(ahora);
    const tresHorasDespues = new Date(ahora.getTime());
    inputFinal.value = defaultTime(tresHorasDespues);
  } else {
    console.error("No se encontraron los inputs de fecha #inicio o #final.");
  }
};

document.getElementById("region").addEventListener("change", poblarComunas);

window.onload = () => {
  poblarRegiones();
  prellenarFechas();
};

// Lógica para mostrar/ocultar el campo de texto del Tema "Otro"
const temaOtroCheckbox = document.getElementById("tema_opcion_otro_checkbox");
const temaOtroTexto = document.getElementById("otra_tema_text");

if (temaOtroCheckbox && temaOtroTexto) {
  temaOtroCheckbox.addEventListener("change", function () {
    if (this.checked) {
      temaOtroTexto.style.display = "inline-block";
      temaOtroTexto.required = true;
    } else {
      temaOtroTexto.style.display = "none";
      temaOtroTexto.value = "";
      temaOtroTexto.required = false;
    }
  });
}

// Lógica para mostrar/ocultar el campo de texto del Contacto "Otro"
const contactoOtroCheckbox = document.getElementById(
  "contactar_opcion_otra_checkbox"
);
const contactoOtroTexto = document.getElementById("otra_contacto_text");

if (contactoOtroCheckbox && contactoOtroTexto) {
  contactoOtroCheckbox.addEventListener("change", function () {
    if (this.checked) {
      contactoOtroTexto.style.display = "inline-block";
      contactoOtroTexto.required = true;
    } else {
      contactoOtroTexto.style.display = "none";
      contactoOtroTexto.value = "";
      contactoOtroTexto.required = false;
    }
  });
}

// --- Lógica para agregar múltiples fotos ---
const MAX_FOTOS = 5;
let contadorFotosActuales = 1;

const btnAgregarFoto = document.getElementById("btn_agregar_foto");
const contenedorFotos = document.getElementById("contenedor_fotos");

btnAgregarFoto.addEventListener("click", function () {
  if (contadorFotosActuales < MAX_FOTOS) {
    contadorFotosActuales++;

    const nuevoInputFoto = document.createElement("input");
    nuevoInputFoto.type = "file";
    nuevoInputFoto.name = "fotos_actividad[]";
    nuevoInputFoto.accept = "image/*";

    contenedorFotos.appendChild(nuevoInputFoto);

    // Si alcanzamos el máximo, deshabilitamos el botón
    if (contadorFotosActuales === MAX_FOTOS) {
      this.disabled = true;
      console.log(
        "Máximo de " +
          MAX_FOTOS +
          " campos de foto alcanzado, botón deshabilitado."
      );
    }
  }
});

// verificaciones

const validateRegion = (region_buscada) => {
  let regiones = [];
  region_comuna.regiones.forEach((el) => regiones.push(el.nombre));
  if (regiones.includes(region_buscada)) {
    return true;
  } else {
    return false;
  }
};

const validateComuna = (region, comuna) => {
  if (!region) return false;
  const datosregion = region_comuna.regiones.find(
    (reg) => reg.nombre === region
  );
  let comunas = [];
  datosregion.comunas.forEach((element) => {
    comunas.push(element.nombre);
  });
  if (comunas.includes(comuna)) {
    return true;
  } else {
    return false;
  }
};

const validateName = (name) => {
  if (!name) return false;
  let lengthvalid = name.trim().length >= 4;
  return lengthvalid;
};

const validateEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};

const validateNumber = (number) => {
  const regex = /^\+\d{3}\.\d{8}$/;
  return regex.test(number);
};

const validateDate = (inicio, final) => {
  const fechaInicio = new Date(inicio); // se le suma un poco de tiempo para que no quede mal por defecto
  const fechaFinal = new Date(final);
  const ahoraMismo = new Date();

  if (fechaFinal <= fechaInicio) {
    return false;
  }
  if (fechaInicio < ahoraMismo) {
    console.log("ahora: " + ahoraMismo);
    console.log("inicio: " + fechaInicio);
    return false;
  }

  return true;
};

const validateTema = (fieldsetElement) => {
  const temaCheckboxes = fieldsetElement.querySelectorAll(
    'input[name="tema_opcion"]:checked'
  );
  const temaOtroCheckbox = fieldsetElement.querySelector(
    "#tema_opcion_otro_checkbox"
  );
  const temaOtroTextoInput = fieldsetElement.querySelector("#otra_tema_text");

  let alMenosUnTemaSeleccionado = temaCheckboxes.length > 0;

  if (temaOtroCheckbox && temaOtroCheckbox.checked) {
    alMenosUnTemaSeleccionado = true;

    if (temaOtroTextoInput) {
      const textoOtro = temaOtroTextoInput.value.trim();
      if (textoOtro.length < 3 || textoOtro.length > 15) {
        return false;
      }
    } else {
      return false;
    }
  }

  if (!alMenosUnTemaSeleccionado) {
    return false;
  }

  return true;
};

const validateContacto = (fieldsetElement) => {
  const contactarCheckboxesNormales = fieldsetElement.querySelectorAll(
    'input[name="contactar_opcion"]:checked'
  );

  const contactoOtroCheckbox = fieldsetElement.querySelector(
    "#contactar_opcion_otra_checkbox"
  );
  const contactoOtroTextoInput = fieldsetElement.querySelector(
    "#otra_contacto_text"
  );

  let totalSeleccionados = contactarCheckboxesNormales.length;

  if (contactoOtroCheckbox && contactoOtroCheckbox.checked) {
    totalSeleccionados++;
    if (contactoOtroTextoInput) {
      const textoOtro = contactoOtroTextoInput.value.trim();
      if (textoOtro.length < 4 || textoOtro.length > 50) {
        return false;
      }
    } else {
      return false;
    }
  }
  if (totalSeleccionados > 5) {
    return false;
  }
  return true;
};

const validateFotos = (fotos) => {
  let archivosSeleccionados = 0;
  const inputsDeFoto = fotos.querySelectorAll(
    'input[name="fotos_actividad[]"]'
  );
  console.log(inputsDeFoto);

  inputsDeFoto.forEach((input) => {
    if (input.files && input.files.length > 0) {
      archivosSeleccionados++;
    }
  });

  if (archivosSeleccionados < 1) {
    return false;
  }

  if (archivosSeleccionados > MAX_FOTOS) {
    return false;
  }

  return { isValid: true };
};

const validar = () => {
  const region = document.getElementById("region");
  const comuna = document.getElementById("comuna");
  const nombre = document.getElementById("nombre");
  const email = document.getElementById("email");
  const numero = document.getElementById("telefono");
  const contact = document.getElementById("fieldset_contacto");
  const inicio = document.getElementById("inicio");
  const final = document.getElementById("final");
  const tema = document.getElementById("fieldset_tema");
  const fotos = document.getElementById("contenedor_fotos");
  const errores = document.getElementById("errores");
  const errores_lista = document.getElementById("errores_lista");
  const exito = document.getElementById("exito");

  errores_lista.innerHTML = "";
  errores_lista.style.marginTop = "25px";

  let msg = [];

  if (!validateRegion(region.value)) {
    msg.push("region no valida \n");
    region.style.borderColor = "red";
  } else {
    region.style.borderColor = "";
  }
  if (!validateComuna(region.value, comuna.value)) {
    msg.push("comuna no valida \n");
    comuna.style.borderColor = "red";
  } else {
    comuna.style.borderColor = "";
  }
  if (!validateName(nombre.value)) {
    msg.push("nombre no valido \n");
    nombre.style.borderColor = "red";
  } else {
    nombre.style.borderColor = "";
  }
  if (!validateEmail(email.value)) {
    msg.push("mail no valido \n");
    email.style.borderColor = "red";
  } else {
    email.style.borderColor = "";
  }
  if (!validateNumber(numero.value)) {
    msg.push("numero no valido \n");
    numero.style.borderColor = "red";
  } else {
    numero.style.borderColor = "";
  }
  if (!validateTema(tema)) {
    msg.push("debes seleccionar un tema y/o hay error en el formato" + "\n");
    tema.style.border = "2px solid red";
  } else {
    tema.style.border = "";
  }
  if (!validateContacto(contact)) {
    msg.push("contacto no valido \n");
    contact.style.borderColor = "red";
  } else {
    contact.style.borderColor = "";
  }
  if (!validateDate(inicio.value, final.value)) {
    msg.push("fechas no válidas \n");
    inicio.style.borderColor = "red";
    final.style.borderColor = "red";
  } else {
    inicio.style.borderColor = "";
    final.style.borderColor = "";
  }
  if (!validateFotos(fotos)) {
    msg.push("Debes seleccionar entre 1 y " + MAX_FOTOS + " fotos.");
    fotos.style.borderWidth = "2px";
    fotos.style.borderStyle = "solid";
    fotos.style.borderColor = "red";
  } else {
    fotos.style.borderWidth = "";
    fotos.style.borderStyle = "";
    fotos.style.borderColor = "";
  }

  if (msg.length > 0) {
    console.log(msg);
    errores.style.display = "block";
    errores_lista.style.display = "block";
    msg.forEach((item) => {
      const elementoLista = document.createElement("li");
      elementoLista.textContent = item;
      errores_lista.appendChild(elementoLista);
    });
    return false;
  } else {
    errores.style.display = "none";
    errores_lista.style.display = "none";
    msg = "";
    console.log("no hay errores");
    return true;
  }
};

botonAgregarActividad.addEventListener("click", function (event) {
  event.preventDefault();

  const esValido = validar();

  if (esValido) {
    modalConfirmacionSubmit.style.display = "flex";
  }
});

btnConfirmarSiSubmit.addEventListener("click", function () {
  modalConfirmacionSubmit.style.display = "none";
  document.getElementById("errores").style.display = "none";
  document.getElementById("errores_lista").innerHTML = "";

  mensajeExitoFinal.style.display = "flex";
});

btnConfirmarNoSubmit.addEventListener("click", function () {
  modalConfirmacionSubmit.style.display = "none";
});

document.getElementById("add").addEventListener("click", (e) => {
  e.preventDefault();
  validar();
});
