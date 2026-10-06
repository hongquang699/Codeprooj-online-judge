async function loadContestScoreboard(contestKey = 'weekly-01') {
  try {
    const data = await window.ContestRankingApi.fetchScoreboard(contestKey, true);
    
    // Update Contest Title
    if (data.contest) {
      const titleEl = document.getElementById('contestTitle');
      const subEl = document.getElementById('contestSubtitle');
      if (titleEl) titleEl.innerHTML = `<i class="fi fi-rr-chart-histogram"></i> ${data.contest.name}`;
      if (subEl) subEl.innerText = `Thể thức: ${data.contest.format.toUpperCase()} | Tổng bài: ${data.problems.length} | Thí sinh: ${data.rows.length}`;
    }

    // Build Table Header
    const headRow = document.querySelector('#scoreboardHead tr');
    if (headRow) {
      let headHtml = `
        <th style="width: 60px;">#</th>
        <th>Thí sinh</th>
        <th style="width: 70px; text-align: center;">=</th>
        <th style="width: 90px; text-align: center;">Penalty</th>
      `;
      for (const p of data.problems) {
        headHtml += `<th class="problem-col" title="${p.name} (${p.code})">${p.prefix}</th>`;
      }
      headRow.innerHTML = headHtml;
    }

    // Build Table Body
    const tbody = document.getElementById('scoreboardBody');
    if (!tbody) return;

    if (!data.rows || data.rows.length === 0) {
      tbody.innerHTML = `<tr><td colspan="${4 + data.problems.length}" style="text-align: center; color: #94a3b8; padding: 40px;">Chưa có bài nộp nào trong cuộc thi này.</td></tr>`;
      return;
    }

    tbody.innerHTML = data.rows.map(row => {
      let badgeCls = 'standard';
      if (row.rank === 1) badgeCls = 'top-1';
      else if (row.rank === 2) badgeCls = 'top-2';
      else if (row.rank === 3) badgeCls = 'top-3';

      const initial = (row.username || '?').charAt(0).toUpperCase();

      let rowHtml = `
        <tr>
          <td><span class="rank-badge ${badgeCls}">${row.rank}</span></td>
          <td>
            <a href="/profile/${encodeURIComponent(row.username)}" class="user-cell" style="text-decoration: none; color: inherit;">
              <div class="user-avatar">${initial}</div>
              <span class="user-handle" style="color: #60a5fa;">
                ${row.username}
              </span>
            </a>
          </td>
          <td style="text-align: center; font-weight: 700; font-size: 15px;">${row.solved}</td>
          <td style="text-align: center; color: #94a3b8;">${row.penalty}</td>
      `;

      // Problem Columns
      for (const p of data.problems) {
        const probRes = row.problem_results ? row.problem_results[p.prefix] : null;
        const cellContent = window.renderProblemScoreCell ? window.renderProblemScoreCell(probRes) : '.';
        rowHtml += `<td class="cell-problem">${cellContent}</td>`;
      }

      rowHtml += `</tr>`;
      return rowHtml;
    }).join('');

  } catch (err) {
    const tbody = document.getElementById('scoreboardBody');
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: #ef4444; padding: 30px;">Lỗi tải bảng điểm: ${err.message}</td></tr>`;
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const contestKey = urlParams.get('id') || urlParams.get('key') || 'weekly-01';
  
  const inputEl = document.getElementById('contestKeyInput');
  if (inputEl) inputEl.value = contestKey;

  loadContestScoreboard(contestKey);

  const btn = document.getElementById('loadScoreboardBtn');
  if (btn) {
    btn.addEventListener('click', () => {
      const key = inputEl ? inputEl.value.trim() : 'weekly-01';
      loadContestScoreboard(key);
    });
  }

  const recalcBtn = document.getElementById('recalcRatingBtn');
  if (recalcBtn) {
    recalcBtn.addEventListener('click', async () => {
      try {
        recalcBtn.disabled = true;
        recalcBtn.innerText = 'Đang tính toán...';
        await window.ContestRankingApi.recalculateRatings(1);
        alert('Đã tính toán và cập nhật rating thành công cho tất cả thí sinh!');
        loadContestScoreboard(contestKey);
      } catch (e) {
        alert('Lỗi tính rating: ' + e.message);
      } finally {
        recalcBtn.disabled = false;
        recalcBtn.innerText = 'Tính lại Rating Kỳ thi';
      }
    });
  }
});

window.loadContestScoreboard = loadContestScoreboard;
