document.addEventListener('DOMContentLoaded', function () {
    // Initialize Lucide Icons
    if (window.lucide) {
        lucide.createIcons();
    }

    // HTMX Settle listener: refresh Lucide icons for any dynamic elements swapped in by HTMX
    document.body.addEventListener('htmx:afterSettle', () => {
        if (window.lucide) {
            lucide.createIcons();
        }
    });

    // Animated counters
    const counters = document.querySelectorAll('[data-counter]');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-counter'));
        let current = 0;
        const step = Math.ceil(target / 30);
        const update = setInterval(() => {
            current += step;
            if (current >= target) { current = target; clearInterval(update); }
            counter.textContent = current;
        }, 40);
    });

    // Toast notification system
    window.showToast = function(message, type = 'success', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = 'toast flex items-center gap-3.5';
        const icons = {
            success: '<i data-lucide="check-circle" class="w-5 h-5 text-emerald-400"></i>',
            error: '<i data-lucide="alert-circle" class="w-5 h-5 text-red-400"></i>',
        };
        toast.innerHTML = (icons[type] || icons.success) + '<span class="text-sm font-semibold tracking-wide">' + message + '</span>';
        document.body.appendChild(toast);
        
        // Initialize the lucide icon in toast
        if (window.lucide) lucide.createIcons({attrs: {class: 'w-5 h-5 text-emerald-400'}});

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    };

    // Intercept cart add to show toast
    document.addEventListener('alpine:initialized', () => {
        if (Alpine.store('cart')) {
            const original = Alpine.store('cart').addItem.bind(Alpine.store('cart'));
            Alpine.store('cart').addItem = function(product) {
                original(product);
                showToast(product.name + ' agregado al carrito', 'success');
            };
        }
    });
});

// Register Alpine.js store for Product Detail Modal
document.addEventListener('alpine:init', () => {
    Alpine.store('productDetailModal', {
        open: false,
        open() {
            this.open = true;
            // Refresh Lucide Icons once modal content is swapped
            setTimeout(() => {
                if (window.lucide) lucide.createIcons();
            }, 100);
        },
        close() {
            this.open = false;
        }
    });
});
