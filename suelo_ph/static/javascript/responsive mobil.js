document.querySelector(".hamburger").addEventListener("click", function () {
    const menu = document.getElementById("mobileMenu");
    menu.style.display = (menu.style.display === "flex") ? "none" : "flex";
});


    document.addEventListener('DOMContentLoaded', function() {
  const acordeonHeaders = document.querySelectorAll('.acordeon-header');
  acordeonHeaders.forEach(header => {
    header.addEventListener('click', () => {
      const content = header.nextElementSibling;   
      header.classList.toggle('active');          
      content.classList.toggle('active');          
    });
  });
});


(function(){
  // ---- Referencias básicas
  const modal    = document.getElementById('modalTemporadas');
  if (!modal) return; // por si la sección no está en esta página

  const abrirBtn = document.getElementById('btnAbrirTemporadas');
  const cerrarEls= modal.querySelectorAll('[data-close]');
  const pista    = modal.querySelector('.carrusel-pista');
  const diapos   = Array.from(modal.querySelectorAll('.carrusel-diapo'));
  const btnPrev  = modal.querySelector('.carrusel-control.anterior');
  const btnNext  = modal.querySelector('.carrusel-control.siguiente');
  const puntos   = modal.querySelector('.carrusel-puntos');

  let indice = 0;

  // ---- Abrir / Cerrar modal
  const abrir  = () => { modal.classList.add('is-open'); document.body.style.overflow = 'hidden'; actualizar(); };
  const cerrar = () => { modal.classList.remove('is-open'); document.body.style.overflow = ''; };

  abrirBtn && abrirBtn.addEventListener('click', abrir);
  cerrarEls.forEach(el => el.addEventListener('click', cerrar));
  modal.addEventListener('click', e => {
    if (e.target.classList.contains('modal-overlay')) cerrar();
  });

  // ---- Teclado dentro del modal
  document.addEventListener('keydown', e => {
    if (!modal.classList.contains('is-open')) return;
    if (e.key === 'Escape') cerrar();
    if (e.key === 'ArrowRight') ir(indice + 1);
    if (e.key === 'ArrowLeft')  ir(indice - 1);
  });

  // ---- Puntos (dots)
  diapos.forEach((_, i) => {
    const b = document.createElement('button');
    b.addEventListener('click', () => ir(i));
    puntos.appendChild(b);
  });

  // ---- Navegación
  function ir(i){
    indice = (i + diapos.length) % diapos.length; // wrap-around
    actualizar();
  }

  function actualizar(){
    // Mueve la pista
    pista.style.transform = `translateX(-${indice * 100}%)`;
    // Activa punto
    const allDots = puntos.querySelectorAll('button');
    allDots.forEach((d, di) => d.classList.toggle('is-active', di === indice));
  }

  btnPrev && btnPrev.addEventListener('click', () => ir(indice - 1));
  btnNext && btnNext.addEventListener('click', () => ir(indice + 1));

  // Estado inicial
  actualizar();
})();

