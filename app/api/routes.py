from flask import jsonify, request
from app.api import api_bp
from app.models.product import Product
from app.models.category import Category
from app.models.banner import Banner
from app.models.setting import BusinessSetting


@api_bp.route('/products/search')
def search_products():
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])
    products = Product.query.filter(
        Product.is_active == True,
        Product.name.ilike(f'%{q}%')
    ).order_by(Product.sort_order.asc()).limit(10).all()

    return jsonify([{
        'id': p.id,
        'name': p.name,
        'slug': p.slug,
        'price': float(p.price),
        'old_price': float(p.old_price) if p.old_price else None,
        'image': p.primary_image,
    } for p in products])


@api_bp.route('/products/filter')
def filter_products():
    category_id = request.args.get('category', type=int)
    min_price = request.args.get('min', type=float)
    max_price = request.args.get('max', type=float)

    query = Product.query.filter_by(is_active=True)

    if category_id:
        query = query.filter_by(category_id=category_id)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    products = query.order_by(Product.sort_order.asc()).all()

    return jsonify([{
        'id': p.id,
        'name': p.name,
        'slug': p.slug,
        'price': float(p.price),
        'old_price': float(p.old_price) if p.old_price else None,
        'image': p.primary_image,
        'is_new': p.is_new,
        'is_featured': p.is_featured,
        'is_offer': p.is_offer,
    } for p in products])


@api_bp.route('/categories')
def get_categories():
    categories = Category.query.filter_by(is_active=True).order_by(Category.order.asc()).all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'slug': c.slug,
        'image': c.image,
        'description': c.description,
    } for c in categories])


@api_bp.route('/banners')
def get_banners():
    banners = Banner.query.filter_by(is_active=True).order_by(Banner.sort_order.asc()).all()
    return jsonify([{
        'id': b.id,
        'image': b.image,
        'title': b.title,
        'subtitle': b.subtitle,
        'button_text': b.button_text,
        'link': b.link,
    } for b in banners])


@api_bp.route('/settings')
def get_settings():
    settings = BusinessSetting.query.all()
    return jsonify({s.key: s.value for s in settings})