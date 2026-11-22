// ── Iconos Lucide ──
// Un observador re-dibuja los iconos que aparezcan después (HTMX, Alpine x-for/x-if, avisos).
(function () {
    let pending = false;
    function renderIcons() {
        pending = false;
        if (window.lucide) lucide.createIcons();
    }
    function schedule() {
        if (!pending) {
            pending = true;
            requestAnimationFrame(renderIcons);
        }
    }
    document.addEventListener('DOMContentLoaded', () => {
        renderIcons();
        new MutationObserver(mutations => {
            for (const m of mutations) {
                for (const node of m.addedNodes) {
                    if (node.nodeType === 1 && (node.matches('i[data-lucide]') || node.querySelector('i[data-lucide]'))) {
                        schedule();
                        return;
                    }
                }
            }
        }).observe(document.body, { childList: true, subtree: true });
    });
})();

// ── Avisos ──
window.showToast = function (message, type = 'success', duration = 2800) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'status');
    const icon = type === 'error'
        ? '<i data-lucide="alert-circle" class="w-5 h-5 text-bubble"></i>'
        : '<svg class="w-5 h-5 text-bubble" aria-hidden="true"><use href="#sparkle"/></svg>';
    toast.innerHTML = icon + '<span class="text-sm font-medium"></span>';
    toast.querySelector('span').textContent = message;
    document.querySelectorAll('.toast').forEach(t => t.remove());
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.transition = 'opacity .3s ease, transform .3s ease';
        toast.style.opacity = '0';
        toast.style.transform += ' translateY(10px)';
        setTimeout(() => toast.remove(), 300);
    }, duration);
};

// ── Panel de detalle de producto ──
document.addEventListener('alpine:init', () => {
    const skeleton = '<div class="p-6 space-y-4"><div class="skeleton aspect-square"></div><div class="skeleton h-6 w-2/3"></div><div class="skeleton h-4 w-1/3"></div></div>';
    Alpine.store('productDetailModal', {
        open: false,
        show() {
            const box = document.getElementById('product-detail-modal-content');
            if (box) { box.innerHTML = skeleton; box.scrollTop = 0; }
            this.open = true;
            document.documentElement.style.overflow = 'hidden';
        },
        close() {
            this.open = false;
            document.documentElement.style.overflow = '';
        }
    });
});
