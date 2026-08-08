/* FinIQ - Main Application Logic & Interactive State */

// Perform Login Action
function performLogin() {
  const loginScreen = document.getElementById('login-screen');
  if (loginScreen) {
    loginScreen.classList.add('fade-out');
    setTimeout(() => {
      loginScreen.style.display = 'none';
    }, 500);
  }
}

// Activate All Tokens Handler
function activateAllTokens() {
  const btn = document.getElementById('btn-activate-all');
  if (btn) {
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Activating All 8 Tokens...';
    btn.disabled = true;
  }

  state.tokens.forEach(t => t.status = 'Activated');

  setTimeout(() => {
    if (btn) {
      btn.innerHTML = '<i class="fa-solid fa-check"></i> All 8 Tokens Activated!';
      btn.style.background = 'linear-gradient(135deg, #059669, #047857)';
    }

    activateToken('TKN-90341');
  }, 700);
}

// Switch Executive Analytics Timeframe (Daily, Weekly, Monthly, Quarterly)
function setAnalyticsTimeframe(period, btnElement) {
  const parent = btnElement.parentElement;
  if (parent) {
    parent.querySelectorAll('.timeframe-btn').forEach(b => b.classList.remove('active'));
    btnElement.classList.add('active');
  }

  const kpiData = {
    daily: {
      conf: '94.2%', confSub: '<i class="fa-solid fa-arrow-up"></i> +0.4 pts vs yesterday',
      over: '6.8%', overSub: '<i class="fa-solid fa-arrow-down"></i> -0.8 pts vs yesterday',
      fraud: '₹8.4 Lakhs', fraudSub: '<i class="fa-solid fa-arrow-up"></i> +12.4% daily avg',
      runtime: '9.2s', runtimeSub: '<i class="fa-solid fa-arrow-down"></i> -0.9s faster',
      sla: '99.6% / 98.0%', acc: '97.1% / 95.0%', zt: '95.4% / 90.0%', cost: '₹1.8L / ₹1.5L'
    },
    weekly: {
      conf: '93.4%', confSub: '<i class="fa-solid fa-arrow-up"></i> +5.4 pts vs previous',
      over: '7.6%', overSub: '<i class="fa-solid fa-arrow-down"></i> -6.6 pts vs previous',
      fraud: '₹2.41 Cr', fraudSub: '<i class="fa-solid fa-arrow-up"></i> +18.2% vs target',
      runtime: '10.1s', runtimeSub: '<i class="fa-solid fa-arrow-down"></i> -2.4s faster',
      sla: '99.2% / 98.0%', acc: '96.4% / 95.0%', zt: '94.8% / 90.0%', cost: '₹42.8L / ₹38.0L'
    },
    monthly: {
      conf: '92.8%', confSub: '<i class="fa-solid fa-arrow-up"></i> +8.9 pts vs prev month',
      over: '8.4%', overSub: '<i class="fa-solid fa-arrow-down"></i> -10.1 pts vs prev month',
      fraud: '₹9.84 Cr', fraudSub: '<i class="fa-solid fa-arrow-up"></i> +24.5% MoM',
      runtime: '10.6s', runtimeSub: '<i class="fa-solid fa-arrow-down"></i> -3.1s faster',
      sla: '98.9% / 98.0%', acc: '95.8% / 95.0%', zt: '93.9% / 90.0%', cost: '₹1.82Cr / ₹1.50Cr'
    },
    quarterly: {
      conf: '91.5%', confSub: '<i class="fa-solid fa-arrow-up"></i> +14.2 pts QoQ',
      over: '9.2%', overSub: '<i class="fa-solid fa-arrow-down"></i> -14.9 pts QoQ',
      fraud: '₹28.5 Cr', fraudSub: '<i class="fa-solid fa-arrow-up"></i> +32.0% QoQ',
      runtime: '11.2s', runtimeSub: '<i class="fa-solid fa-arrow-down"></i> -4.2s faster',
      sla: '98.5% / 98.0%', acc: '95.2% / 95.0%', zt: '92.5% / 90.0%', cost: '₹5.40Cr / ₹4.80Cr'
    }
  };

  const d = kpiData[period] || kpiData['weekly'];

  const elConf = document.getElementById('kpi-confidence');
  const elConfSub = document.getElementById('kpi-confidence-sub');
  const elOver = document.getElementById('kpi-override');
  const elOverSub = document.getElementById('kpi-override-sub');
  const elFraud = document.getElementById('kpi-fraud-avoided');
  const elFraudSub = document.getElementById('kpi-fraud-sub');
  const elRun = document.getElementById('kpi-runtime');
  const elRunSub = document.getElementById('kpi-runtime-sub');

  if (elConf) elConf.innerText = d.conf;
  if (elConfSub) elConfSub.innerHTML = d.confSub;
  if (elOver) elOver.innerText = d.over;
  if (elOverSub) elOverSub.innerHTML = d.overSub;
  if (elFraud) elFraud.innerText = d.fraud;
  if (elFraudSub) elFraudSub.innerHTML = d.fraudSub;
  if (elRun) elRun.innerText = d.runtime;
  if (elRunSub) elRunSub.innerHTML = d.runtimeSub;

  const mSla = document.getElementById('meter-sla-val');
  const mAcc = document.getElementById('meter-acc-val');
  const mZt = document.getElementById('meter-zt-val');
  const mCost = document.getElementById('meter-cost-val');

  if (mSla) mSla.innerText = d.sla;
  if (mAcc) mAcc.innerText = d.acc;
  if (mZt) mZt.innerText = d.zt;
  if (mCost) mCost.innerText = d.cost;

  if (typeof initExecutiveCharts === 'function') {
    initExecutiveCharts(period);
  }
}

// State Store
const state = {
  activeView: 'dashboard-view',
  activeTokenId: 'TKN-90341',
  meshRunning: false,
  meshStep: 0,
  caseFilter: 'all',
  
  tokens: [
    { id: 'TKN-90341', name: 'Rhea Kapoor', custId: 'CUS-118342', type: 'Unauthorized Transaction', channel: 'Mobile App', amount: '₹48,250', priority: 'Critical', sla: '12m', status: 'Queued' },
    { id: 'TKN-90342', name: 'Devansh Rao', custId: 'CUS-118455', type: 'Duplicate Debit', channel: 'Net Banking', amount: '₹12,400', priority: 'High', sla: '24m', status: 'Queued' },
    { id: 'TKN-90343', name: 'Meera Iyer', custId: 'CUS-117901', type: 'Refund Not Received', channel: 'Contact Centre', amount: '₹5,800', priority: 'Normal', sla: '45m', status: 'Queued' },
    { id: 'TKN-90344', name: 'Kabir Sethi', custId: 'CUS-119220', type: 'Card Skimming Suspicion', channel: 'Branch', amount: '₹95,000', priority: 'Critical', sla: '8m', status: 'Queued' },
    { id: 'TKN-90345', name: 'Ananya Bose', custId: 'CUS-116088', type: 'Merchant Chargeback', channel: 'Email', amount: '₹22,100', priority: 'Normal', sla: '1h 10m', status: 'Queued' },
    { id: 'TKN-90346', name: 'Vikram Nair', custId: 'CUS-115730', type: 'UPI Failure Debit', channel: 'Mobile App', amount: '₹4,500', priority: 'Normal', sla: '1h 40m', status: 'Queued' },
    { id: 'TKN-90347', name: 'Simran Gill', custId: 'CUS-114402', type: 'Account Takeover Alert', channel: 'Risk Engine', amount: '₹1,50,000', priority: 'Critical', sla: '5m', status: 'Queued' },
    { id: 'TKN-90348', name: 'Rohan Deshpande', custId: 'CUS-113118', type: 'Subscription Overcharge', channel: 'Web Portal', amount: '₹3,200', priority: 'Low', sla: '2h 15m', status: 'Queued' }
  ],

  recentActivity: [
    { caseId: 'CASE-77092', name: 'Rhea Kapoor', type: 'Unauthorized Transaction', amount: '₹48,250', status: 'Refund Approved', confidence: '96%', time: '09:04 IST' },
    { caseId: 'CASE-77088', name: 'Devansh Rao', type: 'Duplicate Debit', amount: '₹12,400', status: 'Auto Reversal', confidence: '98%', time: '08:57 IST' },
    { caseId: 'CASE-77081', name: 'Ananya Bose', type: 'Merchant Chargeback', amount: '₹22,100', status: 'Claim Rejected', confidence: '91%', time: '08:41 IST' },
    { caseId: 'CASE-77075', name: 'Simran Gill', type: 'Account Takeover', amount: '₹1,50,000', status: 'Account Frozen', confidence: '99%', time: '08:26 IST' },
    { caseId: 'CASE-77069', name: 'Meera Iyer', type: 'Refund Not Received', amount: '₹5,800', status: 'Refund Approved', confidence: '94%', time: '08:12 IST' }
  ],

  approvals: [
    { caseId: 'CASE-77120', name: 'Rhea Kapoor', reason: 'Amount ₹48,250 > ₹25,000 autonomous ceiling', amount: '₹48,250', rec: 'Full Reversal', waitTime: '18m', sla: 'Breaching (3m left)' },
    { caseId: 'CASE-77118', name: 'Kabir Sethi', reason: 'High risk tier & card skimming alert', amount: '₹95,000', rec: 'Block & Reissue', waitTime: '14m', sla: 'Breaching (6m left)' },
    { caseId: 'CASE-77115', name: 'Simran Gill', reason: 'Account Freeze security action', amount: '₹1,50,000', rec: 'Freeze Account', waitTime: '11m', sla: 'Breaching (9m left)' },
    { caseId: 'CASE-77109', name: 'Priya Sharma', reason: 'Confidence score (82%) below threshold', amount: '₹18,900', rec: 'Manual Investigation', waitTime: '8m', sla: 'Normal' },
    { caseId: 'CASE-77104', name: 'Amitabh Sen', reason: 'Cross-border merchant discrepancy', amount: '₹34,000', rec: 'Partial Reversal', waitTime: '5m', sla: 'Normal' },
    { caseId: 'CASE-77098', name: 'Tanya Roy', reason: 'Repeated dispute within 30 days', amount: '₹8,500', rec: 'Reject & Escalate', waitTime: '2m', sla: 'Normal' }
  ],

  agents: [
    { id: 1, name: 'Agent 1 · Intelligent Case Intake', desc: 'Normalisation · Entity extraction · Severity scoring', status: 'completed', badge: '97% · llama-3.1-8b', text: 'Parsed 4 attachments, extracted 12 entities, classified as Tier-2 dispute.' },
    { id: 2, name: 'Agent 2 · Enterprise Context Retrieval', desc: 'Hybrid RAG over 1,284 governed documents', status: 'completed', badge: '95% · llama-3.3-70b', text: 'Retrieved 4 policy chunks across 4 sources (mean relevance 0.89).' },
    { id: 3, name: 'Agent 3 · Decision Intelligence', desc: 'Policy reasoning · Liability determination', status: 'completed', badge: '92% · llama-3.3-70b', text: 'Recommends full reversal of ₹48,250 under zero-liability provision.' },
    { id: 4, name: 'Agent 4 · Zero Trust Decision Validation', desc: 'Adversarial verification of recommendation', status: 'revised', badge: 'REVISE · Contradiction', text: 'Device fingerprint contradiction detected; single revision pass triggered.' },
    { id: 5, name: 'Agent 5 · Pre-Flight Shadow Simulation', desc: 'Predictive financial and retention impact', status: 'completed', badge: '90% · 10k simulations', text: 'Financial outflow ₹48,250 · retention gain 94% · net positive 3.1x.' },
    { id: 6, name: 'Agent 6 · Privacy Protection Engine', desc: 'Zero-knowledge tokenisation of PII', status: 'completed', badge: '100% · Deterministic', text: '9 PII fields tokenised. Zero raw identifiers leaked to trace.' },
    { id: 7, name: 'Agent 7 · Policy Guardrail', desc: 'Approval ceiling and mandate enforcement', status: 'completed', badge: '99% · Rules Engine', text: 'Amount ₹48,250 exceeds ₹25k ceiling — Manager Sign-off required.' },
    { id: 8, name: 'Agent 8 · Execution Orchestration', desc: 'Ledger orchestration · Audit commit', status: 'completed', badge: '99% · Orchestrator', text: 'Execution held pending Manager Approval. Audit entry committed.' }
  ],

  knowledgeDocs: [
    { name: 'Refund Policy v9.2.pdf', cat: 'Policy & SLA', chunks: '412', status: 'Indexed', date: '2026-08-05 02:10' },
    { name: 'RBI Master Direction — Digital Payments.pdf', cat: 'Regulatory Mandate', chunks: '366', status: 'Indexed', date: '2026-08-05 02:10' },
    { name: 'Fraud Investigation SOP.docx', cat: 'Standard Operating Procedure', chunks: '281', status: 'Indexed', date: '2026-08-05 02:10' },
    { name: 'Internal Compliance Manual 2026.pdf', cat: 'Governance & Ceilings', chunks: '205', status: 'Indexed', date: '2026-08-05 02:10' },
    { name: 'Chargeback Handling Guidelines.txt', cat: 'Card Network Rules', chunks: '132', status: 'Indexed', date: '2026-08-05 02:10' }
  ]
};

function showNotification(message, type = 'info') {
  let stack = document.getElementById('app-toast-stack');
  if (!stack) {
    stack = document.createElement('div');
    stack.id = 'app-toast-stack';
    stack.className = 'toast-stack';
    document.body.appendChild(stack);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<i class="fa-solid ${type === 'success' ? 'fa-circle-check' : type === 'error' ? 'fa-circle-exclamation' : 'fa-bell'}"></i> ${message}`;
  stack.appendChild(toast);

  window.setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-6px)';
    window.setTimeout(() => toast.remove(), 220);
  }, 2200);
}

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
  setupNavigation();
  renderDashboard();
  renderTokens();
  renderInvestigation();
  renderApprovals();
  renderCases();
  renderReports();
  renderKnowledge();
  setupModals();
  setupGlobalSearch();
  setupInteractiveComponents();
});

function setupInteractiveComponents() {
  const newDisputeBtn = document.getElementById('btn-new-dispute');
  if (newDisputeBtn) {
    newDisputeBtn.addEventListener('click', () => {
      switchView('tokens-view');
      showNotification('Opened the incoming token queue.', 'info');
    });
  }

  const saveSettingsBtn = document.getElementById('btn-save-settings');
  if (saveSettingsBtn) {
    saveSettingsBtn.addEventListener('click', () => {
      showNotification('Configuration saved and logged to the audit trail.', 'success');
    });
  }

  const uploadBtn = document.getElementById('btn-upload-document');
  if (uploadBtn) {
    let fileInput = document.getElementById('rag-file-input');
    if (!fileInput) {
      fileInput = document.createElement('input');
      fileInput.id = 'rag-file-input';
      fileInput.type = 'file';
      fileInput.accept = '.pdf,.docx,.txt';
      fileInput.style.display = 'none';
      document.body.appendChild(fileInput);
    }

    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => {
      const file = e.target.files && e.target.files[0];
      if (!file) return;

      state.knowledgeDocs.unshift({
        name: file.name,
        cat: 'Pending Upload',
        chunks: '—',
        status: 'Queued',
        date: 'Just now'
      });

      renderKnowledge();
      showNotification(`Document queued for indexing: ${file.name}`, 'success');
      fileInput.value = '';
    });
  }

  const tokenSelect = document.getElementById('select-active-token');
  if (tokenSelect) {
    tokenSelect.addEventListener('change', (e) => {
      const token = state.tokens.find(t => t.id === e.target.value);
      if (!token) return;
      state.activeTokenId = token.id;
      document.getElementById('inv-token-badge').innerText = `Token ${token.id}`;
      document.getElementById('inv-token-title').innerText = `${token.type} raised by ${token.name} for ${token.amount}`;
      document.getElementById('inv-cust-name').innerText = token.name;
      document.getElementById('inv-cust-id').innerText = token.custId;
      showNotification(`Loaded ${token.id} into the investigation workspace.`, 'info');
    });
  }

  document.querySelectorAll('.case-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      state.caseFilter = btn.getAttribute('data-filter') || 'all';
      document.querySelectorAll('.case-filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderCases();
    });
  });
}

// SPA Router & Navigation
function setupNavigation() {
  const navLinks = document.querySelectorAll('.nav-link, .nav-link-trigger');
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetView = link.getAttribute('data-view');
      if (targetView) {
        switchView(targetView);
      }
    });
  });
}

function switchView(viewId) {
  state.activeView = viewId;
  
  // Update view containers
  document.querySelectorAll('.view-container').forEach(view => {
    view.classList.remove('active');
  });
  const targetViewEl = document.getElementById(viewId);
  if (targetViewEl) {
    targetViewEl.classList.add('active');
  }

  // Update active sidebar nav link
  document.querySelectorAll('.sidebar .nav-link').forEach(link => {
    if (link.getAttribute('data-view') === viewId) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  // Update Header titles
  const titleMap = {
    'dashboard-view': { title: 'Operations Control Centre', bc: 'Enterprise Operational Overview' },
    'tokens-view': { title: 'Incoming Investigation Queue', bc: 'Queue Management & Activation' },
    'investigation-view': { title: 'AI Investigation Workspace', bc: 'Eight-Agent Mesh Real-time Sandbox' },
    'approvals-view': { title: 'Human Approval Queue', bc: 'Governance & Four-Eyes Control' },
    'cases-view': { title: 'Enterprise Case History', bc: 'Immutable Resolved Records' },
    'reports-view': { title: 'Signed Investigation Reports', bc: 'Exportable Compliance Records' },
    'knowledge-view': { title: 'Enterprise RAG Management', bc: 'Governed Policy Corpus & Vector Database' },
    'analytics-view': { title: 'Executive Reporting & Analytics', bc: 'Board-Level Operational Intelligence' },
    'settings-view': { title: 'Platform Settings & Governance', bc: 'Model, RAG & Privacy Vault Config' }
  };

  if (titleMap[viewId]) {
    document.getElementById('header-page-title').innerText = titleMap[viewId].title;
    document.getElementById('header-breadcrumb').innerText = titleMap[viewId].bc;
  }
}

// Render Dashboard
function renderDashboard() {
  const tbody = document.getElementById('recent-activity-tbody');
  if (!tbody) return;

  tbody.innerHTML = state.recentActivity.map(act => `
    <tr>
      <td><span class="token-id">${act.caseId}</span></td>
      <td style="font-weight: 600; color: var(--text-main);">${act.name}</td>
      <td>${act.type}</td>
      <td style="font-family: var(--font-mono);">${act.amount}</td>
      <td><span class="badge ${act.status.includes('Approved') || act.status.includes('Reversal') ? 'badge-success' : 'badge-danger'}">${act.status}</span></td>
      <td><span class="badge badge-cyan">${act.confidence}</span></td>
      <td style="font-size: 0.75rem; color: var(--text-dim);">${act.time}</td>
      <td><button class="btn btn-secondary btn-sm" onclick="openReportModal('${act.caseId}')">Report</button></td>
    </tr>
  `).join('');
}

// Render Incoming Tokens Queue
function renderTokens() {
  const container = document.getElementById('token-cards-container');
  if (!container) return;

  container.innerHTML = state.tokens.map(t => `
    <div class="token-card">
      <div class="token-card-header">
        <span class="token-id">${t.id}</span>
        <span class="badge ${t.priority === 'Critical' ? 'badge-danger' : 'badge-warning'}">${t.priority} · SLA ${t.sla}</span>
      </div>
      <div class="token-customer">${t.name}</div>
      <div style="font-size: 0.82rem; color: var(--text-muted); font-weight: 600; margin-bottom: 6px;">${t.type}</div>
      <div class="token-meta">
        <span><i class="fa-solid fa-id-card"></i> ${t.custId}</span>
        <span><i class="fa-solid fa-mobile-screen"></i> ${t.channel}</span>
        <span style="font-family: var(--font-mono); font-weight: 700; color: var(--text-main);">${t.amount}</span>
      </div>
      <div class="token-footer">
        <span style="font-size: 0.75rem; color: var(--text-dim);">Routed from Risk Engine</span>
        <button class="btn btn-primary btn-sm" onclick="activateToken('${t.id}')"><i class="fa-solid fa-bolt"></i> Activate</button>
      </div>
    </div>
  `).join('');
}

// Activate Token from Queue
function activateToken(tokenId) {
  state.activeTokenId = tokenId;
  const token = state.tokens.find(t => t.id === tokenId);
  if (token) {
    document.getElementById('inv-token-badge').innerText = `Token ${token.id}`;
    document.getElementById('inv-token-title').innerText = `${token.type} raised by ${token.name} for ${token.amount}`;
    document.getElementById('inv-cust-name').innerText = token.name;
    document.getElementById('inv-cust-id').innerText = token.custId;
  }
  switchView('investigation-view');
  runAgentMeshSimulation();
}

// Render AI Investigation Workspace
function renderInvestigation() {
  const container = document.getElementById('mesh-agents-container');
  if (!container) return;

  container.innerHTML = state.agents.map(a => `
    <div class="agent-step-card queued" id="agent-card-${a.id}">
      <div class="agent-info">
        <div class="agent-icon"><i class="fa-solid ${getAgentIcon(a.id)}"></i></div>
        <div>
          <div class="agent-name">${a.name}</div>
          <div class="agent-desc">${a.desc}</div>
          <div class="agent-body">Waiting for dispatch…</div>
        </div>
      </div>
      <div class="agent-status-badge">
        <span class="badge badge-cyan">Queued</span>
      </div>
    </div>
  `).join('');

  // Mesh Action Triggers
  const runBtn = document.getElementById('btn-run-mesh');
  if (runBtn) {
    runBtn.addEventListener('click', () => runAgentMeshSimulation());
  }

  const reqBtn = document.getElementById('btn-request-approval');
  if (reqBtn) {
    reqBtn.addEventListener('click', () => openApprovalModal('CASE-77120'));
  }

  const expBtn = document.getElementById('btn-export-report');
  if (expBtn) {
    expBtn.addEventListener('click', () => openReportModal('CASE-77092'));
  }
}

function getAgentIcon(id) {
  const icons = {
    1: 'fa-inbox',
    2: 'fa-database',
    3: 'fa-brain',
    4: 'fa-shield-halved',
    5: 'fa-chart-pie',
    6: 'fa-user-lock',
    7: 'fa-scale-balanced',
    8: 'fa-check-double'
  };
  return icons[id] || 'fa-microchip';
}

function getAgentRuntimeText(agent, phase) {
  const runtimeMap = {
    1: {
      active: 'Scanning incoming evidence bundle…',
      done: 'Parsed 4 attachments and extracted 12 entities.'
    },
    2: {
      active: 'Retrieving governed policy context…',
      done: 'Retrieved 4 policy chunks with 0.89 relevance.'
    },
    3: {
      active: 'Evaluating liability against policy logic…',
      done: 'Recommendation generated with 92% calibrated confidence.'
    },
    4: {
      active: 'Validating zero-trust assumptions…',
      done: 'Contradiction detected; revision pass triggered.'
    },
    5: {
      active: 'Simulating downstream financial impact…',
      done: 'Projected retention uplift and financial exposure.'
    },
    6: {
      active: 'Applying privacy tokenization controls…',
      done: 'PII redaction completed with zero raw leakage.'
    },
    7: {
      active: 'Enforcing approval ceiling and guardrails…',
      done: 'Guardrail review completed and manager approval required.'
    },
    8: {
      active: 'Committing audit-ready execution record…',
      done: 'Execution log committed and case state locked.'
    }
  };

  const choice = runtimeMap[agent.id] || { active: 'Processing decision signals…', done: 'Execution cycle completed.' };
  return phase === 'active' ? choice.active : choice.done;
}

function getAgentDuration(agent) {
  const durations = {
    1: 3200,
    2: 45000,
    3: 7800,
    4: 13200,
    5: 9600,
    6: 5400,
    7: 8600,
    8: 4700
  };

  return durations[agent.id] || 6000;
}

function setAgentCardState(agentId, stateName, detailText, badgeText, badgeClass) {
  const card = document.getElementById(`agent-card-${agentId}`);
  if (!card) return;

  const body = card.querySelector('.agent-body');
  const badge = card.querySelector('.agent-status-badge .badge');

  card.className = `agent-step-card ${stateName}`;
  if (stateName === 'active') {
    card.classList.add('pulse-glow');
  }

  if (body) {
    body.innerHTML = detailText;
  }

  if (badge) {
    badge.className = `badge ${badgeClass}`;
    badge.innerText = badgeText;
  }
}

// Run Agent Mesh Step-by-Step Simulation
function runAgentMeshSimulation() {
  const execBadge = document.getElementById('mesh-exec-status');
  const container = document.getElementById('mesh-agents-container');

  if (execBadge) {
    execBadge.innerText = 'FinIQ Mesh v4 · Dispatching…';
    execBadge.className = 'badge badge-warning pulse-glow';
  }

  if (container) {
    container.classList.add('simulating');
  }

  state.agents.forEach(agent => {
    setAgentCardState(agent.id, 'queued', 'Waiting for dispatch…', 'Queued', 'badge-cyan');
  });

  let currentIndex = 0;

  const playNext = () => {
    if (currentIndex >= state.agents.length) {
      if (execBadge) {
        execBadge.innerText = 'FinIQ Mesh v4 · Complete';
        execBadge.className = 'badge badge-success';
      }
      if (container) {
        container.classList.remove('simulating');
      }
      return;
    }

    const agent = state.agents[currentIndex];
    setAgentCardState(
      agent.id,
      'active',
      `<i class="fa-solid fa-spinner fa-spin"></i> ${getAgentRuntimeText(agent, 'active')}`,
      'Running…',
      'badge-warning'
    );

    const activeDuration = getAgentDuration(agent);

    window.setTimeout(() => {
      const completedState = agent.id === 4 ? 'revised' : 'completed';
      const badgeClass = agent.id === 4 ? 'badge-warning' : 'badge-success';
      const badgeText = agent.id === 4 ? 'Revised' : 'Completed';

      setAgentCardState(
        agent.id,
        completedState,
        getAgentRuntimeText(agent, 'done'),
        badgeText,
        badgeClass
      );

      currentIndex += 1;
      window.setTimeout(playNext, 450);
    }, activeDuration);
  };

  playNext();
}

// Render Approvals Queue
function renderApprovals() {
  const tbody = document.getElementById('approvals-tbody');
  if (!tbody) return;

  tbody.innerHTML = state.approvals.map(app => `
    <tr>
      <td><span class="token-id">${app.caseId}</span></td>
      <td style="font-weight: 600; color: var(--text-main);">${app.name}</td>
      <td style="font-size: 0.8rem; color: var(--text-muted);">${app.reason}</td>
      <td style="font-family: var(--font-mono); font-weight: 700;">${app.amount}</td>
      <td><span class="badge badge-cyan">${app.rec}</span></td>
      <td>${app.waitTime}</td>
      <td><button class="btn btn-primary btn-sm" onclick="openApprovalModal('${app.caseId}')"><i class="fa-solid fa-signature"></i> Review</button></td>
    </tr>
  `).join('');
}

// Render Case History
function renderCases() {
  const tbody = document.getElementById('cases-tbody');
  if (!tbody) return;

  const sampleCases = [
    { id: 'CASE-77092', cust: 'Rhea Kapoor', type: 'Unauthorized Transaction', dec: 'Refund Approved', exec: 'Autonomous (AI)', runtime: '10.1s', date: '2026-08-07 09:04' },
    { id: 'CASE-77088', cust: 'Devansh Rao', type: 'Duplicate Debit', dec: 'Auto Reversal', exec: 'Autonomous (AI)', runtime: '8.4s', date: '2026-08-07 08:57' },
    { id: 'CASE-77081', cust: 'Ananya Bose', type: 'Merchant Chargeback', dec: 'Claim Rejected', exec: 'Autonomous (AI)', runtime: '11.2s', date: '2026-08-07 08:41' },
    { id: 'CASE-77075', cust: 'Simran Gill', type: 'Account Takeover', dec: 'Account Frozen', exec: 'Human Approved', runtime: '14.5s', date: '2026-08-07 08:26' },
    { id: 'CASE-77069', cust: 'Meera Iyer', type: 'Refund Not Received', dec: 'Refund Approved', exec: 'Autonomous (AI)', runtime: '9.0s', date: '2026-08-07 08:12' },
    { id: 'CASE-77061', cust: 'Vikram Nair', type: 'UPI Failure Debit', dec: 'Refund Approved', exec: 'Autonomous (AI)', runtime: '7.8s', date: '2026-08-06 19:44' },
    { id: 'CASE-77054', cust: 'Rohan Deshpande', type: 'Subscription Overcharge', dec: 'Partial Refund', exec: 'Human Approved', runtime: '12.1s', date: '2026-08-06 18:20' },
    { id: 'CASE-77048', cust: 'Kabir Sethi', type: 'Card Skimming', dec: 'Card Blocked', exec: 'Human Approved', runtime: '13.0s', date: '2026-08-06 17:02' }
  ];

  const visibleCases = sampleCases.filter(c => {
    if (state.caseFilter === 'autonomous') return c.exec.includes('Autonomous');
    if (state.caseFilter === 'manager') return c.exec.includes('Human');
    if (state.caseFilter === 'rejected') return c.dec.includes('Rejected');
    return true;
  });

  tbody.innerHTML = visibleCases.map(c => `
    <tr>
      <td><span class="token-id">${c.id}</span></td>
      <td style="font-weight: 600; color: var(--text-main);">${c.cust}</td>
      <td>${c.type}</td>
      <td><span class="badge ${c.dec.includes('Approved') || c.dec.includes('Reversal') ? 'badge-success' : 'badge-purple'}">${c.dec}</span></td>
      <td><span class="badge badge-cyan">${c.exec}</span></td>
      <td style="font-family: var(--font-mono);">${c.runtime}</td>
      <td style="font-size: 0.75rem; color: var(--text-dim);">${c.date}</td>
      <td><button class="btn btn-secondary btn-sm" onclick="openReportModal('${c.id}')"><i class="fa-solid fa-file-lines"></i> Open</button></td>
    </tr>
  `).join('');
}

// Render Reports
function renderReports() {
  const container = document.getElementById('reports-grid-container');
  if (!container) return;

  const reports = [
    { id: 'CASE-77092', title: 'Rhea Kapoor · Unauthorized Transaction', outcome: 'Refund Approved', date: '2026-08-07 09:04' },
    { id: 'CASE-77088', title: 'Devansh Rao · Duplicate Debit', outcome: 'Auto Reversal', date: '2026-08-07 08:57' },
    { id: 'CASE-77081', title: 'Ananya Bose · Merchant Chargeback', outcome: 'Claim Rejected', date: '2026-08-07 08:41' },
    { id: 'CASE-77075', title: 'Simran Gill · Account Takeover', outcome: 'Account Frozen', date: '2026-08-07 08:26' },
    { id: 'CASE-77069', title: 'Meera Iyer · Refund Not Received', outcome: 'Refund Approved', date: '2026-08-07 08:12' },
    { id: 'CASE-77061', title: 'Vikram Nair · UPI Failure Debit', outcome: 'Refund Approved', date: '2026-08-06 19:44' },
    { id: 'CASE-77054', title: 'Rohan Deshpande · Subscription Overcharge', outcome: 'Partial Refund', date: '2026-08-06 18:20' },
    { id: 'CASE-77048', title: 'Kabir Sethi · Card Skimming', outcome: 'Card Blocked', date: '2026-08-06 17:02' }
  ];

  container.innerHTML = reports.map(r => `
    <div class="token-card">
      <div class="token-card-header">
        <span class="token-id">${r.id}</span>
        <span class="badge badge-success">${r.outcome}</span>
      </div>
      <div style="font-weight: 700; color: var(--text-main); margin-bottom: 6px;">${r.title}</div>
      <div style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 12px;">Completed: ${r.date}</div>
      <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 10px;">
        <span style="font-size: 0.72rem; color: var(--status-success);"><i class="fa-solid fa-lock"></i> Digitally Signed</span>
        <button class="btn btn-secondary btn-sm" onclick="openReportModal('${r.id}')"><i class="fa-solid fa-eye"></i> View Report</button>
      </div>
    </div>
  `).join('');
}

// Render Knowledge Base (RAG)
function renderKnowledge() {
  const tbody = document.getElementById('knowledge-tbody');
  if (!tbody) return;

  const docs = state.knowledgeDocs || [];

  tbody.innerHTML = docs.map(d => `
    <tr>
      <td style="font-weight: 700; color: var(--primary-cyan);"><i class="fa-regular fa-file-pdf"></i> ${d.name}</td>
      <td>${d.cat}</td>
      <td style="font-family: var(--font-mono);">${d.chunks}</td>
      <td><span class="badge badge-success">${d.status}</span></td>
      <td style="font-size: 0.75rem; color: var(--text-dim);">${d.date}</td>
      <td>
        <button class="btn btn-secondary btn-sm" onclick="reindexKnowledgeDocument('${d.name}')"><i class="fa-solid fa-rotate"></i> Re-index</button>
      </td>
    </tr>
  `).join('');
}

function reindexKnowledgeDocument(docName) {
  const doc = state.knowledgeDocs.find(d => d.name === docName);
  if (!doc) return;

  doc.status = 'Re-indexed';
  doc.date = 'Just now';
  renderKnowledge();
  showNotification(`Re-index requested for ${docName}.`, 'success');
}

// Modal Handlers
function setupModals() {
  document.querySelectorAll('.modal-close').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active'));
    });
  });

  document.querySelectorAll('.modal-overlay').forEach(m => {
    m.addEventListener('click', (e) => {
      if (e.target === m) m.classList.remove('active');
    });
  });
}

function openApprovalModal(caseId) {
  const modal = document.getElementById('approval-modal');
  const title = document.getElementById('modal-approval-title');
  const body = document.getElementById('modal-approval-body');
  
  if (!modal || !body) return;

  title.innerText = `Approval Review — ${caseId}`;
  body.innerHTML = `
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
      <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 10px; border: 1px solid var(--border-color);">
        <div style="font-weight: 700; color: var(--text-main); margin-bottom: 8px;">Customer Profile</div>
        <div style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;">
          <strong>Name:</strong> Rhea Kapoor (CUS-118342)<br>
          <strong>Segment:</strong> Priority Banking<br>
          <strong>KYC:</strong> Verified — Full KYC<br>
          <strong>Risk Score:</strong> Low (12/100)<br>
          <strong>Lifetime Value:</strong> ₹18.4 Lakhs
        </div>
      </div>

      <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 10px; border: 1px solid var(--border-color);">
        <div style="font-weight: 700; color: var(--text-main); margin-bottom: 8px;">AI Recommendation</div>
        <div style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;">
          <strong>Action:</strong> Full reversal of ₹48,250.00<br>
          <strong>Clause:</strong> RBI Master Direction 9(c)<br>
          <strong>Guardrail:</strong> Exceeds ₹25k autonomous ceiling<br>
          <strong>Confidence:</strong> 92% (Calibrated)<br>
          <strong>Zero Trust:</strong> 6 checks passed (1 revision)
        </div>
      </div>
    </div>

    <div style="margin-bottom: 20px;">
      <div class="form-label">Manager Authorization Notes</div>
      <textarea class="form-control" rows="3" placeholder="Enter approval rationale or governance notes for the immutable log...">Reversal authorized under zero-liability provision. Device mismatch verified as roaming session. Capped SLA met.</textarea>
    </div>

    <div style="display: flex; gap: 12px; justify-content: flex-end;">
      <button class="btn btn-secondary" onclick="closeModal('approval-modal')">Cancel</button>
      <button class="btn btn-danger" onclick="actionApprove('Reject', '${caseId}')"><i class="fa-solid fa-xmark"></i> Reject Claim</button>
      <button class="btn btn-success" onclick="actionApprove('Approve', '${caseId}')"><i class="fa-solid fa-check"></i> Approve Reversal (₹48,250)</button>
    </div>
  `;

  modal.classList.add('active');
}

function actionApprove(type, caseId) {
  alert(`Action Executed: Case ${caseId} ${type}d! Written to audit log.`);
  closeModal('approval-modal');
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove('active');
}

function openReportModal(caseId) {
  const modal = document.getElementById('report-modal');
  const body = document.getElementById('modal-report-body');
  if (!modal || !body) return;

  body.innerHTML = `
    <div style="background: rgba(15, 23, 42, 0.9); padding: 24px; border-radius: 12px; border: 1px solid var(--border-highlight); font-family: var(--font-sans);">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--border-color); padding-bottom: 14px; margin-bottom: 18px;">
        <div>
          <h2 style="font-size: 1.2rem; color: #FFF;">FinIQ Enterprise Investigation Report</h2>
          <div style="font-size: 0.78rem; color: var(--primary-cyan);">Case ID: ${caseId} · Signed & Sealed Record</div>
        </div>
        <div style="text-align: right;">
          <span class="badge badge-success" style="font-size: 0.85rem;">STATUS: EXECUTED</span>
          <div style="font-size: 0.72rem; color: var(--text-dim); margin-top: 4px;">Timestamp: 2026-08-07 09:04:12 IST</div>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 18px; font-size: 0.82rem;">
        <div>
          <div style="color: var(--text-dim);">Complainant Details:</div>
          <div style="color: #FFF; font-weight: 700;">Rhea Kapoor (CUS-118342)</div>
          <div style="color: var(--text-muted);">Priority Banking · Verified Full KYC</div>
        </div>
        <div>
          <div style="color: var(--text-dim);">Disputed Instrument:</div>
          <div style="color: #FFF; font-weight: 700;">Visa Platinum ···· 4821</div>
          <div style="color: var(--text-muted);">Amount: ₹48,250.00 (USD 578.40)</div>
        </div>
      </div>

      <div style="margin-bottom: 18px;">
        <div style="font-weight: 700; color: var(--primary-cyan); font-size: 0.88rem; margin-bottom: 8px;">Zero-Knowledge PII Tokenization Matrix</div>
        <table class="custom-table" style="font-size: 0.78rem;">
          <thead>
            <tr><th>Raw Field</th><th>PII Mask</th><th>Zero-Knowledge Vault Token</th></tr>
          </thead>
          <tbody>
            <tr><td>Customer Name</td><td>Rhea Kapoor</td><td><span class="code-box">USER_ALPHA_91</span></td></tr>
            <tr><td>PAN Card</td><td>AXQPK••••M</td><td><span class="code-box">PAN_HASH_01</span></td></tr>
            <tr><td>Account No</td><td>XXXX XXXX 4821</td><td><span class="code-box">ACC_TOKEN_91</span></td></tr>
            <tr><td>Mobile</td><td>+91 98••••2210</td><td><span class="code-box">MSISDN_TOKEN_44</span></td></tr>
          </tbody>
        </table>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 14px; margin-top: 20px;">
        <div style="font-size: 0.75rem; color: var(--text-dim);">
          Authorised Signatory: <strong>Aarav Menon</strong> (Operations Manager · EMP-40921)
        </div>
        <button class="btn btn-primary btn-sm" onclick="window.print()"><i class="fa-solid fa-print"></i> Print / Export PDF</button>
      </div>
    </div>
  `;

  modal.classList.add('active');
}

// Global Search
function setupGlobalSearch() {
  const searchInput = document.getElementById('global-search');
  if (!searchInput) return;

  searchInput.addEventListener('input', (e) => {
    const val = e.target.value.toLowerCase();
    if (!val) return;

    // Search matches tokens or cases
    const matchToken = state.tokens.find(t => t.id.toLowerCase().includes(val) || t.name.toLowerCase().includes(val));
    if (matchToken) {
      activateToken(matchToken.id);
    }
  });
}
