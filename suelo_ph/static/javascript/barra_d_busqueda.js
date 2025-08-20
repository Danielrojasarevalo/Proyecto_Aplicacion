document.addEventListener("DOMContentLoaded", function () {
    const inputBusqueda = document.getElementById("inputBusqueda");
    const searchButton = document.querySelector("#search-icon button");
    const modal = document.getElementById("modalResultados");
    const cerrarModal = document.querySelector(".cerrar-modal");

    const humedadTd = document.getElementById("humedad-modal");
    const temperaturaTd = document.getElementById("temperatura-modal");
    const phTd = document.getElementById("ph-modal");
    const tablaCuerpo = document.getElementById("tabla-cuerpo");

    searchButton.addEventListener("click", function () {
        const fecha = inputBusqueda.value; // Ejemplo: "2025-08-17"
        const fincaId = new URLSearchParams(window.location.search).get("id");

        if (!fecha || !fincaId) {
            alert("Por favor ingresa una fecha válida.");
            return;
        }

        const url = `/index/login/buscar_fecha/?fecha=${fecha}&finca_id=${fincaId}&_=${Date.now()}`;
        console.log("Buscando con URL:", url);

        fetch(url, {
            credentials: 'include'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log("Datos recibidos:", data);

            // Limpiar tabla
            tablaCuerpo.innerHTML = "";

            if (data.resultados && data.resultados.length > 0) {

                // Mostrar el primer resultado en el modal (opcional)
                const r = data.resultados[0];
                humedadTd.textContent = r.humedad + " %";
                temperaturaTd.textContent = r.temperatura + " °C";
                phTd.textContent = r.ph;
                modal.style.display = "block";

                // Rellenar la tabla con todos los resultados
                data.resultados.forEach(item => {
                    const fila = document.createElement("tr");

                    const fechaCell = document.createElement("td");
                    fechaCell.textContent = new Date(item.fecha).toLocaleString(); // incluye hora

                    const humedadCell = document.createElement("td");
                    humedadCell.textContent = item.humedad + " %";

                    const tempCell = document.createElement("td");
                    tempCell.textContent = item.temperatura + " °C";

                    const phCell = document.createElement("td");
                    phCell.textContent = item.ph;

                    const dispositivoCell = document.createElement("td");
                    dispositivoCell.textContent = item.arduino__nombre || "Desconocido";

                    fila.appendChild(fechaCell);
                    fila.appendChild(humedadCell);
                    fila.appendChild(tempCell);
                    fila.appendChild(phCell);
                    fila.appendChild(dispositivoCell);

                    tablaCuerpo.appendChild(fila);
                });

            } else {
                tablaCuerpo.innerHTML = "<tr><td colspan='5'>No se encontraron datos para esa fecha.</td></tr>";
            }
        })
        .catch(error => {
            console.error("Error en la búsqueda:", error);
            alert("Error en la búsqueda. Revisa la consola para más detalles.");
        });
    });

    cerrarModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});

 

