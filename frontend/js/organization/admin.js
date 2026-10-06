/**
 * Organization Admin Shared UI & Controller
 */

const OrgAdmin = {
  renderSidebar(slug, activeSection = 'dashboard') {
    const target = document.getElementById('orgAdminSidebar');
    if (!target) return;

    const navItems = [
      { id: 'dashboard', label: 'Tổng quan (Dashboard)', icon: 'home', link: `/organizations/${slug}/admin` },
      { id: 'settings', label: 'Cài đặt Tổ chức', icon: 'settings', link: `/organizations/${slug}/admin/settings` },
      { id: 'members', label: 'Quản lý Thành viên', icon: 'users', link: `/organizations/${slug}/admin/members` },
      { id: 'roles', label: 'Vai trò & Cấp bậc', icon: 'shield', link: `/organizations/${slug}/admin/roles` },
      { id: 'permissions', label: 'Ma trận Phân quyền', icon: 'lock', link: `/organizations/${slug}/admin/permissions` },
      { id: 'contests', label: 'Gán & Quản lý Cuộc thi', icon: 'trophy', link: `/organizations/${slug}/admin/contests` },
      { id: 'problems', label: 'Gán & Quản lý Bài tập', icon: 'code', link: `/organizations/${slug}/admin/problems` },
      { id: 'blog', label: 'Bài viết / Blog', icon: 'file-text', link: `/organizations/${slug}/admin/blog` },
      { id: 'announcements', label: 'Thông báo Chính thức', icon: 'bell', link: `/organizations/${slug}/admin/announcements` },
      { id: 'invitations', label: 'Lời mời Thành viên', icon: 'mail', link: `/organizations/${slug}/admin/invitations` },
      { id: 'audit-log', label: 'Nhật ký Kiểm toán (Audit)', icon: 'activity', link: `/organizations/${slug}/admin/audit-log` }
    ];

    target.innerHTML = `
      <div class="org-admin-sidebar">
        <div class="org-admin-sidebar-title">Quản trị Tổ chức</div>
        ${navItems.map(item => `
          <a href="${item.link}" class="org-admin-nav-item ${activeSection === item.id ? 'active' : ''}">
            <cp-icon name="${item.icon}" size="sm"></cp-icon>
            <span>${item.label}</span>
          </a>
        `).join('')}

        <div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid #1e293b;">
          <a href="/organizations/${slug}" class="org-admin-nav-item" style="color:#60a5fa;">
            <cp-icon name="arrow-left" size="sm"></cp-icon>
            <span>&larr; Xem trang công khai</span>
          </a>
        </div>
      </div>
    `;
  }
};
