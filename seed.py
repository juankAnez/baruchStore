import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app import create_app
from app.extensions import db
from app.models.admin_user import AdminUser
from app.models.setting import BusinessSetting

app = create_app()

with app.app_context():
    db.create_all()

    if not AdminUser.query.first():
        admin = AdminUser(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        print('OK - Usuario admin creado (admin / admin123)')

    default_settings = {
        'business_name': 'Baruch Store',
        'whatsapp': '',
        'instagram': '',
        'facebook': '',
        'email': '',
        'address': '',
        'hours': '',
        'footer_text': '(c) 2026 Baruch Store. Todos los derechos reservados.',
        'whatsapp_message': 'Hola! Quiero hacer un pedido:',
    }

    for key, value in default_settings.items():
        if not BusinessSetting.query.filter_by(key=key).first():
            setting = BusinessSetting(key=key, value=value)
            db.session.add(setting)
            print(f'OK - Setting creado: {key}')

    db.session.commit()
    print('\nSeed completado. App lista para usar.')