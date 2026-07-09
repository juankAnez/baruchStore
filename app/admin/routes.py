import os
import json
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from app.admin import admin_bp
from app.extensions import db
from app.models.product import Product, ProductImage
from app.models.category import Category
from app.models.banner import Banner
from app.models.setting import BusinessSetting
from app.forms import ProductForm, CategoryForm, BannerForm
from app.services.image_service import save_image, delete_image


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
    category_id = request.args.get('category', type=int)
    search = request.args.get('q', '').strip()

    query = Product.query

    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    products_list = query.order_by(Product.sort_order.asc(), Product.created_at.desc()).all()
    categories = Category.query.order_by(Category.order.asc()).all()

    return render_template('admin/products.html', **{
        'products': products_list,
        'categories': categories,
        'selected_category': category_id,
        'search': search,
    })


@admin_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
def product_create():
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]

    if form.validate_on_submit():
        features_list = [f.strip() for f in form.features.data.split('\n') if f.strip()] if form.features.data else []

        product = Product(
            name=form.name.data,
            sku=form.sku.data or None,
            category_id=form.category_id.data,
            subcategory=form.subcategory.data or '',
            brand=form.brand.data or '',
            price=form.price.data,
            old_price=form.old_price.data,
            short_description=form.short_description.data or '',
            description=form.description.data or '',
            features=features_list,
            sort_order=form.sort_order.data or 0,
            is_active=form.is_active.data,
            is_featured=form.is_featured.data,
            is_new=form.is_new.data,
            is_offer=form.is_offer.data,
        )
        product.save()

        files = request.files.getlist('images')
        for i, file in enumerate(files):
            if file and file.filename:
                try:
                    filename = save_image(file, 'productos', convert_webp=True)
                    img = ProductImage(
                        product_id=product.id,
                        filename=filename,
                        is_primary=(i == 0),
                        sort_order=i
                    )
                    db.session.add(img)
                except ValueError as e:
                    flash(str(e), 'warning')

        db.session.commit()
        flash('Producto creado correctamente', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, title='Nuevo Producto')


@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def product_edit(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]

    if request.method == 'GET':
        form.features.data = '\n'.join(product.features) if product.features else ''

    if form.validate_on_submit():
        features_list = [f.strip() for f in form.features.data.split('\n') if f.strip()] if form.features.data else []

        product.name = form.name.data
        product.sku = form.sku.data or ''
        product.category_id = form.category_id.data
        product.subcategory = form.subcategory.data or ''
        product.brand = form.brand.data or ''
        product.price = form.price.data
        product.old_price = form.old_price.data
        product.short_description = form.short_description.data or ''
        product.description = form.description.data or ''
        product.features = features_list
        product.sort_order = form.sort_order.data or 0
        product.is_active = form.is_active.data
        product.is_featured = form.is_featured.data
        product.is_new = form.is_new.data
        product.is_offer = form.is_offer.data

        db.session.commit()

        files = request.files.getlist('images')
        for i, file in enumerate(files):
            if file and file.filename:
                try:
                    filename = save_image(file, 'productos', convert_webp=True)
                    img = ProductImage(
                        product_id=product.id,
                        filename=filename,
                        is_primary=(not product.images and i == 0),
                        sort_order=(product.images[-1].sort_order + 1 if product.images else 0) + i
                    )
                    db.session.add(img)
                except ValueError as e:
                    flash(str(e), 'warning')

        db.session.commit()
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, product=product, title='Editar Producto')


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
    for img in product.images:
        delete_image(img.filename, 'productos')
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('admin.products'))


@admin_bp.route('/products/duplicate/<int:product_id>', methods=['POST'])
@login_required
def duplicate_product(product_id):
    original = Product.query.get_or_404(product_id)
    product = Product(
        name=f'{original.name} (copia)',
        sku=f'{original.sku}-COPY' if original.sku else '',
        category_id=original.category_id,
        subcategory=original.subcategory,
        brand=original.brand,
        price=original.price,
        old_price=original.old_price,
        short_description=original.short_description,
        description=original.description,
        features=original.features,
        sort_order=original.sort_order + 1,
        is_active=False,
        is_featured=False,
        is_new=False,
        is_offer=False,
    )
    product.save()
    flash('Producto duplicado correctamente', 'success')
    return redirect(url_for('admin.products'))


@admin_bp.route('/products/images/delete/<int:image_id>', methods=['POST'])
@login_required
def delete_product_image(image_id):
    img = ProductImage.query.get_or_404(image_id)
    delete_image(img.filename, 'productos')
    db.session.delete(img)
    db.session.commit()
    flash('Imagen eliminada', 'success')
    return redirect(url_for('admin.product_edit', product_id=img.product_id))


@admin_bp.route('/products/images/primary/<int:image_id>', methods=['POST'])
@login_required
def set_primary_image(image_id):
    img = ProductImage.query.get_or_404(image_id)
    ProductImage.query.filter_by(product_id=img.product_id).update({'is_primary': False})
    img.is_primary = True
    db.session.commit()
    flash('Imagen principal actualizada', 'success')
    return redirect(url_for('admin.product_edit', product_id=img.product_id))


# --------------- CATEGORÍAS ---------------

@admin_bp.route('/categories')
@login_required
def categories():
    all_categories = Category.query.order_by(Category.order.asc()).all()
    return render_template('admin/categories.html', categories=all_categories)


@admin_bp.route('/categories/create', methods=['GET', 'POST'])
@login_required
def category_create():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data or '',
            icon=form.icon.data or '',
            order=form.order.data or 0,
            is_active=form.is_active.data,
        )
        category.save()

        file = request.files.get('image')
        if file and file.filename:
            try:
                filename = save_image(file, 'categories', convert_webp=True)
                category.image = filename
                db.session.commit()
            except ValueError as e:
                flash(str(e), 'warning')

        flash('Categoría creada correctamente', 'success')
        return redirect(url_for('admin.categories'))

    return render_template('admin/category_form.html', form=form, title='Nueva Categoría')


@admin_bp.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def category_edit(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)

    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data or ''
        category.icon = form.icon.data or ''
        category.order = form.order.data or 0
        category.is_active = form.is_active.data
        db.session.commit()

        file = request.files.get('image')
        if file and file.filename:
            try:
                if category.image:
                    delete_image(category.image, 'categories')
                filename = save_image(file, 'categories', convert_webp=True)
                category.image = filename
                db.session.commit()
            except ValueError as e:
                flash(str(e), 'warning')

        flash('Categoría actualizada correctamente', 'success')
        return redirect(url_for('admin.categories'))

    return render_template('admin/category_form.html', form=form, category=category, title='Editar Categoría')


@admin_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@login_required
def category_delete(category_id):
    category = Category.query.get_or_404(category_id)
    if category.image:
        delete_image(category.image, 'categories')
    db.session.delete(category)
    db.session.commit()
    flash('Categoría eliminada correctamente', 'success')
    return redirect(url_for('admin.categories'))


# --- BANNERS ---------------

@admin_bp.route('/banners')
@login_required
def banners():
    all_banners = Banner.query.order_by(Banner.sort_order.asc()).all()
    return render_template('admin/banners.html', banners=all_banners)


@admin_bp.route('/banners/create', methods=['GET', 'POST'])
@login_required
def banner_create():
    form = BannerForm()
    if form.validate_on_submit():
        banner = Banner(
            title=form.title.data or '',
            subtitle=form.subtitle.data or '',
            button_text=form.button_text.data or '',
            link=form.link.data or '',
            sort_order=form.sort_order.data or 0,
            is_active=form.is_active.data,
        )
        db.session.add(banner)
        db.session.commit()

        file = request.files.get('image')
        if file and file.filename:
            try:
                filename = save_image(file, 'banners', convert_webp=True)
                banner.image = filename
                db.session.commit()
            except ValueError as e:
                flash(str(e), 'warning')

        flash('Banner creado correctamente', 'success')
        return redirect(url_for('admin.banners'))

    return render_template('admin/banner_form.html', form=form, title='Nuevo Banner')


@admin_bp.route('/banners/edit/<int:banner_id>', methods=['GET', 'POST'])
@login_required
def banner_edit(banner_id):
    banner = Banner.query.get_or_404(banner_id)
    form = BannerForm(obj=banner)

    if form.validate_on_submit():
        banner.title = form.title.data or ''
        banner.subtitle = form.subtitle.data or ''
        banner.button_text = form.button_text.data or ''
        banner.link = form.link.data or ''
        banner.sort_order = form.sort_order.data or 0
        banner.is_active = form.is_active.data
        db.session.commit()

        file = request.files.get('image')
        if file and file.filename:
            try:
                if banner.image:
                    delete_image(banner.image, 'banners')
                filename = save_image(file, 'banners', convert_webp=True)
                banner.image = filename
                db.session.commit()
            except ValueError as e:
                flash(str(e), 'warning')

        flash('Banner actualizado correctamente', 'success')
        return redirect(url_for('admin.banners'))

    return render_template('admin/banner_form.html', form=form, banner=banner, title='Editar Banner')


@admin_bp.route('/banners/delete/<int:banner_id>', methods=['POST'])
@login_required
def banner_delete(banner_id):
    banner = Banner.query.get_or_404(banner_id)
    if banner.image:
        delete_image(banner.image, 'banners')
    db.session.delete(banner)
    db.session.commit()
    flash('Banner eliminado correctamente', 'success')
    return redirect(url_for('admin.banners'))


# --------------- SETTINGS ---------------

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