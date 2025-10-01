// Generador de PDF para la página datos.html
// Dependencias: jspdf (window.jspdf) y jspdf-autotable (doc.autoTable)
(function(){
  function generarPDFDatos() {
    const tabla = document.querySelector('.tabla-wrapper table') || document.querySelector('table');
    if (!tabla) return alert('No se encontró la tabla para exportar.');

    const headers = Array.from(tabla.querySelectorAll('thead th')).map(th => th.textContent.trim());
    const rows = Array.from(tabla.querySelectorAll('tbody tr')).map(tr => {
      return Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim());
    });

    if (!window.jspdf || !window.jspdf.jsPDF) {
      return alert('La biblioteca jsPDF no está cargada. Intenta recargar la página.');
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({ orientation: 'landscape' });
    doc.setFontSize(16);
    doc.text('Datos de Sensores', 14, 20);

    doc.autoTable({
      startY: 28,
      head: [headers],
      body: rows,
      theme: 'grid',
      headStyles: { fillColor: [29,145,0], textColor: 255 },
      styles: { fontSize: 10 }
    });

    doc.save('datos_sensores.pdf');
  }

  document.addEventListener('DOMContentLoaded', function(){
    const btn = document.getElementById('download-pdf-btn');
    if (!btn) return;
    btn.addEventListener('click', function(e){
      e.preventDefault();
      generarPDFDatos();
    });
  });
})();
