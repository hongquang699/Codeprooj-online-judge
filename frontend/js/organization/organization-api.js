/**
 * CodeProOJ - Organization Client API & UI Components
 */

const OrgAPI = {
  BASE_URL: (window.API_BASE || window.location.origin) + '/api/v1/organizations',

  getCurrentUser() {
    return localStorage.getItem('username') || '';
  },

  getOrgSlugFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('org')) return urlParams.get('org');

    const pathParts = window.location.pathname.split('/').filter(Boolean);
    const orgIndex = pathParts.indexOf('organizations');
    if (orgIndex !== -1 && pathParts[orgIndex + 1]) {
      return pathParts[orgIndex + 1];
    }
    return 'codeprooj'; // Default fallback
  },

  async request(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...(options.headers || {})
    };

    try {
      const res = await fetch(`${this.BASE_URL}${endpoint}`, { ...options, headers });
      const json = await res.json();
      return json;
    } catch (err) {
      console.error(`OrgAPI Error [${endpoint}]:`, err);
      return { status: 500, error: 'Lỗi kết nối tới máy chủ.' };
    }
  },

  getOrg(slug) {
    return this.request(`/${slug}/`);
  },

  listOrgs(search = '') {
    return this.request(`/?search=${encodeURIComponent(search)}`);
  },

  createOrg(payload) {
    return this.request('/', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  },

  joinOrg(slug) {
    return this.request(`/${slug}/join/`, { method: 'POST' });
  },

  leaveOrg(slug) {
    return this.request(`/${slug}/leave/`, { method: 'POST' });
  },

  getMembers(slug, role = 'all', search = '') {
    return this.request(`/${slug}/members/?role=${encodeURIComponent(role)}&search=${encodeURIComponent(search)}`);
  },

  getContests(slug) {
    return this.request(`/${slug}/contests/`);
  },

  getProblems(slug, difficulty = 'all', search = '') {
    return this.request(`/${slug}/problems/?difficulty=${encodeURIComponent(difficulty)}&search=${encodeURIComponent(search)}`);
  },

  getRanking(slug) {
    return this.request(`/${slug}/ranking/`);
  },

  getBlog(slug) {
    return this.request(`/${slug}/blog/`);
  },

  getBlogDetail(slug, id) {
    return this.request(`/${slug}/blog/${id}/`);
  },

  getAnnouncements(slug) {
    return this.request(`/${slug}/announcements/`);
  },

  getActivity(slug) {
    return this.request(`/${slug}/activity/`);
  },

  // Admin APIs
  getAdminStats(slug) {
    return this.request(`/${slug}/admin/stats/`);
  },

  getAdminRoles(slug) {
    return this.request(`/${slug}/admin/roles/`);
  },

  getAdminInvitations(slug) {
    return this.request(`/${slug}/admin/invitations/`);
  },

  getAdminAuditLog(slug) {
    return this.request(`/${slug}/admin/audit-log/`);
  },

  updateSettings(slug, payload) {
    return this.request(`/${slug}/`, {
      method: 'PATCH',
      body: JSON.stringify(payload)
    });
  },

  updateMember(slug, username, payload) {
    return this.request(`/${slug}/members/${username}/`, {
      method: 'PATCH',
      body: JSON.stringify(payload)
    });
  },

  removeMember(slug, username) {
    return this.request(`/${slug}/members/${username}/`, {
      method: 'DELETE'
    });
  },

  linkContest(slug, payload) {
    const body = typeof payload === 'object' ? payload : { contest_key: payload };
    return this.request(`/${slug}/contests/`, {
      method: 'POST',
      body: JSON.stringify(body)
    });
  },

  unlinkContest(slug, contestKey) {
    return this.request(`/${slug}/contests/`, {
      method: 'DELETE',
      body: JSON.stringify({ contest_key: contestKey })
    });
  },

  getAvailableContests(slug) {
    return this.request(`/${slug}/contests/?available=1`);
  },

  linkProblem(slug, payload) {
    const body = typeof payload === 'object' ? payload : { code: payload };
    return this.request(`/${slug}/problems/`, {
      method: 'POST',
      body: JSON.stringify(body)
    });
  },

  createProblem(slug, payload) {
    return this.request(`/${slug}/problems/`, {
      method: 'POST',
      body: JSON.stringify({ ...payload, is_new: true })
    });
  },

  unlinkProblem(slug, problemCode) {
    return this.request(`/${slug}/problems/`, {
      method: 'DELETE',
      body: JSON.stringify({ code: problemCode })
    });
  },

  getAvailableProblems(slug) {
    return this.request(`/${slug}/problems/?available=1`);
  },

  createPost(slug, payload) {
    return this.request(`/${slug}/blog/`, {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  },

  deletePost(slug, postId) {
    return this.request(`/${slug}/blog/${postId}/`, {
      method: 'DELETE'
    });
  },

  createAnnouncement(slug, payload) {
    return this.request(`/${slug}/announcements/`, {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  },

  deleteAnnouncement(slug, annId) {
    return this.request(`/${slug}/announcements/`, {
      method: 'DELETE',
      body: JSON.stringify({ id: annId })
    });
  },

  sendInvitation(slug, payload) {
    return this.request(`/${slug}/admin/invitations/`, {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  },

  // ── UI Components Renderers ──
  renderHeader(org, activeTab = 'overview') {
    const container = document.getElementById('orgHeaderTarget');
    if (!container) return;

    const isMember = Boolean(org.user_role);
    const canAccessAdmin = org.can_manage === true;

    // Admin Floating Quick Shortcut (Exclusively rendered for Admins)
    let floatingBtn = document.getElementById('orgAdminFloatingShortcut');
    if (canAccessAdmin) {
      if (!floatingBtn) {
        floatingBtn = document.createElement('a');
        floatingBtn.id = 'orgAdminFloatingShortcut';
        floatingBtn.href = `/frontend/html/organization/admin/index.html?org=${org.slug}`;
        floatingBtn.title = `Lối tắt Bảng Điều Khiển Quản Trị Tổ Chức (Dành riêng cho Admin)`;
        floatingBtn.innerHTML = `
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:6px;"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
          <span>Quản trị ${org.short_name || org.name || 'Tổ chức'}</span>
        `;
        Object.assign(floatingBtn.style, {
          position: 'fixed',
          bottom: '24px',
          right: '24px',
          zIndex: '9999',
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          padding: '10px 18px',
          background: 'linear-gradient(135deg, #7c3aed, #4f46e5)',
          color: '#ffffff',
          fontWeight: '700',
          fontSize: '0.88rem',
          borderRadius: '9999px',
          boxShadow: '0 8px 24px rgba(124, 58, 237, 0.45), 0 2px 6px rgba(0,0,0,0.3)',
          textDecoration: 'none',
          border: '1px solid rgba(255,255,255,0.2)',
          transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
          cursor: 'pointer'
        });
        floatingBtn.onmouseenter = () => { floatingBtn.style.transform = 'translateY(-2px) scale(1.03)'; floatingBtn.style.boxShadow = '0 12px 28px rgba(124, 58, 237, 0.6)'; };
        floatingBtn.onmouseleave = () => { floatingBtn.style.transform = 'translateY(0) scale(1)'; floatingBtn.style.boxShadow = '0 8px 24px rgba(124, 58, 237, 0.45)'; };
        document.body.appendChild(floatingBtn);
      }
    } else if (floatingBtn) {
      floatingBtn.remove();
    }

    const verifiedHtml = org.verified ? `
      <span class="org-verified-badge" title="Tổ chức chính chủ được xác minh">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" style="vertical-align:middle;">
          <path d="M9 12L11 14L15 10M12 3L13.91 4.26L16.14 3.73L17.55 5.48L19.78 5.74L20.31 7.97L22.06 9.38L21.53 11.61L22.79 13.52L21.53 15.43L22.06 17.66L20.31 19.07L19.78 21.3L17.55 21.56L16.14 23.31L13.91 22.78L12 24.04L10.09 22.78L7.86 23.31L6.45 21.56L4.22 21.3L3.69 19.07L1.94 17.66L2.47 15.43L1.21 13.52L2.47 11.61L1.94 9.38L3.69 7.97L4.22 5.74L6.45 5.48L7.86 3.73L10.09 4.26L12 3Z" fill="#38BDF8" stroke="#0284C7" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M8.5 12.5L11 15L16 9" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        ĐÃ XÁC MINH
      </span>
    ` : '';

    container.innerHTML = `
      <div class="org-hero-card">
        <div class="org-hero-cover"></div>
        <div class="org-hero-body">
          <div class="org-hero-profile">
            <div class="org-hero-logo">
              <img src="${org.logo || '/frontend/assets/icons/org-default.svg'}" alt="${org.name}">
            </div>
            <div class="org-hero-info">
              <div class="org-hero-title-row">
                <h1 class="org-hero-name">${org.short_name || org.name}</h1>
                ${verifiedHtml}
              </div>
              <div class="org-hero-fullname">${org.name}</div>
              <div class="org-hero-meta">
                <span class="org-hero-meta-item">
                  <cp-icon name="user" size="sm"></cp-icon> <strong>${(org.member_count || 0).toLocaleString()}</strong> thành viên
                </span>
                ${org.website ? `
                  <span class="org-hero-meta-item">
                    <cp-icon name="globe" size="sm"></cp-icon> <a href="${org.website}" target="_blank" style="color:#60a5fa;">${org.website.replace('https://', '')}</a>
                  </span>
                ` : ''}
                ${org.user_role ? `
                  <span class="org-hero-meta-item" style="color:#38bdf8;">
                    <cp-icon name="award" size="sm"></cp-icon> Vai trò: <strong>${org.user_role}</strong>
                  </span>
                ` : ''}
              </div>
            </div>
          </div>

          <div class="org-hero-actions">
            ${isMember ? `
              <button onclick="OrgAPI.handleLeave('${org.slug}')" class="btn-org-outline" style="color:#f87171; border-color:rgba(239, 68, 68, 0.4);">
                <cp-icon name="logout" size="sm"></cp-icon> Rời tổ chức
              </button>
            ` : `
              <button onclick="OrgAPI.handleJoin('${org.slug}')" class="btn-org-cta">
                <cp-icon name="plus" size="sm"></cp-icon> Tham gia tổ chức
              </button>
            `}

            ${canAccessAdmin ? `
              <a href="/frontend/html/organization/admin/index.html?org=${org.slug}" class="btn-org-admin" style="box-shadow: 0 4px 14px rgba(139, 92, 246, 0.4);" title="Lối tắt Quản trị Tổ chức (Dành riêng cho Admin)">
                <cp-icon name="settings" size="sm"></cp-icon> Quản trị Tổ chức
              </a>
            ` : ''}
          </div>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="org-tabs-card">
        <a href="/organizations/${org.slug}/overview" class="org-tab-link ${activeTab === 'overview' ? 'active' : ''}">
          <cp-icon name="home" size="sm"></cp-icon> Tổng quan
        </a>
        <a href="/organizations/${org.slug}/contests" class="org-tab-link ${activeTab === 'contests' ? 'active' : ''}">
          <cp-icon name="trophy" size="sm"></cp-icon> Cuộc thi
          <span class="org-tab-badge">${org.contest_count || 0}</span>
        </a>
        <a href="/organizations/${org.slug}/problems" class="org-tab-link ${activeTab === 'problems' ? 'active' : ''}">
          <cp-icon name="code" size="sm"></cp-icon> Bài tập
          <span class="org-tab-badge">${org.problem_count || 0}</span>
        </a>
        <a href="/organizations/${org.slug}/members" class="org-tab-link ${activeTab === 'members' ? 'active' : ''}">
          <cp-icon name="users" size="sm"></cp-icon> Thành viên
          <span class="org-tab-badge">${(org.member_count || 0).toLocaleString()}</span>
        </a>
        <a href="/organizations/${org.slug}/ranking" class="org-tab-link ${activeTab === 'ranking' ? 'active' : ''}">
          <cp-icon name="chart" size="sm"></cp-icon> Bảng xếp hạng
        </a>
        <a href="/organizations/${org.slug}/blog" class="org-tab-link ${activeTab === 'blog' ? 'active' : ''}">
          <cp-icon name="file-text" size="sm"></cp-icon> Blog / Tin tức
        </a>
        <a href="/organizations/${org.slug}/announcements" class="org-tab-link ${activeTab === 'announcements' ? 'active' : ''}">
          <cp-icon name="bell" size="sm"></cp-icon> Thông báo
        </a>
        <a href="/organizations/${org.slug}/activity" class="org-tab-link ${activeTab === 'activity' ? 'active' : ''}">
          <cp-icon name="activity" size="sm"></cp-icon> Hoạt động
        </a>
      </div>
    `;
  },

  async handleJoin(slug) {
    const res = await this.joinOrg(slug);
    alert(res.message || res.error);
    if (res.status === 200) window.location.reload();
  },

  async handleLeave(slug) {
    if (!confirm('Bạn có chắc chắn muốn rời khỏi tổ chức này?')) return;
    const res = await this.leaveOrg(slug);
    alert(res.message || res.error);
    if (res.status === 200) window.location.reload();
  }
};
