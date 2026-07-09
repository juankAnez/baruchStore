from app.extensions import db


class BusinessSetting(db.Model):
    __tablename__ = 'business_settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.Text)

    def __str__(self):
        return self.key