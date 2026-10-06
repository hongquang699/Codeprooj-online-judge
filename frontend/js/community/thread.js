/**
 * Thread Detail & Reply Logic
 */
document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const threadId = urlParams.get('id');
  if (threadId) {
    loadThread(threadId);
    setupReplyForm(threadId);
  }
});

async function loadThread(threadId) {
  const titleEl = document.getElementById('threadTitle');
  const catEl = document.getElementById('threadCategory');
  const originalPostEl = document.getElementById('threadOriginalPost');
  const repliesListEl = document.getElementById('threadRepliesList');

  try {
    const res = await CommunityAPI.getThread(threadId);
    if (!res || res.status !== 200) {
      if (titleEl) titleEl.textContent = 'Không tìm thấy chủ đề';
      return;
    }

    const t = res.data;
    if (titleEl) titleEl.textContent = t.title;
    if (catEl) catEl.textContent = t.category_name;

    if (originalPostEl) {
      originalPostEl.innerHTML = `
        <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1rem;">
          <div class="comm-avatar">${t.author_username.charAt(0).toUpperCase()}</div>
          <div>
            <div style="font-weight:700;color:#fff;">${t.author_username}</div>
            <div style="font-size:0.78rem;color:#94a3b8;">Đăng lúc ${new Date(t.created_at).toLocaleString('vi-VN')}</div>
          </div>
        </div>
        <div style="line-height:1.6;color:#e2e8f0;white-space:pre-wrap;">${t.content}</div>
      `;
    }

    if (repliesListEl) {
      const posts = t.posts || [];
      if (posts.length === 0) {
        repliesListEl.innerHTML = '<div style="color:#64748b;padding:1.5rem 0;">Chưa có phản hồi nào. Hãy là người đầu tiên trao đổi!</div>';
      } else {
        repliesListEl.innerHTML = posts.map(p => `
          <div class="comm-card" style="margin-bottom:1rem;background:#0d1322;">
            <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.75rem;">
              <div class="comm-avatar" style="width:32px;height:32px;font-size:0.85rem;">${p.author_username.charAt(0).toUpperCase()}</div>
              <div>
                <span style="font-weight:700;color:#fff;font-size:0.9rem;">${p.author_username}</span>
                <span style="font-size:0.75rem;color:#94a3b8;margin-left:0.5rem;">${new Date(p.created_at).toLocaleString('vi-VN')}</span>
              </div>
            </div>
            <div style="line-height:1.6;color:#cbd5e1;white-space:pre-wrap;">${p.content}</div>
          </div>
        `).join('');
      }
    }

  } catch (err) {
    console.error('Error loading thread:', err);
  }
}

function setupReplyForm(threadId) {
  const btn = document.getElementById('btnSubmitReply');
  const input = document.getElementById('replyContent');
  if (!btn || !input) return;

  btn.addEventListener('click', async () => {
    const content = input.value.trim();
    if (!content) {
      alert('Vui lòng nhập nội dung phản hồi!');
      return;
    }

    btn.disabled = true;
    btn.textContent = 'Đang gửi...';

    try {
      const res = await CommunityAPI.replyThread(threadId, content);
      if (res && res.status === 201) {
        input.value = '';
        await loadThread(threadId);
      } else {
        alert(res?.error?.message || 'Không thể gửi phản hồi');
      }
    } catch (err) {
      alert('Lỗi: ' + err.message);
    } finally {
      btn.disabled = false;
      btn.textContent = 'Gửi phản hồi';
    }
  });
}
