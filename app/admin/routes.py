from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from app.admin import admin_bp
from app.extensions import db
from app.models.product import Product, ProductImage
from app.models.category import Category
from app.models.banner import Banner
from app.models.setting import BusinessSetting


@admin_bp.route('/')
@login_required
def dashboard():
    total_products = Product.query.count()
    active_products = Product.query.filter_by(is_active=True).count()
    hidden_products = Product.query.filter_by(is_active=False).count()
    total_categories = Category.query.count()
    featured_products = Product.query.filter_by(is_featured=True, is_active=True).count()
    new_products = Product.query.filter_by(is_new=True, is_active=True).count()
    latest_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html', **locals())


@admin_bp.route('/products')
@login_required
def products():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('q', '').strip()

    query = Product.query

    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    products = query.order_by(Product.sort_order.asc(), Product.created_at.desc()).all()
    categories = Category.query.order_by(Category.order.asc()).all()

    return render_template('admin/products.html', **{
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'search': search,
    })


@admin_bp.route('/products/toggle/<int:product_id>')
@login_required
def toggle_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.is_active = not product.is_active
    db.session.commit()
    if request.headers.get('HX-Request'):
        return render_template('admin/_product_row.html', product=product)
    return redirect(url_for('admin.products'))


@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('admin.products'))


@admin_bp.route('/categories')
@login_required
def categories():
    all_categories = Category.query.order_by(Category.order.asc()).all()
    return render_template('admin/categories.html', categories=all_categories)


@admin_bp.route('/banners')
@login_required
def banners():
    all_banners = Banner.query.order_by(Banner.sort_order.asc()).all()
    return render_template('admin/banners.html', banners=all_banners)


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        for key, value in request.form.items():
            if key != 'csrf_token':
                setting = BusinessSetting.query.filter_by(key=key).first()
                if setting:
                    setting.value = value
                else:
                    setting = BusinessSetting(key=key, value=value)
                    db.session.add(setting)
        db.session.commit()
        flash('Configuración guardada correctamente', 'success')
        return redirect(url_for('admin.settings'))

    settings_list = BusinessSetting.query.all()
    settings_dict = {s.key: s.value for s in settings_list}
    return render_template('admin/settings.html', settings=settings_dict)