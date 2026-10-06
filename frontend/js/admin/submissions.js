/**
 * CodeProOJ - Admin Submission Operations
 */
const AdminSubmissions = {
  async rejudge(id) {
    if (!confirm(`Rejudge bài nộp #${id}?`)) return;
    try {
      const res = await fetch(`/api/v2/rejudge/${id}`, { method: 'POST' });
      const json = await res.json();
      alert(json.data?.message || 'Đã gửi lại bài vào máy chấm');
      window.location.reload();
    } catch (e) {
      alert('Lỗi: ' + e.message);
    }
  }
};

window.AdminSubmissions = AdminSubmissions;
