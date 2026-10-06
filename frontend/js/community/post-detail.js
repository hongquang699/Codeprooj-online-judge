/**
 * Post Detail Logic - View post, comments, add comment, like
 */
document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const postId = urlParams.get('id');
  if (postId) {
    loadPostDetail(postId);
    loadComments(postId);
    setupCommentForm(postId);
  }
});

async function loadPostDetail(postId) {
  const titleEl = document.getElementById('postDetailTitle');
  const authorEl = document.getElementById('postDetailAuthor');
  const dateEl = document.getElementById('postDetailDate');
  const contentEl = document.getElementById('postDetailContent');
  const tagsEl = document.getElementById('postDetailTags');
  const likeBtn = document.getElementById('btnLikePost');
  const likeCountEl = document.getElementById('postLikeCount');

  try {
    const res = await CommunityAPI.getPost(postId);
    if (!res || res.status !== 200) {
      if (titleEl) titleEl.textContent = 'Không tìm thấy bài viết';
      return;
    }

    const p = res.data;
    if (titleEl) titleEl.textContent = p.title;
    if (authorEl) authorEl.textContent = p.author_username;
    if (dateEl) dateEl.textContent = new Date(p.created_at).toLocaleString('vi-VN');
    if (contentEl) contentEl.innerHTML = p.content.replace(/\n/g, '<br>');
    if (likeCountEl) likeCountEl.textContent = p.like_count || 0;

    if (tagsEl) {
      tagsEl.innerHTML = (p.tags || []).map(t => `<span class="comm-tag">#${t}</span>`).join('');
    }

    if (likeBtn) {
      likeBtn.onclick = async () => {
        const likeRes = await CommunityAPI.toggleReaction('post', postId, 'like');
        if (likeRes && likeRes.status === 200 && likeCountEl) {
          likeCountEl.textContent = likeRes.data.reaction_count;
        }
      };
    }
  } catch (err) {
    console.error('Error loading post detail:', err);
  }
}

async function loadComments(postId) {
  const listEl = document.getElementById('commentsList');
  if (!listEl) return;

  try {
    const res = await CommunityAPI.getComments(postId);
    if (!res || res.status !== 200) return;

    const comments = res.data.objects || [];
    if (comments.length === 0) {
      listEl.innerHTML = '<div style="color:#64748b;padding:1.5rem 0;">Chưa có bình luận nào. Hãy chia sẻ suy nghĩ của bạn!</div>';
    } else {
      listEl.innerHTML = comments.map(c => `
        <div class="comm-comment-item">
          <div class="comm-avatar" style="width:34px;height:34px;font-size:0.85rem;">
            ${c.author_username.charAt(0).toUpperCase()}
          </div>
          <div class="comm-comment-bubble">
            <div class="comm-comment-meta">
              <strong style="color:#fff;font-size:0.88rem;">${c.author_username}</strong>
              <span style="font-size:0.75rem;color:#64748b;">${new Date(c.created_at).toLocaleDateString('vi-VN', {hour:'2-digit', minute:'2-digit'})}</span>
            </div>
            <div style="font-size:0.9rem;color:#cbd5e1;line-height:1.5;">${c.content}</div>
          </div>
        </div>
      `).join('');
    }
  } catch (err) {
    console.error('Error loading comments:', err);
  }
}

function setupCommentForm(postId) {
  const btn = document.getElementById('btnSubmitComment');
  const input = document.getElementById('commentInput');
  if (!btn || !input) return;

  btn.addEventListener('click', async () => {
    const content = input.value.trim();
    if (!content) {
      alert('Vui lòng nhập nội dung bình luận!');
      return;
    }

    btn.disabled = true;
    try {
      const res = await CommunityAPI.addComment(postId, { content });
      if (res && res.status === 201) {
        input.value = '';
        await loadComments(postId);
      } else {
        alert(res?.error?.message || 'Không thể gửi bình luận');
      }
    } catch (err) {
      alert('Lỗi: ' + err.message);
    } finally {
      btn.disabled = false;
    }
  });
}
