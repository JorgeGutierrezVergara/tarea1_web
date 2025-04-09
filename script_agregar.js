import { region_comuna } from "./region_comuna.js";
//import { DateTime } from "luxon";
// seleccion region y comuna
const poblarRegiones = () => {
  let region_select = document.getElementById("select-region");
  let regiones = region_comuna.regiones;
  for (const region of regiones) {
    let option = document.createElement("option");
    option.value = region.nombre;
    option.text = region.nombre;
    region_select.appendChild(option);
  }
};

const poblarComunas = () => {
  let comuna_select = document.getElementById("select-comuna");
  comuna_select.innerHTML = '<option value="">Seleccione comuna</option>';
  let region_value = document.getElementById("select-region").value;
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

document
  .getElementById("select-region")
  .addEventListener("change", poblarComunas);

window.onload = () => {
  poblarRegiones();
};

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

const validateContact = (contact) => {
  if (!contact) return true;
  const contactos = ["whatssapp", "telegram", "x", "tiktok", "otra"];
  return contactos.includes(contact);
};

// const validateInitialDate = (date) => {
//   const regex = /^(\d{2})-(\d{2})-(\d{4}) (\d{2}):(\d{2})$/;
//   return regex.test(date);
// };

// const validateEndDate = (inicio, final) => {
//   const fechaInicial = DateTime.fromFormat(inicio, "dd-MM-yyyy HH:mm");
//   const fechaFinal = DateTime.fromFormat(final, "dd-MM-yyyy HH:mm");
//   return fechaFinal > fechaInicial;
// };

const validateTema = (tema) => {
  if (!tema) return false;
  const temas = [
    "musica",
    "deporte",
    "ciencias",
    "religion",
    "política",
    "tecnología",
    "juegos",
    "baile",
    "comida",
    "otro",
  ];
  return temas.includes(tema);
}; //mostrar input si se elige "otro"

// const validateFoto = (foto) => {
//   if (!foto || !foto.files) {
//     return false;
//   }
//   const extensiones = ["jpg", "jpeg", "png", "gif", "webp"];
//   const extension = foto.value.name.split(".").pop().toLowerCase();
//   return extensiones.includes(extension);
// };

const validar = () => {
  const region = document.getElementById("select-region");
  const comuna = document.getElementById("select-comuna");
  const nombre = document.getElementById("nombre");
  const email = document.getElementById("email");
  const numero = document.getElementById("telefono");
  const contact = document.getElementById("select-contacto");
  const inicio = document.getElementById("inicio");
  const final = document.getElementById("final");
  const tema = document.getElementById("select-tema");
  const foto = document.getElementById("img");
  const errores = document.getElementById("errores");
  const errores_lista = document.getElementById("errores_lista");
  const exito = document.getElementById("exito");

  exito.innerHTML = "";
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
  if (!validateTema(tema.value)) {
    msg.push("tema no valido \n");
    tema.style.borderColor = "red";
  } else {
    tema.style.borderColor = "";
  }
  if (!validateContact(contact.value)) {
    msg.push("contacto no valido \n");
    contact.style.borderColor = "red";
  } else {
    contact.style.borderColor = "";
  }
  // if (!validateInitialDate(inicio.value)) {
  //   msg.push("fecha inicial no valida");
  // }
  // if (!validateEndDate(inicio, final.value)) {
  //   msg.push("fecha final no valida");
  // }
  // if (!validateFoto(foto.value)) {
  //   msg.push("foto no valida");
  //   foto.style.borderColor = "red";
  // } else {
  //   foto.style.borderColor = "";
  // }

  if (msg.length > 0) {
    console.log(msg);
    errores.style.display = "block";
    errores_lista.style.display = "block";
    exito.style.display = "none";
    msg.forEach((item) => {
      const elementoLista = document.createElement("li");
      elementoLista.textContent = item;
      errores_lista.appendChild(elementoLista);
    });
  } else {
    errores.style.display = "none";
    errores_lista.style.display = "none";
    exito.style.display = "block";
    exito.textContent = "Exito!";
    msg = "";
    console.log("no hay errores");
  }
};
document.getElementById("add").addEventListener("click", (e) => {
  e.preventDefault();
  validar();
});
