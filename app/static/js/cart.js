document.addEventListener('alpine:init', () => {
    Alpine.store('cart', {
        items: JSON.parse(localStorage.getItem('baruch-cart') || '[]'),
        open: false,
        whatsappNumber: (window.BARUCH_CONFIG?.whatsapp || '').replace(/[^0-9]/g, ''),
        shippingForm: {
            name: localStorage.getItem('baruch-shipping-name') || '',
            address: localStorage.getItem('baruch-shipping-address') || '',
            phone: localStorage.getItem('baruch-shipping-phone') || '',
            payment: localStorage.getItem('baruch-shipping-payment') || 'Efectivo'
        },

        get count() {
            return this.items.reduce((sum, item) => sum + item.quantity, 0);
        },

        get subtotal() {
            return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
        },

        get total() {
            return this.subtotal;
        },

        addItem(product) {
            const existing = this.items.find(i => i.id === product.id);
            if (existing) {
                existing.quantity += 1;
            } else {
                this.items.push({ ...product, quantity: 1 });
            }
            this.persist();
        },

        removeItem(index) {
            this.items.splice(index, 1);
            this.persist();
        },

        increaseQuantity(index) {
            this.items[index].quantity += 1;
            this.persist();
        },

        decreaseQuantity(index) {
            const item = this.items[index];
            if (item.quantity > 1) {
                item.quantity -= 1;
            } else {
                this.items.splice(index, 1);
            }
            this.persist();
        },

        clearCart() {
            this.items = [];
            this.persist();
        },

        persist() {
            localStorage.setItem('baruch-cart', JSON.stringify(this.items));
            // Persist form data as a convenience for the customer
            localStorage.setItem('baruch-shipping-name', this.shippingForm.name);
            localStorage.setItem('baruch-shipping-address', this.shippingForm.address);
            localStorage.setItem('baruch-shipping-phone', this.shippingForm.phone);
            localStorage.setItem('baruch-shipping-payment', this.shippingForm.payment);
        },

        checkoutWhatsApp() {
            // Save form changes to local storage
            this.persist();

            // Validate form
            if (!this.shippingForm.name.trim()) {
                if (window.showToast) window.showToast("Por favor, ingresa tu Nombre completo", "error");
                return;
            }
            if (!this.shippingForm.address.trim()) {
                if (window.showToast) window.showToast("Por favor, ingresa tu Dirección de envío", "error");
                return;
            }
            if (!this.shippingForm.phone.trim()) {
                if (window.showToast) window.showToast("Por favor, ingresa un Teléfono de contacto", "error");
                return;
            }

            // Build professional WhatsApp message
            const lines = [];
            lines.push('🛒 *NUEVO PEDIDO - BARUCH STORE*');
            lines.push('==================================');
            lines.push('');
            lines.push('*Datos del Cliente:*');
            lines.push(`• *Nombre:* ${this.shippingForm.name.trim()}`);
            lines.push(`• *Dirección:* ${this.shippingForm.address.trim()}`);
            lines.push(`• *Teléfono:* ${this.shippingForm.phone.trim()}`);
            lines.push(`• *Método de Pago:* ${this.shippingForm.payment}`);
            lines.push('');
            lines.push('*Productos:*');
            
            this.items.forEach(item => {
                const subtotal = (item.price * item.quantity).toFixed(2);
                lines.push(`• ${item.name} (x${item.quantity}) - $${subtotal}`);
            });
            
            lines.push('');
            lines.push('==================================');
            lines.push(`*TOTAL A PAGAR: $${this.total.toFixed(2)}*`);
            lines.push('==================================');
            lines.push('');
            lines.push('_Por favor, confírmame el pedido para coordinar la entrega. ¡Gracias!_');

            const message = lines.join('\n');
            const targetPhone = this.whatsappNumber ? this.whatsappNumber.replace(/[^0-9]/g, '') : '';
            const url = `https://wa.me/${targetPhone}?text=${encodeURIComponent(message)}`;
            
            // Open WhatsApp
            window.open(url, '_blank');

            // Clear cart & close sidebar
            this.clearCart();
            this.open = false;
            
            if (window.showToast) {
                window.showToast("¡Pedido enviado por WhatsApp! Carrito vaciado.", "success");
            }
        }
    });
});