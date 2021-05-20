from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
        
    parser=reqparse.RequestParser() #should just make into a function
    parser.add_argument('price', 
        type=float, 
        required=True, 
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id', 
        type=int, 
        required=True, 
        help="Ever item needs a store id!"
    )

    @jwt_required()
    def get(self, name):
        item=ItemModel.find_by_name(name)

        if item:
            return item.json()
            
        return {'message': "Item not found"}, 404

    def post(self, name):
        #error first approach, deal with possible errors first
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400 #bad request

        data=Item.parser.parse_args() #force=True, always process the request.  silent=True if invalid, just return None 
        item=ItemModel(name, **data)
        #print(item.json())
        try:
            #print("in post about to item.insert()")
            item.save_to_db()
        except:
            return{"message":"An error occurred inserting the item."}, 500 #internal server error
            
        return item.json(), 201 #created.  202 is accepted, for a delayed creation.


    def delete(self, name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message': 'Item deleted'}

    def put(self, name):
        data=Item.parser.parse_args() #parses the JSON payload #request.get_json()
        #print(data['another']) if try to print will get an error since, even if included in JSON payload, will be removed.

        item=ItemModel.find_by_name(name)

        if item is None:
            item=ItemModel(name, **data)
        else:
            item.price=data['price']
            item.store_id=data["store_id"]
            
        item.save_to_db()

        return item.json()




class ItemList(Resource):
    def get(self):        
        #more Pythonic
        return {'items':[item.json() for item in ItemModel.query.all()]}
        #alt: (better if working with people from other languages i.e. javaScript)
        #return {'items':list(map(lambda x: x.json(), ItemModel.query.all()))}
