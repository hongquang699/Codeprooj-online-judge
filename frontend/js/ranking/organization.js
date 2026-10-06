async function loadOrgRankings() {
  try {
    const data = await window.RankingApi.fetchOrgRankings();
    const tbody = document.getElementById('orgTableBody');
    if (!tbody) return;

    if (!data.organizations || data.organizations.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #94a3b8; padding: 40px;">Không có dữ liệu tổ chức.</td></tr>';
      return;
    }

    tbody.innerHTML = data.organizations.map((org, idx) => {
      let badgeCls = 'standard';
      if (idx === 0) badgeCls = 'top-1';
      else if (idx === 1) badgeCls = 'top-2';
      else if (idx === 2) badgeCls = 'top-3';

      return `
        <tr>
          <td><span class="rank-badge ${badgeCls}">${idx + 1}</span></td>
          <td>
            <strong>${org.name}</strong>
            <span style="color: #94a3b8; font-size: 12px; margin-left: 8px;">(${org.short_name})</span>
          </td>
          <td>${org.members_count}</td>
          <td><strong style="color: #3b82f6;">${org.total_solved}</strong></td>
          <td><strong style="color: #10b981;">${org.avg_rating}</strong></td>
          <td>
            ${org.top_member ? `<a href="/profile/${encodeURIComponent(org.top_member)}" style="color: #f59e0b; font-weight: 600; text-decoration: none;">${org.top_member}</a>` : '-'}
          </td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    const tbody = document.getElementById('orgTableBody');
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: #ef4444; padding: 30px;">Lỗi: ${err.message}</td></tr>`;
    }
  }
}

document.addEventListener('DOMContentLoaded', loadOrgRankings);
window.loadOrgRankings = loadOrgRankings;
