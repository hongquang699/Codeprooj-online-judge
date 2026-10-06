/**
 * Forum logic - Load Categories and Threads
 */
document.addEventListener('DOMContentLoaded', () => {
  initForum();
});

async function initForum() {
  const catGrid = document.getElementById('forumCatGrid');
  const threadTableBdy = document.getElementById('forumThreadTbody');

  try {
    const catRes = await CommunityAPI.getCategories();
    if (catRes && catRes.status === 200 && catGrid) {
      catGrid.innerHTML = catRes.data.objects.map(c => `
        <a href="/frontend/html/community/forum/category.html?slug=${c.slug}" class="forum-cat-card">
          <div>
            <div class="forum-cat-title">
              <span>💬</span> ${c.name}
            </div>
            <div class="forum-cat-desc">${c.description}</div>
          </div>
          <div class="forum-cat-meta">
            <span>📝 ${c.thread_count || 0} chủ đề</span>
            <span>💬 ${c.post_count || 0} phản hồi</span>
          </div>
        </a>
      `).join('');
    }

    const threadRes = await CommunityAPI.getThreads();
    if (threadRes && threadRes.status === 200 && threadTableBdy) {
      if (threadRes.data.objects.length === 0) {
        threadTableBdy.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:2rem;color:#64748b;">Chưa có chủ đề thảo luận nào.</td></tr>';
      } else {
        threadTableBdy.innerHTML = threadRes.data.objects.map(t => {
          const dateStr = new Date(t.last_activity_at).toLocaleDateString('vi-VN', {hour:'2-digit', minute:'2-digit'});
          return `
            <tr class="forum-thread-row">
              <td>
                <div style="display:flex;align-items:center;">
                  ${t.is_pinned ? '<span class="pinned-badge">GHIM</span>' : ''}
                  ${t.is_locked ? '<span class="locked-badge">KHÓA</span>' : ''}
                  <a href="/frontend/html/community/forum/thread.html?id=${t.id}" class="forum-thread-title">${t.title}</a>
                </div>
                <div style="font-size:0.78rem;color:#94a3b8;margin-top:0.25rem;">
                  Tác giả: <a href="/frontend/html/user/profile.html?u=${t.author_username}" style="color:#60a5fa;text-decoration:none;">${t.author_username}</a>
                </div>
              </td>
              <td><span style="font-size:0.82rem;color:#94a3b8;background:#1e293b;padding:0.2rem 0.5rem;border-radius:4px;">${t.category_name}</span></td>
              <td style="color:#cbd5e1;font-weight:600;">${t.reply_count}</td>
              <td style="color:#94a3b8;">${t.view_count}</td>
              <td style="font-size:0.8rem;color:#64748b;">${dateStr}</td>
            </tr>
          `;
        }).join('');
      }
    }
  } catch (err) {
    console.error('Forum load error:', err);
  }
}
