from flask import render_template, request
from app.catalog import catalog_bp
from app.models.product import Product, ProductImage
from app.models.category import Category
from app.models.banner import Banner
from app.models.setting import BusinessSetting


def get_settings():
    settings = BusinessSetting.query.all()
    return {s.key: s.value for s in settings}


@catalog_bp.route('/')
def home():
    ctx = {'settings': get_settings()}
    ctx['banners'] = Banner.query.filter_by(is_active=True).order_by(Banner.sort_order.asc()).all()
    ctx['featured'] = Product.query.filter_by(is_active=True, is_featured=True).order_by(Product.sort_order.asc()).limit(8).all()
    ctx['new_products'] = Product.query.filter_by(is_active=True, is_new=True).order_by(Product.created_at.desc()).limit(8).all()
    ctx['categories'] = Category.query.filter_by(is_active=True).order_by(Category.order.asc()).all()
    return render_template('public/home.html', **ctx)


@catalog_bp.route('/catalogo')
def catalog():
    ctx = {'settings': get_settings()}
    ctx['category_id'] = request.args.get('category', type=int)
    ctx['search'] = request.args.get('q', '').strip()
    ctx['min_price'] = request.args.get('min', type=float)
    ctx['max_price'] = request.args.get('max', type=float)

    q = Product.query.filter_by(is_active=True)

    if ctx['category_id']:
        q = q.filter_by(category_id=ctx['category_id'])
    if ctx['search']:
        q = q.filter(Product.name.ilike(f'%{ctx["search"]}%'))
    if ctx['min_price'] is not None:
        q = q.filter(Product.price >= ctx['min_price'])
    if ctx['max_price'] is not None:
        q = q.filter(Product.price <= ctx['max_price'])

    ctx['products'] = q.order_by(Product.sort_order.asc(), Product.created_at.desc()).all()
    ctx['categories'] = Category.query.filter_by(is_active=True).order_by(Category.order.asc()).all()
    ctx['selected_category'] = ctx['category_id']
    
    if request.headers.get('HX-Request'):
        return render_template('public/_products_grid_partial.html', **ctx)
    return render_template('public/catalog.html', **ctx)


@catalog_bp.route('/producto/<slug>')
def product_detail(slug):
    ctx = {'settings': get_settings(), 'slug': slug}
    ctx['product'] = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    ctx['related'] = Product.query.filter(
        Product.category_id == ctx['product'].category_id,
        Product.id != ctx['product'].id,
        Product.is_active == True
    ).limit(4).all()
    
    if request.headers.get('HX-Request'):
        return render_template('public/_product_detail_modal.html', **ctx)
    return render_template('public/product_detail.html', **ctx)


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