document.addEventListener("DOMContentLoaded", function () {
  async function obtenerDatosActividadesPorDia() {
    const url = "/api/estadisticas/actividades_por_dia";
    try {
      const respuesta = await fetch(url);
      if (!respuesta.ok) {
        throw new Error(`Error al contactar la API: ${respuesta.status}`);
      }
      const datos = await respuesta.json();
      return datos;
    } catch (error) {
      console.error("Error al obtener los datos de actividades:", error);
      return [];
    }
  }

  async function crearGraficoActividades() {
    try {
      const datosActividades = await obtenerDatosActividadesPorDia();

      Highcharts.chart("container-grafico-lineas", {
        chart: {
          type: "line",
        },
        title: {
          text: "Cantidad de Actividades por Día",
        },
        xAxis: {
          type: "datetime",
          title: {
            text: "Fecha",
          },
        },
        yAxis: {
          title: {
            text: "Cantidad de Actividades",
          },
          min: 0,
        },
        tooltip: {
          xDateFormat: "%d/%m/%Y",
          pointFormat: "{series.name}: <b>{point.y}</b>",
        },
        series: [
          {
            name: "Actividades",
            data: datosActividades,
            color: "#5499C7",
          },
        ],
        legend: {
          enabled: true,
        },
        credits: {
          enabled: false,
        },
        responsive: {
          rules: [
            {
              condition: {
                maxWidth: 500,
              },
              chartOptions: {
                legend: {
                  layout: "horizontal",
                  align: "center",
                  verticalAlign: "bottom",
                },
              },
            },
          ],
        },
      });
    } catch (error) {
      console.error("Error al crear el gráfico:", error);
      document.getElementById("container-grafico-lineas").innerHTML =
        '<p style="color:red;">No se pudieron cargar los datos para el gráfico.</p>';
    }
  }
  crearGraficoActividades();

  async function obtenerDatosActividadesPorTema() {
    const url = "/api/estadisticas/actividades_por_tipo";
    try {
      const respuesta = await fetch(url);
      if (!respuesta.ok) {
        throw new Error(
          `Error al contactar la API de temas: ${respuesta.status}`
        );
      }
      const datos = await respuesta.json();
      return datos;
    } catch (error) {
      console.error("Error al obtener los datos de temas:", error);
      return [];
    }
  }

  async function crearGraficoActividadesPorTema() {
    try {
      const datosTemas = await obtenerDatosActividadesPorTema();

      Highcharts.chart("container-grafico-torta", {
        chart: {
          type: "pie",
        },
        title: {
          text: "Actividades por Tema",
        },
        tooltip: {
          pointFormat:
            "{series.name}: <b>{point.percentage:.1f}%</b><br>Cantidad: {point.y}",
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: "pointer",
            dataLabels: {
              enabled: true,
              format: "<b>{point.name}</b>: {point.percentage:.1f} %",
            },
            showInLegend: true,
          },
        },
        series: [
          {
            name: "Temas",
            colorByPoint: true,
            data: datosTemas,
          },
        ],
        credits: {
          enabled: false,
        },
      });
    } catch (error) {
      console.error("Error al crear el gráfico de torta:", error);
      document.getElementById("container-grafico-torta").innerHTML =
        '<p style="color:red;">No se pudieron cargar los datos para el gráfico de torta.</p>';
    }
  }

  crearGraficoActividadesPorTema();

  async function obtenerDatosActividadesPorMesYPeriodo() {
    const url = "/api/estadisticas/actividades_por_mes_y_periodo";
    try {
      const respuesta = await fetch(url);
      if (!respuesta.ok) {
        throw new Error(
          `Error al contactar la API de barras: ${respuesta.status}`
        );
      }
      const datos = await respuesta.json();
      return datos;
    } catch (error) {
      console.error(
        "Error al obtener los datos para el gráfico de barras:",
        error
      );
      return { categories: [], series: [] };
    }
  }

  async function crearGraficoActividadesPorMesYPeriodo() {
    try {
      const datosBarras = await obtenerDatosActividadesPorMesYPeriodo();

      Highcharts.chart("container-grafico-barras", {
        chart: {
          type: "column",
        },
        title: {
          text: "Actividades por Mes y Periodo del Día",
        },
        xAxis: {
          categories: datosBarras.categories,
          title: {
            text: "Mes",
          },
          crosshair: true,
        },
        yAxis: {
          min: 0,
          title: {
            text: "Cantidad de Actividades",
          },
          allowDecimals: false,
        },
        tooltip: {
          headerFormat:
            '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b></td></tr>',
          footerFormat: "</table>",
          shared: true,
          useHTML: true,
        },
        plotOptions: {
          column: {
            pointPadding: 0.2,
            borderWidth: 0,
            dataLabels: {
              enabled: true,
            },
          },
        },
        series: datosBarras.series,
        credits: {
          enabled: false,
        },
      });
    } catch (error) {
      console.error("Error al crear el gráfico de barras:", error);
      document.getElementById("container-grafico-barras").innerHTML =
        '<p style="color:red;">No se pudieron cargar los datos para el gráfico de barras.</p>';
    }
  }

  crearGraficoActividadesPorMesYPeriodo();
});
