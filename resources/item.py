from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel


class ItemList(Resource):
    def get(self):       
        return {'items':[item.json() for item in ItemModel.query.all()]} 

class Item(Resource):
        parser = reqparse.RequestParser()
        @jwt_required()
        def get(self,name):
            item = ItemModel.find_by_name(name)
            if item:
                return item.json()
            return {'message': 'The item does not exist'}, 404

        def post(self,name):
            self.parser.add_argument('price', type=float,default=0.0)
            self.parser.add_argument('store_id',type=int,required=True,help='Every item need a store id')
            if ItemModel.find_by_name(name):
                return{'message':"An item with name {} already exists.".format(name)}, 400

            data = self.parser.parse_args()    
            item = ItemModel(name,data['price'],data['store_id'])

            try:
                item.save_to_db()
            except:
                return {'message': 'An error occured inserting the item'}, 500
            
            return item.json(), 201
        
        def delete(self, name):
            item = ItemModel.find_by_name(name)
            if item:
                item.delete_from_db()
            
            return {'message':'Item deleted'}
                


        def put(self,name):
            Item.parser.add_argument('price',
                type=float,
                required=True,
                help= "This field cannot be left blank"
            )
            Item.parser.add_argument(
                'store_id',
                type=int,
                required=False,
                help='Every item need a store id'
            )
            data = Item.parser.parse_args()
            item = ItemModel.find_by_name(name)
            if item is None:
                item =ItemModel(name,**data)
            else:
                for x in data.keys():
                    if data[x] is not None and x in item.__dict__:
                        item.query.filter_by(name=name).update({x:data[x]})
            item.save_to_db()
            return item.json()