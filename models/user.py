from db import db

class UserModel(db.Model): #tells SQLAlchemy entity that user model are things that we are going to be saving to and retrieving from a db and creates mapping between the db and the objects

    __tablenmae__="users"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80)) #80 is a limit to the length of the string
    password=db.Column(db.String(80))

    def __init__(self, username, password) -> None:
        self.username=username
        self.password=password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()