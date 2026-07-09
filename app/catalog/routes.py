from flask import render_template, request
from app.catalog import catalog_bp
from app.models.product import Product
from app.models.category import Category
from app.models.banner import Banner
from app.models.setting import BusinessSetting


def get_settings():
    settings = BusinessSetting.query.all()
    return {s.key: s.value for s in settings}


@catalog_bp.route('/')
def home():
    settings = get_settings()
    banners = Banner.query.filter_by(is_active=True).order_by(Banner.sort_order.asc()).all()
    featured = Product.query.filter_by(is_active=True, is_featured=True).order_by(Product.sort_order.asc()).limit(8).all()
    new_products = Product.query.filter_by(is_active=True, is_new=True).order_by(Product.created_at.desc()).limit(8).all()
    categories = Category.query.filter_by(is_active=True).order_by(Category.order.asc()).all()
    return render_template('public/home.html', **locals())


@catalog_bp.route('/catalogo')
def catalog():
    settings = get_settings()
    category_id = request.args.get('category', type=int)
    search = request.args.get('q', '').strip()
    min_price = request.args.get('min', type=float)
    max_price = request.args.get('max', type=float)

    query = Product.query.filter_by(is_active=True)

    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    products = query.order_by(Product.sort_order.asc(), Product.created_at.desc()).all()
    categories = Category.query.filter_by(is_active=True).order_by(Category.order.asc()).all()
    selected_category = category_id
    return render_template('public/catalog.html', **locals())


@catalog_bp.route('/producto/<slug>')
def product_detail(slug):
    settings = get_settings()
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    related = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()
    return render_template('public/product_detail.html', **locals())


@catalog_bp.route('/producto/<slug>/galeria')
def product_gallery(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()
    images = ProductImage.query.filter_by(product_id=product.id).order_by(ProductImage.sort_order.asc()).all()
    return render_template('public/_product_gallery.html', product=product, images=images)


@catalog_bp.route('/search')
def search_products():
    q = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)
    products = []
    if len(q) >= 2:
        query = Product.query.filter(Product.is_active == True, Product.name.ilike(f'%{q}%'))
        if category_id:
            query = query.filter_by(category_id=category_id)
        products = query.order_by(Product.sort_order.asc()).limit(10).all()
    return render_template('public/_search_results.html', products=products)