import logging
from flask import Flask, render_template
from app.config import config
from app.extensions import db, migrate, login_manager, csrf
from app.models.admin_user import AdminUser

DEFAULT_STORE_NAME = 'Brillo Rosa'


@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.catalog import catalog_bp
    from app.api import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(catalog_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.template_filter('money')
    def money(value):
        """$45.900 — miles con punto; decimales solo si los hay (con coma)."""
        try:
            v = float(value or 0)
        except (TypeError, ValueError):
            return value
        if v.is_integer():
            return '$' + f'{v:,.0f}'.replace(',', '.')
        return '$' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

    @app.context_processor
    def inject_public_context():
        # Valores comunes para navbar/footer/base; las vistas pueden sobrescribirlos.
        from app.models.setting import BusinessSetting
        from app.models.category import Category
        try:
            settings = {s.key: s.value for s in BusinessSetting.query.all()}
            categories = Category.query.filter_by(is_active=True).order_by(Category.order.asc()).all()
        except Exception:
            db.session.rollback()
            settings, categories = {}, []
        store_name = (settings.get('business_name') or '').strip() or DEFAULT_STORE_NAME
        return {'settings': settings, 'categories': categories, 'store_name': store_name}

    @app.errorhandler(404)
    def not_found(e):
        return render_template('public/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('public/500.html'), 500

    with app.app_context():
        from app.models import admin_user, category, product, banner, setting
        db.create_all()

    return app