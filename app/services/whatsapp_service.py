import urllib.parse
from app.models.setting import BusinessSetting


def get_setting(key, default=''):
    setting = BusinessSetting.query.filter_by(key=key).first()
    return setting.value if setting else default


def build_whatsapp_message(cart_items, total):
    business_name = get_setting('business_name', 'Baruch Store')
    lines = [f'🛒 *Pedido {business_name}*', '']
    for item in cart_items:
        subtotal = item['price'] * item['quantity']
        lines.append(
            f'• {item["name"]} x{item["quantity"]} = ${subtotal:.2f}'
        )
    lines.extend(['', f'*Total: ${total:.2f}*'])
    return '\n'.join(lines)


def get_whatsapp_url(cart_items, total):
    phone = get_setting('whatsapp', '').strip()
    if not phone:
        return '#'
    phone = phone.replace('+', '').replace(' ', '').replace('-', '')
    message = build_whatsapp_message(cart_items, total)
    return f'https://wa.me/{phone}?text={urllib.parse.quote(message)}'


def get_instagram_url():
    username = get_setting('instagram', '').strip()
    if not username:
        return '#'
    username = username.replace('@', '').strip()
    return f'https://instagram.com/{username}'