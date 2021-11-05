from market import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def assign_ownership(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def remove_ownership(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()


def __repr__(self):
    return f'Item {self.name}'
