(function () {
  'use strict';
  const contestKey = ContestAdminAPI.getContestKey();
  const api = (path, options) => ContestAdminAPI.antiCheat(contestKey, path, options);
  const byId = id => document.getElementById(id);
  let activeCase = null;

  ContestAdminUI.renderSidebar('anti-cheat', contestKey);
  ContestAdminUI.renderHeader('Chống gian lận', 'Quét bài nộp, xem bằng chứng và xử lý hồ sơ nghi vấn');

  function notice(message, kind = '') {
    byId('acNotice').textContent = message;
    byId('acNotice').dataset.kind = kind;
  }

  function cell(row, value) {
    const td = row.insertCell();
    td.textContent = value === null || value === undefined ? '—' : String(value);
    return td;
  }

  function badge(row, status) {
    const td = row.insertCell();
    const span = document.createElement('span');
    span.className = 'ac-badge';
    span.dataset.status = status;
    span.textContent = status;
    td.appendChild(span);
  }

  function action(row, label, handler) {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = label;
    button.addEventListener('click', handler);
    row.insertCell().appendChild(button);
  }

  function emptyRows(tbody, columns, message) {
    const row = tbody.insertRow();
    const td = row.insertCell();
    td.colSpan = columns;
    td.textContent = message;
  }

  async function loadDashboard() {
    const data = await api('/dashboard');
    byId('acScans').textContent = data.scans;
    byId('acPending').textContent = data.pending_scans;
    byId('acOpen').textContent = data.open_cases;
    byId('acConfirmed').textContent = data.confirmed_cases;
    const latest = data.latest_scan;
    byId('acScanStatus').textContent = latest
      ? `Lượt mới nhất #${latest.id}: ${latest.status} · ${latest.processed}/${latest.total} bài · ${latest.matches} cặp nghi vấn`
      : 'Chưa có lượt quét nào.';
  }

  async function loadScans() {
    const data = await api('/scans');
    const tbody = byId('acScanRows');
    tbody.replaceChildren();
    if (!data.scans.length) return emptyRows(tbody, 7, 'Chưa có lượt quét.');
    for (const scan of data.scans) {
      const row = tbody.insertRow();
      cell(row, `#${scan.id}`);
      cell(row, scan.target_submission ? `Bài nộp #${scan.target_submission}` : 'Toàn bộ kỳ thi');
      badge(row, scan.status);
      cell(row, `${scan.processed}/${scan.total}`);
      cell(row, scan.matches);
      cell(row, new Date(scan.created_at).toLocaleString('vi-VN'));
      if (scan.status === 'FAILED') {
        action(row, 'Thử lại', async () => {
          try {
            await api(`/scans/${scan.id}/retry`, { method: 'POST', body: '{}' });
            notice('Đã xếp lại lượt quét.', 'success');
            await refresh();
          } catch (error) { notice(error.message, 'error'); }
        });
      } else cell(row, scan.error || '');
    }
  }

  async function loadCases() {
    const status = byId('acCaseFilter').value;
    const data = await api(`/cases${status ? `?status=${encodeURIComponent(status)}` : ''}`);
    const tbody = byId('acCaseRows');
    tbody.replaceChildren();
    if (!data.cases.length) return emptyRows(tbody, 7, 'Chưa có hồ sơ nghi vấn.');
    for (const item of data.cases) {
      const row = tbody.insertRow();
      cell(row, `#${item.id}`);
      cell(row, item.problem);
      cell(row, `${item.user_a} · ${item.user_b}`);
      cell(row, `${item.score.toFixed(2)}%`);
      badge(row, item.status);
      cell(row, new Date(item.created_at).toLocaleString('vi-VN'));
      action(row, 'Xem bằng chứng', () => openEvidence(item));
    }
  }

  async function openEvidence(item) {
    try {
      const data = await api(`/cases/${item.id}/evidence`);
      activeCase = data.case;
      byId('acEvidenceTitle').textContent = `Hồ sơ #${item.id} · ${item.problem} · ${item.score.toFixed(2)}%`;
      byId('acEvidenceMeta').textContent = `Thuật toán ${item.algorithm_version}; fingerprint chung: ${data.evidence.common_fingerprints}. ${data.source_unchanged ? 'Mã nguồn khớp bản đã quét.' : 'Mã nguồn đã thay đổi; cần quét lại.'}`;
      byId('acSourceAHeading').textContent = `${item.user_a} · bài nộp #${item.submission_a}`;
      byId('acSourceBHeading').textContent = `${item.user_b} · bài nộp #${item.submission_b}`;
      byId('acSourceA').textContent = data.source_a;
      byId('acSourceB').textContent = data.source_b;
      byId('acDecisionReason').value = '';
      const canDecide = ['OPEN', 'UNDER_REVIEW'].includes(item.status);
      byId('acConfirm').hidden = !canDecide;
      byId('acDismiss').hidden = !canDecide;
      byId('acPenaltySection').hidden = item.status !== 'CONFIRMED';
      const users = byId('acPenaltyUser');
      users.replaceChildren();
      for (const [id, name] of [[item.user_a_id, item.user_a], [item.user_b_id, item.user_b]]) {
        const option = document.createElement('option');
        option.value = String(id);
        option.textContent = name;
        users.appendChild(option);
      }
      byId('acEvidenceDialog').showModal();
    } catch (error) { notice(error.message, 'error'); }
  }

  async function decide(actionName) {
    if (!activeCase) return;
    const reason = byId('acDecisionReason').value.trim();
    if (reason.length < 10) return notice('Hãy ghi lý do ít nhất 10 ký tự.', 'error');
    try {
      await api(`/cases/${activeCase.id}/${actionName}`, { method: 'POST', body: JSON.stringify({ reason }) });
      byId('acEvidenceDialog').close();
      notice('Đã ghi quyết định và nhật ký kiểm toán.', 'success');
      await refresh();
    } catch (error) { notice(error.message, 'error'); }
  }

  async function issuePenalty() {
    if (!activeCase) return;
    const reason = byId('acDecisionReason').value.trim();
    if (reason.length < 10) return notice('Hãy ghi lý do xử lý ít nhất 10 ký tự.', 'error');
    try {
      await api(`/cases/${activeCase.id}/penalties`, { method: 'POST', body: JSON.stringify({
        kind: byId('acPenaltyKind').value, user_id: Number(byId('acPenaltyUser').value), reason
      }) });
      byId('acEvidenceDialog').close();
      notice('Đã ghi quyết định xử lý. Thí sinh có quyền khiếu nại.', 'success');
      await refresh();
    } catch (error) { notice(error.message, 'error'); }
  }

  async function loadSettings() {
    const data = await api('/settings');
    byId('acEnabled').checked = data.enabled;
    byId('acThreshold').value = data.similarity_threshold;
    byId('acMinTokens').value = data.min_tokens;
    byId('acScanMode').value = data.scan_mode;
  }

  async function loadAppeals() {
    const data = await api('/appeals');
    const tbody = byId('acAppealRows');
    tbody.replaceChildren();
    if (!data.appeals.length) return emptyRows(tbody, 6, 'Chưa có khiếu nại.');
    for (const item of data.appeals) {
      const row = tbody.insertRow();
      cell(row, `#${item.id}`);
      cell(row, `#${item.case_id}`);
      cell(row, item.appellant);
      cell(row, item.reason);
      badge(row, item.status);
      if (item.status !== 'OPEN') { cell(row, item.decision); continue; }
      const td = row.insertCell();
      for (const [label, decision] of [['Chấp nhận', 'UPHELD'], ['Bác bỏ', 'REJECTED']]) {
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = label;
        button.addEventListener('click', async () => {
          const explanation = window.prompt(`Giải thích quyết định ${label.toLowerCase()} khiếu nại #${item.id}:`);
          if (!explanation) return;
          try {
            const result = await api(`/appeals/${item.id}/resolve`, { method: 'POST', body: JSON.stringify({ decision, explanation }) });
            notice(result.manual_reinstatement_required
              ? 'Đã chấp nhận khiếu nại. Hãy khôi phục tư cách thi đấu trong mục Thí sinh; hệ thống giữ nguyên các quyết định kỷ luật khác.'
              : 'Đã xử lý khiếu nại.', 'success');
            await refresh();
          } catch (error) { notice(error.message, 'error'); }
        });
        td.appendChild(button);
      }
    }
  }

  async function refresh() {
    try { await Promise.all([loadDashboard(), loadScans(), loadCases(), loadAppeals()]); }
    catch (error) { notice(`Không tải được dữ liệu: ${error.message}`, 'error'); }
  }

  byId('acRefresh').addEventListener('click', refresh);
  byId('acCaseFilter').addEventListener('change', loadCases);
  byId('acStartScan').addEventListener('click', async () => {
    try {
      await api('/scans', { method: 'POST', body: '{}' });
      notice('Đã xếp lượt quét toàn bộ kỳ thi.', 'success');
      await refresh();
    } catch (error) { notice(error.message, 'error'); }
  });
  byId('acSettingsForm').addEventListener('submit', async event => {
    event.preventDefault();
    try {
      await api('/settings', { method: 'PATCH', body: JSON.stringify({
        enabled: byId('acEnabled').checked,
        similarity_threshold: Number(byId('acThreshold').value),
        min_tokens: Number(byId('acMinTokens').value),
        scan_mode: byId('acScanMode').value,
      }) });
      notice('Đã lưu chính sách quét.', 'success');
      await refresh();
    } catch (error) { notice(error.message, 'error'); }
  });
  byId('acCloseDialog').addEventListener('click', () => byId('acEvidenceDialog').close());
  byId('acConfirm').addEventListener('click', () => decide('confirm'));
  byId('acDismiss').addEventListener('click', () => decide('dismiss'));
  byId('acIssuePenalty').addEventListener('click', issuePenalty);
  loadSettings().catch(error => notice(error.message, 'error'));
  refresh();
  setInterval(() => { if (!byId('acEvidenceDialog').open) refresh(); }, 10000);
})();
