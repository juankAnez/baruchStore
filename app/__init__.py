import logging
from flask import Flask, render_template
from app.config import config
from app.extensions import db, migrate, login_manager, csrf
from app.models.admin_user import AdminUser


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