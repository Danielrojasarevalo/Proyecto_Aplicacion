let fincas = [];
let fincaSeleccionadaIndex = null;

function cargarFincas(dataFincas) {
  fincas = dataFincas; 
  const lista = document.getElementById('lista-fincas');
  lista.innerHTML = '';

  if (fincas.length === 0) {
    const li = document.createElement('li');
    li.textContent = 'No tienes fincas registradas';
    lista.appendChild(li);
  } else {
    fincas.forEach((finca, index) => {
      const li = document.createElement('li');
      li.textContent = `${finca.nombre} - ${finca.ubicacion}`;
      li.setAttribute('data-id', finca.id);
      li.tabIndex = 0;
      li.onclick = () => seleccionarFinca(index);
      lista.appendChild(li);
    });
  }
}

function seleccionarFinca(index) {
  fincaSeleccionadaIndex = index;
  const items = document.querySelectorAll('#lista-fincas li');
  items.forEach((li, i) => li.classList.toggle('selected', i === index));
}

function showModal(modal) {
  if (!modal) {
    console.warn('showModal: modal es null');
    return;
  }
  modal.classList.add('show');
  const overlay = document.getElementById('modal-overlay');
  if (overlay) overlay.classList.add('show');
}

function hideModal() {
  const modales = [document.getElementById('login-modal'), document.getElementById('crear-finca-modal')];
  modales.forEach(modal => {
    if (modal) modal.classList.remove('show');
  });
  const overlay = document.getElementById('modal-overlay');
  if (overlay) overlay.classList.remove('show');
}

function modificarFinca() {
  if (fincaSeleccionadaIndex === null) {
    alert('Por favor selecciona una finca.');
    return;
  }
  const fincaId = fincas[fincaSeleccionadaIndex].id;
  window.location.href = `/index/login/login/datos?id=${fincaId}`;
}

document.addEventListener('DOMContentLoaded', () => {
  const abrir_modal_fincas = abrir_modal_fincas_str === 'True' || abrir_modal_fincas_str === 'true';

  if (abrir_modal_fincas) {
  fetch('/index/login/api/fincas/', { credentials: 'include' })
  .then(res => res.json())
  .then(data => {
    console.log('Datos fincas recibidos:', data);
    cargarFincas(data.fincas);
    showModal(document.getElementById('login-modal'));
  })
  .catch(console.error);
  }
});

function showFormularioFincaModal() {
  const crearModal = document.getElementById('crear-finca-modal');
  if (crearModal) {
    showModal(crearModal);
  } else {
    console.warn('showFormularioFincaModal: no se encontró el modal crear-finca-modal');
  }
}
// Función para ocultar la contraseña en el campo de entrada
document.addEventListener('DOMContentLoaded', () => {
  const passwordInput = document.getElementById('password');
  const togglePassword = document.getElementById('togglePassword');

  let realValue = '';
  let timeout = null;
  let isVisible = false;

  passwordInput.addEventListener('input', (e) => {
    const typed = e.target.value;

    // Caso: agregando una letra nueva
    if (typed.length > realValue.length) {
      const newChar = typed.slice(-1);
      realValue += newChar;

      // Mostrar todo como • menos la última letra real
      passwordInput.type = 'text';
      passwordInput.value = '•'.repeat(realValue.length - 1) + newChar;

      clearTimeout(timeout);
      timeout = setTimeout(() => {
        if (!isVisible) {
          passwordInput.type = 'password';
          passwordInput.value = '•'.repeat(realValue.length);
        }
      }, 500);
    }

    // Caso: borrando
    else if (typed.length < realValue.length) {
      realValue = realValue.slice(0, typed.length);
      passwordInput.type = 'text';
      passwordInput.value = '•'.repeat(realValue.length);

      clearTimeout(timeout);
      timeout = setTimeout(() => {
        if (!isVisible) {
          passwordInput.type = 'password';
        }
      }, 0);
    }
  });

  togglePassword.addEventListener('click', () => {
    isVisible = !isVisible;

    if (isVisible) {
      passwordInput.type = 'text';
      passwordInput.value = realValue;
      togglePassword.textContent = '🙈';
    } else {
      passwordInput.type = 'password';
      passwordInput.value = '•'.repeat(realValue.length);
      togglePassword.textContent = '🙉';
    }
  });

  // Al enviar el formulario, poner la contraseña real
  const form = passwordInput.closest('form');
  if (form) {
    form.addEventListener('submit', () => {
      passwordInput.value = realValue;
      passwordInput.type = 'password';
    });
  }
});

// Oculta todo hasta que se cargue bien
document.documentElement.classList.add('loading');

// Mostrar página al cargar completamente
window.addEventListener('load', () => {
  document.documentElement.classList.remove('loading');
  document.body.style.opacity = '1';
});

// Transición de salida al cambiar de enlace
document.addEventListener('DOMContentLoaded', () => {
  const contenedor = document.querySelector('.contenedor') || document.body;

  document.querySelectorAll('.opciones a').forEach((enlace) => {
    enlace.addEventListener('click', (e) => {
      e.preventDefault();

      const destino = enlace.getAttribute('href');
      contenedor.classList.add('fade-out');

      setTimeout(() => {
        window.location.href = destino;
      }, 500); // Tiempo del fade-out
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const formCrearFinca = document.getElementById('crearFincaForm');

  if (formCrearFinca) {
    formCrearFinca.addEventListener('submit', function (e) {
      e.preventDefault(); // Evita recargar la página

      const nombre = document.getElementById('nombre_finca_input').value.trim();
      const ubicacion = document.getElementById('ubicacion_finca').value.trim();
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      if (!nombre || !ubicacion) {
        alert('Por favor completa todos los campos.');
        return;
      }

      fetch('/index/login/crear_finca_ajax/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken
        },
        body: new FormData(formCrearFinca),
        credentials: 'include'
      })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          alert(data.error);
        } else {
          alert('Finca creada con éxito');
          fetch('/index/login/api/fincas/', { credentials: 'include' })
            .then(r => r.json())
            .then(d => {
              cargarFincas(d.fincas);
              if (d.fincas && d.fincas.length > 0) {
                seleccionarFinca(d.fincas.length - 1);
              }
            });
          hideModal();
          formCrearFinca.reset();
        }
      })
      .catch(err => {
        alert('Error al crear finca.');
        console.error('Error al crear finca:', err);
      });
    });
  }
});





// Exportar funciones si usas eventos inline
// window.hideModal = hideModal;
// window.showFormularioFincaModal = showFormularioFincaModal;
// window.modificarFinca = modificarFinca;
