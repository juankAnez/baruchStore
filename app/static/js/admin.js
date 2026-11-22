/* Panel de administración */

// Iconos Lucide (también los que lleguen después por HTMX o Alpine)
(function () {
    let pending = false;
    const render = () => { pending = false; if (window.lucide) lucide.createIcons(); };
    const schedule = () => { if (!pending) { pending = true; requestAnimationFrame(render); } };
    document.addEventListener('DOMContentLoaded', () => {
        render();
        new MutationObserver(ms => {
            for (const m of ms) for (const n of m.addedNodes) {
                if (n.nodeType === 1 && (n.matches('i[data-lucide]') || n.querySelector('i[data-lucide]'))) { schedule(); return; }
            }
        }).observe(document.body, { childList: true, subtree: true });
    });
})();

document.addEventListener('DOMContentLoaded', function () {
    // Token CSRF en las peticiones HTMX
    document.body.addEventListener('htmx:configRequest', function (evt) {
        evt.detail.headers['X-CSRFToken'] = document.querySelector('meta[name="csrf-token"]')?.content || '';
    });

    // Ctrl/Cmd + K: ir al buscador de la página
    document.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
            const input = document.querySelector('input[name="q"]');
            if (input) { e.preventDefault(); input.focus(); }
        }
    });
});

// Confirmación con estilo para formularios con data-confirm
document.addEventListener('alpine:init', () => {
    Alpine.store('confirm', {
        open: false, message: '', blocked: false, form: null,
        ask(form) {
            this.form = form;
            this.message = form.dataset.confirm;
            this.blocked = form.hasAttribute('data-confirm-block');
            this.open = true;
        },
        accept() {
            const form = this.form;
            this.open = false;
            if (form) { form.dataset.confirmed = '1'; form.requestSubmit ? form.requestSubmit() : form.submit(); }
        },
        cancel() { this.open = false; this.form = null; },
    });
});
document.addEventListener('submit', (e) => {
    const form = e.target;
    if (!(form instanceof HTMLFormElement) || !form.dataset.confirm) return;
    if (form.dataset.confirmed === '1') { delete form.dataset.confirmed; return; }
    e.preventDefault();
    if (window.Alpine) Alpine.store('confirm').ask(form);
    else if (confirm(form.dataset.confirm)) form.submit();
}, true);

// Vista previa de imágenes en los campos de subida (Alpine)
// Uso: <div x-data="imagePicker()"> ... <input type="file" @change="pick($event)"> ...
window.imagePicker = function () {
    return {
        previews: [],
        dragging: false,
        pick(e) {
            this.previews.forEach(p => URL.revokeObjectURL(p.url));
            this.previews = [...e.target.files].map(f => ({ name: f.name, url: URL.createObjectURL(f) }));
        },
        drop(e) {
            this.dragging = false;
            const input = this.$refs.file;
            if (!e.dataTransfer?.files?.length || !input) return;
            const dt = new DataTransfer();
            [...e.dataTransfer.files].filter(f => f.type.startsWith('image/'))
                .slice(0, input.multiple ? 50 : 1).forEach(f => dt.items.add(f));
            input.files = dt.files;
            this.pick({ target: input });
        },
    };
};
