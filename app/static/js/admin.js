/* ═══════════════════════════════════════════════════════
   Baruch Store - Admin Panel JavaScript
   ═══════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

    // ── HTMX configuration ──
    document.body.addEventListener('htmx:configRequest', function(evt) {
        evt.detail.headers['X-CSRFToken'] = document.querySelector('meta[name="csrf-token"]')?.content || '';
    });

    // ── HTMX after swap animations ──
    document.body.addEventListener('htmx:afterSwap', function(evt) {
        if (evt.detail.target) {
            evt.detail.target.style.opacity = '0';
            evt.detail.target.style.transform = 'translateY(-4px)';
            requestAnimationFrame(() => {
                evt.detail.target.style.transition = 'all 0.2s ease';
                evt.detail.target.style.opacity = '1';
                evt.detail.target.style.transform = 'translateY(0)';
            });
        }
    });

    // ── Auto-dismiss flash messages ──
    const flashMessages = document.querySelectorAll('#flash-messages > div');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-8px)';
            msg.style.transition = 'all 0.3s ease';
            setTimeout(() => msg.remove(), 300);
        }, 5000);
    });

    // ── File input label update ──
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', function() {
            const label = this.closest('.border-dashed')?.querySelector('p');
            if (label && this.files.length > 0) {
                label.textContent = `${this.files.length} archivo(s) seleccionado(s)`;
            }
        });
    });

    // ── Confirm delete dialogs ──
    document.querySelectorAll('form[onsubmit]').forEach(form => {
        form.addEventListener('submit', function(e) {
            const message = this.getAttribute('onsubmit')?.replace("return confirm('", '').replace("')", '');
            if (message && !confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // ── Keyboard shortcuts ──
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K: Focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[name="q"]');
            if (searchInput) searchInput.focus();
        }
    });

    console.log('Admin panel loaded');
});
