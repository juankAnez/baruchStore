document.addEventListener('alpine:init', () => {
    Alpine.store('cart', {
        items: JSON.parse(localStorage.getItem('baruch-cart') || '[]'),
        open: false,

        get count() {
            return this.items.reduce((sum, item) => sum + item.quantity, 0);
        },

        get subtotal() {
            return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
        },

        get total() {
            return this.subtotal;
        },

        get whatsappUrl() {
            const lines = ['🛒 *Pedido Baruch Store*', ''];
            this.items.forEach(item => {
                const sub = (item.price * item.quantity).toFixed(2);
                lines.push(`• ${item.name} x${item.quantity} = $${sub}`);
            });
            lines.push('', `*Total: $${this.total.toFixed(2)}*`);
            const message = lines.join('\n');
            return `https://wa.me/?text=${encodeURIComponent(message)}`;
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
        }
    });
});