/**
 * CodeProOJ Contest Scoreboard Logic
 * Connects to /api/v2/contest/<contest>/scoreboard
 */

async function loadScoreboard() {
  const urlParams = new URLSearchParams(window.location.search);
  const contestKey = urlParams.get('contest') || 'weekly-01';

  const nameEl = document.getElementById('contestName');
  const tbody = document.getElementById('scoreboardBody');

  try {
    const res = await api.get(`/contest/${encodeURIComponent(contestKey)}/scoreboard`);
    if (!res.success || !res.data) {
      if (tbody) {
        tbody.innerHTML = `
          <tr>
            <td colspan="5" style="text-align: center; padding: 2rem; color: #ef4444;">
              Không thể tải bảng điểm cho kỳ thi <code>${contestKey}</code>.
            </td>
          </tr>
        `;
      }
      return;
    }

    const data = res.data;
    if (nameEl) nameEl.innerText = data.name || contestKey;

    const standings = data.standings || [];
    if (standings.length === 0) {
      if (tbody) {
        tbody.innerHTML = `
          <tr>
            <td colspan="5" style="text-align: center; padding: 2rem; color: var(--color-text-muted);">
              Chưa có thí sinh nào tham gia kỳ thi này.
            </td>
          </tr>
        `;
      }
      return;
    }

    if (tbody) {
      tbody.innerHTML = standings.map((s, idx) => {
        let medal = '';
        if (s.rank === 1) medal = '🥇';
        else if (s.rank === 2) medal = '🥈';
        else if (s.rank === 3) medal = '🥉';

        return `
          <tr>
            <td style="font-weight: 700; text-align: center;">
              ${medal} ${s.rank}
            </td>
            <td>
              <a href="/profile/${encodeURIComponent(s.user)}" style="color: #60a5fa; font-weight: 600; text-decoration: none;">
                ${s.user}
              </a>
            </td>
            <td style="font-weight: 700; color: #10b981; font-size: 1.1rem;">
              ${s.score}
            </td>
            <td style="color: var(--color-text-muted);">
              ${s.penalty} phút
            </td>
            <td>
              <span class="badge badge-ac">Tham gia</span>
            </td>
          </tr>
        `;
      }).join('');
    }
  } catch (err) {
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: #ef4444;">Lỗi: ${err.message}</td></tr>`;
    }
  }
}

document.addEventListener('DOMContentLoaded', loadScoreboard);
