// Abrir / cerrar modals
function toggleModal(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.toggle('open');
}

// Cerrar modal al click en el overlay
document.querySelectorAll('.admin-modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', e => {
    if (e.target === overlay) overlay.classList.remove('open');
  });
});

// Cerrar con Escape
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.admin-modal-overlay.open').forEach(el => el.classList.remove('open'));
  }
});

// Pre-rellenar formulario de edición de libro
function editarLibro(id, isbn, titulo, genero, anio, ejemplares, descripcion) {
  const form = document.getElementById('formEditarLibro');
  if (!form) return;
  form.action = `/admin/libros/${id}/editar`;
  document.getElementById('edit-isbn').value       = isbn       || '';
  document.getElementById('edit-titulo').value     = titulo     || '';
  document.getElementById('edit-genero').value     = genero     || '';
  document.getElementById('edit-anio').value       = anio       || '';
  document.getElementById('edit-ejemplares').value = ejemplares || 1;
  document.getElementById('edit-descripcion').value = descripcion || '';
  toggleModal('modalEditarLibro');
}
