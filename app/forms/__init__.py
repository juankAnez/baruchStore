from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, TextAreaField, FloatField, BooleanField, IntegerField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Optional, NumberRange


class ProductForm(FlaskForm):
    name = StringField('Nombre del producto', validators=[DataRequired()])
    sku = StringField('SKU (código)', validators=[Optional()])
    category_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    subcategory = StringField('Subcategoría', validators=[Optional()])
    brand = StringField('Marca', validators=[Optional()])
    price = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    old_price = FloatField('Precio anterior (para descuento)', validators=[Optional(), NumberRange(min=0)])
    short_description = TextAreaField('Descripción corta', validators=[Optional()])
    description = TextAreaField('Descripción completa', validators=[Optional()])
    features = TextAreaField('Características (una por línea)', validators=[Optional()])
    sort_order = IntegerField('Orden de aparición', validators=[Optional()], default=0)
    is_active = BooleanField('Activo')
    is_featured = BooleanField('Destacado')
    is_new = BooleanField('Nuevo')
    is_offer = BooleanField('Oferta')
    images = FileField('Imágenes', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Solo imágenes (jpg, png, gif, webp)')
    ])


class CategoryForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[Optional()])
    icon = StringField('Icono (emoji)', validators=[Optional()])
    order = IntegerField('Orden', validators=[Optional()], default=0)
    is_active = BooleanField('Activo')
    image = FileField('Imagen', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Solo imágenes')
    ])


class BannerForm(FlaskForm):
    title = StringField('Título', validators=[Optional()])
    subtitle = StringField('Subtítulo', validators=[Optional()])
    button_text = StringField('Texto del botón', validators=[Optional()])
    link = StringField('Enlace', validators=[Optional()])
    sort_order = IntegerField('Orden', validators=[Optional()], default=0)
    is_active = BooleanField('Activo')
    image = FileField('Imagen', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Solo imágenes')
    ])