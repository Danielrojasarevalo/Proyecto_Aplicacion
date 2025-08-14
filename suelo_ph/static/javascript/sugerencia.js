document.addEventListener('DOMContentLoaded', function() {
    let temporadaSeleccionada = null;
    const opcionesTemporada = document.querySelectorAll('.opcion-temporada');
    const buscarBtn = document.getElementById('buscar-btn');
    const fechaDesdeInput = document.getElementById('fechaDesde');
    const fechaHastaInput = document.getElementById('fechaHasta');
    const errorMessageDiv = document.createElement('div');
    errorMessageDiv.id = 'error-message';
    errorMessageDiv.style.cssText = 'color: red; background-color: #ffe6e6; padding: 10px; border: 1px solid red; text-align: center; margin: 10px; display: none;';
    
    // Obtener el token CSRF para las peticiones POST
    const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
    
    const mainContentWrapper = document.querySelector('.main-content-wrapper');
    if (mainContentWrapper) {
        mainContentWrapper.parentNode.insertBefore(errorMessageDiv, mainContentWrapper);
    }

    opcionesTemporada.forEach(btn => {
        btn.addEventListener('click', function() {
            opcionesTemporada.forEach(b => b.classList.remove('selected', 'activo'));
            btn.classList.add('selected', 'activo');
            temporadaSeleccionada = btn.getAttribute('data-temporada');
        });
    });

    buscarBtn.addEventListener('click', async function(e) {
        e.preventDefault();
        const fechaDesde = fechaDesdeInput.value;
        const fechaHasta = fechaHastaInput.value;

        errorMessageDiv.style.display = 'none';

        // Validaciones del lado del cliente antes de enviar
        if (!temporadaSeleccionada) {
            errorMessageDiv.textContent = 'Por favor, escoja una temporada.';
            errorMessageDiv.style.display = 'block';
            return;
        }
        if (!fechaDesde || !fechaHasta) {
            errorMessageDiv.textContent = 'Por favor, seleccione las fechas de inicio y fin.';
            errorMessageDiv.style.display = 'block';
            return;
        }

        const fincaId = new URLSearchParams(window.location.search).get('id');
        const data = {
            fecha_desde: fechaDesde,
            fecha_hasta: fechaHasta,
            tipo_abono_nombre: temporadaSeleccionada,
            finca_id: fincaId
        };

        try {
            // Usa el endpoint correcto según el include de Django
            const response = await fetch('/index/login/resultados_json/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken 
                },
                body: JSON.stringify(data)
            });
            const responseData = await response.json();

            if (responseData.status === 'ok') {
                // Redirige a la URL correcta con todos los parámetros necesarios
                window.location.href = `/index/login/resultados/?fecha_desde=${fechaDesde}&fecha_hasta=${fechaHasta}&temporada=${temporadaSeleccionada}&finca_id=${fincaId}`;
            } else {
                errorMessageDiv.textContent = responseData.message;
                errorMessageDiv.style.display = 'block';
            }
        } catch (error) {
            console.error('Error en la comunicación:', error);
            errorMessageDiv.textContent = 'Ocurrió un error en la comunicación con el servidor. Por favor, inténtelo de nuevo.';
            errorMessageDiv.style.display = 'block';
        }
    });
});