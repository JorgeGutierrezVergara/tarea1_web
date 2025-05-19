const IMAGEN_POR_DEFECTO =
  "https://www.upack.in/media/catalog/product/cache/1b6285b0519a2e4e16a97e58faf7625a/u/n/universal_kraft_5_4.jpg";

export const actividades = [
  {
    id: 1,
    nombreActividad: "Noche de Película y Debate",
    diaHoraInicio: "2025-05-23T19:00", // Viernes pasado (ejemplo)
    diaHoraTermino: "2025-05-23T22:00",
    region: "Metropolitana de Santiago",
    comuna: "Santiago",
    sector: "Sala multiuso Beauchef, Edificio A, Piso 3",
    nombreOrganizador: "Cine Club FCFM",
    emailOrganizador: "cineclub@ing.uchile.cl",
    celularOrganizador: "+56911223344",
    contactarPor: [
      { tipo: "email", valor: "cineclub@ing.uchile.cl" },
      { tipo: "instagram", valor: "@cineclubfcfm" },
    ],
    temas: ["Cine", "Debate", "Cultural"],
    descripcionOtroTema: "",
    descripcionActividad:
      "Proyección de la película 'El Secreto de sus Ojos' seguida de un debate sobre sus temas principales. ¡Habrá cabritas!",
    fotos: [IMAGEN_POR_DEFECTO], // Array con una o varias fotos
  },
  {
    id: 2,
    nombreActividad: "Clase de Cocina: Pastas Frescas",
    diaHoraInicio: "2025-05-24T11:00", // Sábado
    diaHoraTermino: "2025-05-24T14:00",
    region: "Metropolitana de Santiago",
    comuna: "Providencia",
    sector: "Taller de cocina 'El Buen Gusto', Av. Providencia 123",
    nombreOrganizador: "Chef Sofía Reyes",
    emailOrganizador: "sofia.reyes.chef@example.com",
    celularOrganizador: "+56922334455",
    contactarPor: [
      { tipo: "whatsapp", valor: "+56922334455" },
      { tipo: "otra_contacto", valor: "Formulario en www.elbuengusto.cl" },
    ],
    temas: ["Comida", "Taller", "Manualidades"],
    descripcionOtroTema: "",
    descripcionActividad:
      "Aprende a hacer deliciosas pastas frescas desde cero: tallarines y ravioles. Incluye degustación y copa de vino. Cupos limitados.",
    fotos: [IMAGEN_POR_DEFECTO, IMAGEN_POR_DEFECTO], // Ejemplo con dos "instancias" de la misma foto
  },
  {
    id: 3,
    nombreActividad: "Torneo de Ajedrez Rápido",
    diaHoraInicio: "2025-05-25T15:00", // Domingo
    diaHoraTermino: "2025-05-25T19:00",
    region: "Metropolitana de Santiago",
    comuna: "Ñuñoa",
    sector: "Club de Ajedrez Ñuñoa, Calle Los Aromos 456",
    nombreOrganizador: "Club de Ajedrez Ñuñoa",
    emailOrganizador: "contacto@ajedreznunoa.cl",
    celularOrganizador: "",
    contactarPor: [{ tipo: "telegram", valor: "t.me/ajedreznunoa" }],
    temas: ["Juegos", "Deporte", "Competencia"],
    descripcionOtroTema: "",
    descripcionActividad:
      "Torneo abierto de ajedrez, modalidad rápida (15 min por jugador). Premios para los primeros lugares. Inscripción previa requerida.",
    fotos: [IMAGEN_POR_DEFECTO],
  },
  {
    id: 4,
    nombreActividad: "Senderismo al Cerro Manquehue",
    diaHoraInicio: "2025-05-31T09:00", // Próximo Sábado
    diaHoraTermino: "2025-05-31T15:00",
    region: "Metropolitana de Santiago",
    comuna: "Vitacura",
    sector: "Entrada por Agua del Palo",
    nombreOrganizador: "Grupo Amigos del Trekking",
    emailOrganizador: "amigostrekking@example.com",
    celularOrganizador: "+56933445566",
    contactarPor: [
      { tipo: "whatsapp", valor: "+56933445566" },
      { tipo: "instagram", valor: "@amigostrekking" },
    ],
    temas: ["Deporte", "Aire Libre", "Naturaleza"],
    descripcionOtroTema: "",
    descripcionActividad:
      "Ascenso al Cerro Manquehue para disfrutar de las vistas de Santiago. Dificultad media. Llevar agua, snack, bloqueador solar y gorro. ¡Nos encontramos en la entrada!",
    fotos: [
      IMAGEN_POR_DEFECTO,
      IMAGEN_POR_DEFECTO,
      IMAGEN_POR_DEFECTO,
      IMAGEN_POR_DEFECTO,
      IMAGEN_POR_DEFECTO,
    ],
  },
  {
    id: 5,
    nombreActividad: "Taller de Programación para Principiantes",
    diaHoraInicio: "2025-06-01T10:00", // Próximo Domingo
    diaHoraTermino: "", // Sin hora de término especificada
    region: "Metropolitana de Santiago",
    comuna: "Santiago",
    sector: "Online vía Zoom (link se envía al inscribir)",
    nombreOrganizador: "Comunidad Dev Learning",
    emailOrganizador: "info@devlearning.org",
    celularOrganizador: "",
    contactarPor: [
      { tipo: "email", valor: "info@devlearning.org" },
      { tipo: "x", valor: "@DevLearningOrg" },
      { tipo: "tiktok", valor: "@devlearningclips" },
    ],
    temas: ["Tecnología", "Educación", "Otro Tema"],
    descripcionOtroTema: "Desarrollo Web", // Descripción para "Otro Tema"
    descripcionActividad:
      "Aprende los fundamentos de la programación con Python en este taller introductorio. No se necesita experiencia previa. Ideal para quienes quieren iniciarse en el mundo del desarrollo.",
    fotos: [IMAGEN_POR_DEFECTO],
  },
];
