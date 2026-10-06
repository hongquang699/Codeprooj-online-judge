/**
 * Notifications Logic
 */
document.addEventListener('DOMContentLoaded', () => {
  loadNotifications();
  setupReadAll();
});

async function loadNotifications() {
  const listEl = document.getElementById('notifsList');
  if (!listEl) return;

  try {
    const res = await CommunityAPI.getNotifications();
    if (!res || res.status !== 200) {
      listEl.innerHTML = '<div style="color:#94a3b8;padding:2rem;">Không thể tải thông báo.</div>';
      return;
    }

    const notifs = res.data.objects || [];
    if (notifs.length === 0) {
      listEl.innerHTML = '<div style="color:#64748b;padding:2rem;text-align:center;">Bạn không có thông báo mới nào.</div>';
      return;
    }

    listEl.innerHTML = notifs.map(n => {
      const icon = n.notification_type === 'comment' ? '💬' : (n.notification_type === 'reply' ? '↩️' : (n.notification_type === 'reaction' ? '👍' : '🔔'));
      const bg = n.is_read ? 'transparent' : 'rgba(59, 130, 246, 0.05)';
      return `
        <div style="padding:1rem;border-bottom:1px solid rgba(255,255,255,0.05);background:${bg};display:flex;align-items:flex-start;gap:0.75rem;">
          <div style="font-size:1.2rem;">${icon}</div>
          <div style="flex:1;">
            <div style="font-weight:700;color:#fff;font-size:0.92rem;margin-bottom:0.2rem;">${n.title}</div>
            <div style="font-size:0.86rem;color:#cbd5e1;line-height:1.4;">${n.message}</div>
            <div style="font-size:0.75rem;color:#64748b;margin-top:0.4rem;">${new Date(n.created_at).toLocaleString('vi-VN')}</div>
          </div>
          ${n.link ? `<a href="${n.link}" class="comm-btn-primary" style="padding:0.3rem 0.75rem;font-size:0.78rem;">Xem</a>` : ''}
        </div>
      `;
    }).join('');

  } catch (err) {
    console.error('Notifications error:', err);
  }
}

function setupReadAll() {
  const btn = document.getElementById('btnReadAll');
  if (!btn) return;
  btn.addEventListener('click', async () => {
    try {
      await CommunityAPI.readAllNotifications();
      await loadNotifications();
    } catch (err) {
      console.error('Read all error:', err);
    }
  });
}
