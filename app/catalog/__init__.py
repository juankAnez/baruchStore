from flask import Blueprint

catalog_bp = Blueprint('catalog', __name__,
                        template_folder='templates',
                        static_folder='../static')

from app.catalog import routes