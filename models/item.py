from db import db

class ItemModel(db.Model): #tells SQLAlchemy entity that Item model are things that we are going to be saving to and retrieving from a db and creates mapping between the db and the objects

    __tablename__='items'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80))
    price=db.Column(db.Float(precision=2)) #sets 2 decimal places

    store_id=db.Column(db.Integer, db.ForeignKey('stores.id'))
    store=db.relationship('StoreModel')

    def __init__(self, name, price, store_id) -> None:
        self.name=name
        self.price=price
        self.store_id=store_id

    def json(self):
        return({'name':self.name, 'price':self.price})

    @classmethod
    def find_by_name(cls, name):
        return ItemModel.query.filter_by(name=name).first() #Select select * From ItemModel (table) Where name=name limit 1

    def save_to_db(self): #both inserts and updates...upserting
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()