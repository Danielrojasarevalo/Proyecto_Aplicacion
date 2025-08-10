function actualizarTabla() {
    const tbody = document.getElementById('tabla-cuerpo');
    tbody.innerHTML = '<tr><td colspan="5">Cargando datos...</td></tr>';

    // Obtener el ID de la finca de la URL
    const urlParams = new URLSearchParams(window.location.search);
    const fincaId = urlParams.get('id');

    if (!fincaId) {
        tbody.innerHTML = '<tr><td colspan="5">No se ha seleccionado una finca</td></tr>';
        return;
    }

    // URL simplificada como en el código funcional
    fetch(`/historial_datos_api/?id=${fincaId}`)
      .then(response => {
        if (!response.ok) throw new Error('Error en la respuesta de la API');
        return response.json();
      })
      .then(data => {
        if (!data.length) {
          tbody.innerHTML = '<tr><td colspan="5">No hay datos disponibles.</td></tr>';
          return;
        }

        tbody.innerHTML = ''; // Limpiar la tabla

        data.forEach(registro => {
          let clase = '';
          if (registro.temperatura !== null) {
            if (registro.temperatura <= 40) clase = 'normal';
            else if (registro.temperatura > 40 && registro.temperatura <= 70) clase = 'advertencia';
            else clase = 'peligro';
          }

          const fila = document.createElement('tr');
          if (clase) fila.classList.add(clase);

          fila.innerHTML = `
            <td>${formatDjangoDate(registro.fecha)}</td>
            <td>${registro.humedad !== null ? registro.humedad : '--'}</td>
            <td>${registro.temperatura !== null ? registro.temperatura : '--'}</td>
            <td>${registro.ph !== null ? registro.ph : '--'}</td>
            <td>${registro.arduino || '--'}</td>
          `;

          tbody.appendChild(fila);
        });
      })
      .catch(error => {
        tbody.innerHTML = `<tr><td colspan="5">Error al cargar datos: ${error.message}</td></tr>`;
        console.error('Error al obtener datos:', error);
      });
}

// Función para formatear la fecha de Django a formato legible
function formatDjangoDate(fecha) {
  if (!fecha) return '--';
  // Si ya es string tipo 'YYYY-MM-DD HH:mm:ss', solo mostrar la parte de fecha y hora
  if (typeof fecha === 'string') {
    // Si tiene formato ISO, reemplazar T por espacio y quitar milisegundos
    return fecha.replace('T', ' ').split('.')[0];
  }
  // Si es Date
  if (fecha instanceof Date) {
    return fecha.toLocaleString();
  }
  return fecha;
}

window.onload = () => {
    actualizarTabla();
    setInterval(actualizarTabla, 10000);
};