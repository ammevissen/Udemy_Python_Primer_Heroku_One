from db import db

class StoreModel(db.Model): #tells SQLAlchemy entity that Item model are things that we are going to be saving to and retrieving from a db and creates mapping between the db and the objects

    __tablename__='stores'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80))
   
    items=db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name) -> None:
        self.name=name

    def json(self):
        return({'name':self.name, 'items':[item.json() for item in self.items.all()]}) #lazy=dynamic means it will not be loaded until called, so need the .all() to call that table

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #Select select * From ItemModel (table) Where name=name limit 1

    def save_to_db(self): #both inserts and updates...upserting
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()