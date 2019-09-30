import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.item import Item, ItemList
from security import authenticate, identity
from resources.user import UserRegister
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'nils'
app.config['JWT_AUTH_URL_RULE']='/api/auth'
api = Api(app)

jwt = JWT(app,authenticate,identity)

api.add_resource(Store,'/api/store/<string:name>')
api.add_resource(StoreList,'/api/stores')
api.add_resource(ItemList,'/api/items')
api.add_resource(Item,'/api/item/<string:name>')
api.add_resource(UserRegister,'/api/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)