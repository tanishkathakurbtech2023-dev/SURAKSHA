const API_BASE = '/api';

function randomNonce() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

function getApiKey() {
  const input = document.getElementById('api-key');
  return input?.value?.trim() || localStorage.getItem('suraksha_api_key') || 'dev-api-key';
}

function showToast(message, type = 'ok') {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.className = `toast ${type}`;
  setTimeout(() => (toast.className = 'toast hidden'), 2800);
}

function setLoading(button, loading) {
  if (!button) return;
  if (loading) {
    button.dataset.prev = button.textContent;
    button.textContent = 'Please wait...';
    button.disabled = true;
  } else {
    button.textContent = button.dataset.prev || 'Submit';
    button.disabled = false;
  }
}

async function request(url, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    'X-API-Key': getApiKey(),
    ...(options.headers || {}),
  };

  const response = await fetch(url, { ...options, headers });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data?.detail || JSON.stringify(data));
  }
  return data;
}

function writeOutput(id, payload) {
  document.getElementById(id).textContent = JSON.stringify(payload, null, 2);
}

function updateKpis(summary) {
  document.getElementById('kpi-total').textContent = summary.total_transactions ?? 0;
  document.getElementById('kpi-flagged').textContent = summary.flagged_transactions ?? 0;
  document.getElementById('kpi-blocked').textContent = summary.blocked_transactions ?? 0;
  document.getElementById('kpi-chain').textContent = summary.chain_size ?? 0;
}

async function refreshHealth() {
  const chip = document.getElementById('health-chip');
  try {
    const health = await fetch('/health').then((r) => r.json());
    chip.textContent = `Backend: ${health.status} (${health.env || 'n/a'})`;
    chip.classList.add('ok');
  } catch {
    chip.textContent = 'Backend unreachable';
    chip.classList.add('bad');
  }
}

async function refreshSummary() {
  const summary = await request(`${API_BASE}/admin/summary`, { method: 'GET' });
  writeOutput('summary-output', summary);
  updateKpis(summary);
  return summary;
}

document.getElementById('save-key-btn').addEventListener('click', () => {
  const key = document.getElementById('api-key').value.trim();
  if (!key) {
    showToast('Enter a valid API key first.', 'err');
    return;
  }
  localStorage.setItem('suraksha_api_key', key);
  showToast('API key saved locally.', 'ok');
});

document.getElementById('risk-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const submitBtn = event.target.querySelector('button[type="submit"]');
  setLoading(submitBtn, true);

  const form = new FormData(event.target);
  const payload = {
    user_id: form.get('user_id'),
    amount: Number(form.get('amount')),
    device_trust: Number(form.get('device_trust')),
    network_risk: Number(form.get('network_risk')),
  };

  try {
    const result = await request(`${API_BASE}/auth/risk`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    writeOutput('risk-output', result);
    showToast('Risk score computed successfully.', 'ok');
  } catch (error) {
    writeOutput('risk-output', { error: error.message });
    showToast(`Risk scoring failed: ${error.message}`, 'err');
  } finally {
    setLoading(submitBtn, false);
  }
});

document.getElementById('txn-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const submitBtn = event.target.querySelector('button[type="submit"]');
  setLoading(submitBtn, true);

  const form = new FormData(event.target);
  const payload = {
    user_id: form.get('user_id'),
    txn_id: form.get('txn_id'),
    to_account: form.get('to_account'),
    amount: Number(form.get('amount')),
    device_trust: Number(form.get('device_trust')),
    network_risk: Number(form.get('network_risk')),
    nonce: randomNonce(),
  };

  try {
    const result = await request(`${API_BASE}/transactions/process`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    writeOutput('txn-output', result);
    await refreshSummary();
    const outcome = result.decision?.toUpperCase() || 'DONE';
    showToast(`Transaction ${outcome}: ${result.reason || 'processed'}`, result.decision === 'block' ? 'err' : 'ok');
  } catch (error) {
    writeOutput('txn-output', { error: error.message });
    showToast(`Transaction failed: ${error.message}`, 'err');
  } finally {
    setLoading(submitBtn, false);
  }
});

document.getElementById('summary-btn').addEventListener('click', async () => {
  try {
    await refreshSummary();
    showToast('Summary refreshed.', 'ok');
  } catch (error) {
    writeOutput('summary-output', { error: error.message });
    showToast(`Summary failed: ${error.message}`, 'err');
  }
});

(function boot() {
  const savedKey = localStorage.getItem('suraksha_api_key');
  if (savedKey) {
    document.getElementById('api-key').value = savedKey;
  }
  refreshHealth();
  refreshSummary().catch(() => {});
})();

document.getElementById('helpdesk-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const submitBtn = event.target.querySelector('button[type="submit"]');
  setLoading(submitBtn, true);
  const form = new FormData(event.target);
  try {
    const result = await request(`${API_BASE}/helpdesk/chat`, {
      method: 'POST',
      body: JSON.stringify({
        message: form.get('message'),
        language: form.get('language'),
      }),
    });
    writeOutput('helpdesk-output', result);
    showToast('Helpdesk response ready.', 'ok');
  } catch (error) {
    writeOutput('helpdesk-output', { error: error.message });
    showToast(`Helpdesk failed: ${error.message}`, 'err');
  } finally {
    setLoading(submitBtn, false);
  }
});

document.getElementById('report-btn').addEventListener('click', async () => {
  try {
    const result = await request(`${API_BASE}/admin/report`, { method: 'GET' });
    writeOutput('report-output', result);
    showToast('Report generated.', 'ok');
  } catch (error) {
    writeOutput('report-output', { error: error.message });
    showToast(`Report failed: ${error.message}`, 'err');
  }
});

document.getElementById('audit-query-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const submitBtn = event.target.querySelector('button[type="submit"]');
  setLoading(submitBtn, true);
  const form = new FormData(event.target);
  try {
    const result = await request(`${API_BASE}/admin/audit/query`, {
      method: 'POST',
      body: JSON.stringify({ query: form.get('query') }),
    });
    writeOutput('audit-query-output', result);
    showToast('Audit query complete.', 'ok');
  } catch (error) {
    writeOutput('audit-query-output', { error: error.message });
    showToast(`Audit query failed: ${error.message}`, 'err');
  } finally {
    setLoading(submitBtn, false);
  }
});

document.getElementById('behaviour-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const submitBtn = event.target.querySelector('button[type="submit"]');
  setLoading(submitBtn, true);
  const form = new FormData(event.target);
  const features = String(form.get('features'))
    .split(',')
    .map((v) => Number(v.trim()))
    .filter((v) => !Number.isNaN(v));

  try {
    const result = await request(`${API_BASE}/auth/behaviour`, {
      method: 'POST',
      body: JSON.stringify({ session_features: features }),
    });
    writeOutput('behaviour-output', result);
    showToast(`Trust score ${result.trust_score}`, result.reauth_required ? 'err' : 'ok');
  } catch (error) {
    writeOutput('behaviour-output', { error: error.message });
    showToast(`Behaviour profiling failed: ${error.message}`, 'err');
  } finally {
    setLoading(submitBtn, false);
  }
});
