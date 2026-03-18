/**
 * Skill Track — Shared JS Utilities & API Client
 */

const API_BASE = 'http://localhost:5000/api';

// ── Token Management ─────────────────────────────────
const Auth = {
  getToken: () => localStorage.getItem('st_token'),
  getUser:  () => JSON.parse(localStorage.getItem('st_user') || 'null'),
  setSession: (token, user) => {
    localStorage.setItem('st_token', token);
    localStorage.setItem('st_user', JSON.stringify(user));
  },
  clear: () => {
    localStorage.removeItem('st_token');
    localStorage.removeItem('st_user');
  },
  isLoggedIn: () => !!localStorage.getItem('st_token'),
  requireAuth: () => {
    if (!Auth.isLoggedIn()) {
      window.location.href = '/frontend/html/login.html';
      return false;
    }
    return true;
  }
};

// ── API Client ───────────────────────────────────────
const api = {
  async request(method, endpoint, data = null) {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' }
    };
    const token = Auth.getToken();
    if (token) opts.headers['Authorization'] = `Bearer ${token}`;
    if (data) opts.body = JSON.stringify(data);

    try {
      const res = await fetch(API_BASE + endpoint, opts);
      const json = await res.json();
      if (!res.ok) throw new Error(json.error || `HTTP ${res.status}`);
      return json;
    } catch (err) {
      if (err.message.includes('401')) {
        Auth.clear();
        window.location.href = '/frontend/html/login.html';
      }
      throw err;
    }
  },
  get:    (ep)       => api.request('GET',    ep),
  post:   (ep, data) => api.request('POST',   ep, data),
  put:    (ep, data) => api.request('PUT',    ep, data),
  delete: (ep)       => api.request('DELETE', ep),
};

// ── Toast ────────────────────────────────────────────
function toast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const t = document.createElement('div');
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  t.className = `toast ${type}`;
  t.innerHTML = `<span>${icons[type]||'·'}</span><span>${message}</span>`;
  container.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

// ── Modal helpers ─────────────────────────────────────
function openModal(id) {
  document.getElementById(id)?.classList.add('open');
}
function closeModal(id) {
  document.getElementById(id)?.classList.remove('open');
}

// ── Sidebar active link ───────────────────────────────
function setActiveNav() {
  const current = window.location.pathname.split('/').pop();
  document.querySelectorAll('.nav-item').forEach(el => {
    el.classList.toggle('active', el.getAttribute('href') === current || el.dataset.page === current);
  });
}

// ── Render user info in sidebar ───────────────────────
function renderUserChip() {
  const user = Auth.getUser();
  if (!user) return;
  const nameEl = document.querySelector('.user-chip .name');
  const roleEl = document.querySelector('.user-chip .role');
  const avatarEl = document.querySelector('.user-chip .avatar');
  if (nameEl) nameEl.textContent = user.username || user.email;
  if (roleEl) roleEl.textContent = user.role;
  if (avatarEl) avatarEl.textContent = (user.username || user.email)[0].toUpperCase();
}

// ── Format date ───────────────────────────────────────
function fmtDate(d) {
  if (!d) return '—';
  return new Date(d).toLocaleDateString('en-IN', { day:'2-digit', month:'short', year:'numeric' });
}

function fmtDateTime(d) {
  if (!d) return '—';
  return new Date(d).toLocaleString('en-IN', { day:'2-digit', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' });
}

// ── Badge helper ──────────────────────────────────────
function statusBadge(status) {
  const map = {
    Active:'green', Ongoing:'green', Present:'green', Pass:'green', Paid:'green', Completed:'green', Converted:'green', Selected:'green',
    Inactive:'gray', Archived:'gray', Upcoming:'gray',
    Absent:'red', Fail:'red', Overdue:'red', Lost:'red', Rejected:'red', Dropped:'red', Cancelled:'red',
    Pending:'yellow', 'In Progress':'yellow', Interested:'yellow', 'Follow-up':'yellow', Scheduled:'yellow', Partial:'yellow', Applied:'yellow',
    Late:'yellow', Leave:'purple', Shortlisted:'blue', Contacted:'blue', New:'blue', Interviewed:'purple',
  };
  const cls = map[status] || 'gray';
  return `<span class="badge badge-${cls}">${status}</span>`;
}

// ── Logout ────────────────────────────────────────────
function logout() {
  Auth.clear();
  window.location.href = '/frontend/html/login.html';
}

// ── Search filter ─────────────────────────────────────
function filterTable(inputId, tableId) {
  const input = document.getElementById(inputId);
  if (!input) return;
  input.addEventListener('input', () => {
    const q = input.value.toLowerCase();
    document.querySelectorAll(`#${tableId} tbody tr`).forEach(row => {
      row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  });
}

// ── Sidebar HTML ──────────────────────────────────────
function buildSidebar(activeItem) {
  const user = Auth.getUser();
  const role = user?.role || '';

  const allNav = [
    { icon: '⬡', label: 'Dashboard', href: 'admin-dashboard.html',  roles: ['admin','super_admin'] },
    { icon: '⬡', label: 'Dashboard', href: 'trainer-dashboard.html', roles: ['trainer'] },
    { icon: '⬡', label: 'Dashboard', href: 'student-dashboard.html', roles: ['student'] },
    { icon: '⬡', label: 'Dashboard', href: 'marketer-dashboard.html',roles: ['marketer'] },

    { section: 'Admin', roles: ['admin','super_admin'] },
    { icon: '👥', label: 'Students',  href: 'students.html',    roles: ['admin','super_admin'] },
    { icon: '🎓', label: 'Trainers',  href: 'trainers.html',   roles: ['admin','super_admin'] },
    { icon: '📚', label: 'Courses',   href: 'courses.html',    roles: ['admin','super_admin','trainer'] },
    { icon: '🗂', label: 'Batches',   href: 'batches.html',    roles: ['admin','super_admin','trainer'] },
    { icon: '💰', label: 'Fees',      href: 'fees.html',       roles: ['admin','super_admin'] },

    { section: 'Training', roles: ['admin','super_admin','trainer'] },
    { icon: '✅', label: 'Attendance', href: 'attendance.html', roles: ['admin','super_admin','trainer'] },
    { icon: '📁', label: 'Projects',   href: 'projects.html',  roles: ['admin','super_admin','trainer','student'] },
    { icon: '📊', label: 'Assessments',href: 'assessments.html',roles: ['admin','super_admin','trainer'] },

    { section: 'Placement', roles: ['admin','super_admin','student'] },
    { icon: '💼', label: 'Jobs',       href: 'jobs.html',      roles: ['admin','super_admin','student','trainer'] },

    { section: 'Marketing', roles: ['admin','super_admin','marketer'] },
    { icon: '🎯', label: 'Leads',      href: 'leads.html',     roles: ['admin','super_admin','marketer'] },

    { section: 'Analytics', roles: ['admin','super_admin'] },
    { icon: '📈', label: 'Reports',    href: 'reports.html',   roles: ['admin','super_admin'] },
  ];

  let html = '';
  allNav.forEach(item => {
    if (!item.roles.includes(role) && !item.roles.includes('all')) return;
    if (item.section) {
      html += `<div class="sidebar-section">${item.section}</div>`;
    } else {
      const active = item.label === activeItem ? 'active' : '';
      html += `<a href="${item.href}" class="nav-item ${active}"><span class="nav-icon">${item.icon}</span>${item.label}</a>`;
    }
  });

  return `
  <div class="sidebar" id="sidebar">
    <div class="sidebar-logo">
      <a class="logo-text" href="#"><span class="logo-dot"></span> Skill Track</a>
    </div>
    <nav class="sidebar-nav">${html}</nav>
    <div class="sidebar-footer">
      <div class="user-chip">
        <div class="avatar">U</div>
        <div class="info">
          <div class="name">User</div>
          <div class="role">${role}</div>
        </div>
      </div>
      <button onclick="logout()" class="btn btn-outline w-full mt-8" style="font-size:12px">Sign Out</button>
    </div>
  </div>`;
}

// ── Init page ─────────────────────────────────────────
function initPage(activeNav) {
  if (!Auth.requireAuth()) return;
  const shell = document.getElementById('app-shell');
  if (shell) {
    const sidebar = buildSidebar(activeNav);
    shell.insertAdjacentHTML('afterbegin', sidebar);
    renderUserChip();
  }
}
