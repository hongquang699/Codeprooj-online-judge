function renderPagination(total, page, pageSize, onPageChange, containerId = 'rankingPagination') {
  const container = document.getElementById(containerId);
  if (!container) return;

  const totalPages = Math.ceil(total / pageSize);
  if (totalPages <= 1) {
    container.innerHTML = '';
    return;
  }

  let html = `<div class="pagination-wrapper">`;
  html += `<button class="page-btn" ${page <= 1 ? 'disabled' : ''} onclick="(${onPageChange})(${page - 1})">← Trang trước</button>`;
  
  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || (i >= page - 2 && i <= page + 2)) {
      html += `<button class="page-btn ${i === page ? 'active' : ''}" onclick="(${onPageChange})(${i})">${i}</button>`;
    } else if (i === page - 3 || i === page + 3) {
      html += `<span class="page-dots">...</span>`;
    }
  }

  html += `<button class="page-btn" ${page >= totalPages ? 'disabled' : ''} onclick="(${onPageChange})(${page + 1})">Trang sau →</button>`;
  html += `</div>`;
  container.innerHTML = html;
}
window.renderPagination = renderPagination;
