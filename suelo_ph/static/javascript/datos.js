function actualizarTabla() {
    const tbody = document.getElementById('tabla-cuerpo');
    tbody.innerHTML = '<tr><td colspan="4">Cargando datos...</td></tr>';

    fetch(urlDatosApi)
      .then(response => {
        if (!response.ok) throw new Error('Error en la respuesta de la API');
        return response.json();
      })
      .then(data => {
        if (!data.length) {
          tbody.innerHTML = '<tr><td colspan="4">No hay datos disponibles.</td></tr>';
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
            <td>${registro.fecha || '--'}</td>
            <td>${registro.humedad !== null ? registro.humedad : '--'}</td>
            <td>${registro.temperatura !== null ? registro.temperatura : '--'}</td>
            <td>${registro.ph !== null ? registro.ph : '--'}</td>
          `;

          tbody.appendChild(fila);
        });
      })
      .catch(error => {
        tbody.innerHTML = `<tr><td colspan="4">Error al cargar datos: ${error.message}</td></tr>`;
        console.error('Error al obtener datos:', error);
      });
}

// Ejecutar al cargar la página y actualizar cada 10 segundos
window.onload = () => {
    actualizarTabla();
    setInterval(actualizarTabla, 10000);
};
