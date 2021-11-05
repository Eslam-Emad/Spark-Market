import bcrypt
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from market import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer, nullable=False, default=100000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.email_address = email

    def can_purchase(self, item):
        return self.budget >= item.price

    def can_sell(self, item):
        return item in self.items

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f'{self.budget}$'

    def validate_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash)

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password_setter(self, password):
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def __repr__(self):
        return f'{self.username}'
