// ===== Utility Functions =====

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('collapsed');
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('appToast');
    const body = document.getElementById('toastMessage');
    body.textContent = message;
    toast.className = 'toast align-items-center border-0 text-bg-' +
        (type === 'success' ? 'success' : type === 'error' ? 'danger' : 'warning');
    new bootstrap.Toast(toast, { delay: 3000 }).show();
}

function formatDate(dateStr) {
    return dateStr || '-';
}

function getScoreClass(score, maxScore) {
    const pct = maxScore > 0 ? (score / maxScore) * 100 : 0;
    if (pct >= 90) return 'excellent';
    if (pct >= 75) return 'good';
    if (pct >= 60) return 'fair';
    return 'poor';
}

function getScoreColor(score, maxScore) {
    const pct = maxScore > 0 ? (score / maxScore) * 100 : 0;
    if (pct >= 90) return '#16a34a';
    if (pct >= 75) return '#4361ee';
    if (pct >= 60) return '#f59e0b';
    return '#e63946';
}

async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' },
    };
    if (data) options.body = JSON.stringify(data);
    const resp = await fetch(url, options);
    if (!resp.ok) throw new Error(`API error: ${resp.status}`);
    return resp.json();
}

// Set current date
document.addEventListener('DOMContentLoaded', () => {
    const dateEl = document.getElementById('current-date');
    if (dateEl) {
        const now = new Date();
        dateEl.textContent = now.getFullYear() + '-' +
            String(now.getMonth() + 1).padStart(2, '0') + '-' +
            String(now.getDate()).padStart(2, '0');
    }
});
