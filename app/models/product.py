from app.extensions import db
from app.models.category import slugify


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    sku = db.Column(db.String(80))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    subcategory = db.Column(db.String(120))
    brand = db.Column(db.String(120))
    price = db.Column(db.Float, nullable=False)
    old_price = db.Column(db.Float)
    short_description = db.Column(db.Text)
    description = db.Column(db.Text)
    features = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_new = db.Column(db.Boolean, default=False)
    is_offer = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    images = db.relationship('ProductImage', backref='product', lazy='joined',
                             cascade='all, delete-orphan',
                             order_by='ProductImage.sort_order')

    @property
    def primary_image(self):
        primary = ProductImage.query.filter_by(product_id=self.id, is_primary=True).first()
        if primary:
            return primary.filename
        first = ProductImage.query.filter_by(product_id=self.id).first()
        return first.filename if first else None

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    def save(self):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.query.filter_by(slug=slug).first():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return self.name


class ProductImage(db.Model):
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.now())