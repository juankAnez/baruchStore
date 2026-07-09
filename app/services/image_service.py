import os
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
IMAGE_SIZE = (1200, 1200)
THUMB_SIZE = (400, 400)
QUALITY = 85


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file, subfolder='productos', convert_webp=False):
    if not allowed_file(file.filename):
        raise ValueError(f'Formato de archivo no permitido: {file.filename}')

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_path, exist_ok=True)

    img = Image.open(file)
    img = img.convert('RGB')
    img.thumbnail(IMAGE_SIZE, Image.LANCZOS)

    if convert_webp:
        filename = f'{os.path.splitext(secure_filename(file.filename))[0]}.webp'
        filepath = os.path.join(upload_path, filename)
        img.save(filepath, 'WEBP', quality=QUALITY, optimize=True)
    else:
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_path, filename)
        img.save(filepath, quality=QUALITY, optimize=True)

    thumb_filename = f'thumb_{filename}'
    thumb_path = os.path.join(upload_path, thumb_filename)
    thumb = img.copy()
    thumb.thumbnail(THUMB_SIZE, Image.LANCZOS)
    ext = 'WEBP' if convert_webp else 'JPEG' if filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg'} else 'PNG'
    thumb.save(thumb_path, ext, quality=QUALITY, optimize=True)

    return filename


def delete_image(filename, subfolder='productos'):
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    for fname in [filename, f'thumb_{filename}']:
        filepath = os.path.join(upload_path, fname)
        if os.path.exists(filepath):
            os.remove(filepath)