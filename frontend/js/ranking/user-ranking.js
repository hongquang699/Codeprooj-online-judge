async function loadUserRankingProfile(username = 'tourist_vn') {
  try {
    const data = await window.RankingApi.fetchUserRanking(username);
    const container = document.getElementById('userCardContainer');
    if (!container) return;

    const tierCls = window.getTierClass ? window.getTierClass(data.tier, data.rating) : ((data.rating === 0 || !data.rating) ? 'tier-unrated' : 'tier-new');

    container.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px; margin-bottom: 24px;">
        <div>
          <h2 class="${tierCls}" style="font-size: 26px; margin: 0 0 6px 0;">${data.username}</h2>
          <div style="color: #94a3b8; font-size: 14px;">
            ${data.school ? `<span><i class="fi fi-rr-graduation-cap"></i> ${data.school}</span> • ` : ''}
            <span><i class="fi fi-rr-globe"></i> ${data.country}</span>
          </div>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
          <span class="rating-pill pill-${(data.badge || 'spec').toLowerCase()}" style="font-size: 13px; padding: 4px 12px;">
            ${data.tier}
          </span>
          <a href="/frontend/html/ranking/rating-history.html?user=${encodeURIComponent(data.username)}" class="ranking-btn" style="text-decoration: none;">
            <i class="fi fi-rr-chart-line-up"></i> Xem biểu đồ Rating
          </a>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px;">
        <div style="background: #0f172a; padding: 16px; border-radius: 8px; text-align: center; border: 1px solid #1e293b;">
          <div style="color: #94a3b8; font-size: 12px; margin-bottom: 4px;"><i class="fi fi-rr-trophy"></i> XẾP HẠNG TOÀN CẦU</div>
          <div style="font-size: 24px; font-weight: 800; color: #fbbf24;">#${data.global_rank}</div>
        </div>
        <div style="background: #0f172a; padding: 16px; border-radius: 8px; text-align: center; border: 1px solid #1e293b;">
          <div style="color: #94a3b8; font-size: 12px; margin-bottom: 4px;"><i class="fi fi-rr-bolt"></i> CURRENT RATING</div>
          <div class="${tierCls}" style="font-size: 24px; font-weight: 800;">${data.rating}</div>
        </div>
        <div style="background: #0f172a; padding: 16px; border-radius: 8px; text-align: center; border: 1px solid #1e293b;">
          <div style="color: #94a3b8; font-size: 12px; margin-bottom: 4px;"><i class="fi fi-rr-star"></i> MAX RATING</div>
          <div style="font-size: 24px; font-weight: 800; color: #f1f5f9;">${data.max_rating}</div>
        </div>
        <div style="background: #0f172a; padding: 16px; border-radius: 8px; text-align: center; border: 1px solid #1e293b;">
          <div style="color: #94a3b8; font-size: 12px; margin-bottom: 4px;"><i class="fi fi-rr-check"></i> BÀI ĐÃ GIẢI (AC)</div>
          <div style="font-size: 24px; font-weight: 800; color: #10b981;">${data.solved}</div>
        </div>
        <div style="background: #0f172a; padding: 16px; border-radius: 8px; text-align: center; border: 1px solid #1e293b;">
          <div style="color: #94a3b8; font-size: 12px; margin-bottom: 4px;"><i class="fi fi-rr-document"></i> TỔNG BÀI NỘP</div>
          <div style="font-size: 24px; font-weight: 800; color: #3b82f6;">${data.submissions}</div>
        </div>
        <div style="background: #0f172a; padding: 16px; border-radius: 8px; text-align: center; border: 1px solid #1e293b;">
          <div style="color: #94a3b8; font-size: 12px; margin-bottom: 4px;"><i class="fi fi-rr-flag"></i> KỲ THI ĐÃ ĐẤU</div>
          <div style="font-size: 24px; font-weight: 800; color: #a855f7;">${data.contests_count}</div>
        </div>
      </div>
    `;
  } catch (err) {
    const container = document.getElementById('userCardContainer');
    if (container) {
      container.innerHTML = `<div style="text-align: center; color: #ef4444; padding: 40px;">Lỗi tải hồ sơ: ${err.message}</div>`;
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const user = urlParams.get('user') || 'tourist_vn';
  loadUserRankingProfile(user);
});

window.loadUserRankingProfile = loadUserRankingProfile;
