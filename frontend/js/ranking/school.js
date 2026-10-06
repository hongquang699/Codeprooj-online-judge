async function loadSchoolRankings() {
  try {
    const data = await window.RankingApi.fetchSchoolRankings();
    const tbody = document.getElementById('schoolTableBody');
    if (!tbody) return;

    if (!data.schools || data.schools.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #94a3b8; padding: 40px;">Không có dữ liệu trường học.</td></tr>';
      return;
    }

    tbody.innerHTML = data.schools.map((s, idx) => {
      let badgeCls = 'standard';
      if (idx === 0) badgeCls = 'top-1';
      else if (idx === 1) badgeCls = 'top-2';
      else if (idx === 2) badgeCls = 'top-3';

      return `
        <tr>
          <td><span class="rank-badge ${badgeCls}">${idx + 1}</span></td>
          <td><strong>${s.school}</strong></td>
          <td>${s.students_count}</td>
          <td><strong style="color: #3b82f6;">${s.total_solved}</strong></td>
          <td><strong style="color: #10b981;">${s.avg_rating}</strong></td>
          <td>
            ${s.top_student ? `<a href="/profile/${encodeURIComponent(s.top_student)}" style="color: #f59e0b; font-weight: 600; text-decoration: none;">${s.top_student}</a>` : '-'}
          </td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    const tbody = document.getElementById('schoolTableBody');
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: #ef4444; padding: 30px;">Lỗi: ${err.message}</td></tr>`;
    }
  }
}

document.addEventListener('DOMContentLoaded', loadSchoolRankings);
window.loadSchoolRankings = loadSchoolRankings;
