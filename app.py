from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db #should be ok to import at the top

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db' #could be other types such as postgres
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #turns off Flask Alchemy tracker, but not the SQLAlchemy tracker (which is the better of the two) 
app.secret_key='jose' #if this was production code, would need this to be in a secure location (seperate)
api=Api(app)


@app.before_first_request
def create_tables():
    db.create_all() #will create the tables in the db file if they have not already been created

jwt=JWT(app, authenticate, identity) #creates an endpoint /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') #http://127.0.0.1:5000/student/studentName
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')



if __name__=='__main__':  #so only runs when this is the main file, not when this file is an imported file (__name__!=__main__)
    # from db import db #should be ok to import at the top
    db.init_app(app)
    
    app.run(port=5000, debug=True)

