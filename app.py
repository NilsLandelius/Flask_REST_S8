import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.item import Item, ItemList
from resources.user import UserRegister, User, UserLogin
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPOGATE_EXCEPTIONS'] = True
app.secret_key = 'nils'
api = Api(app)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: #This needs to be changed from hard-coded to a DB check or config-file
        return {'is_admin': True}
    return {'is_admin': False}

api.add_resource(Store,'/api/store/<string:name>')
api.add_resource(StoreList,'/api/stores')
api.add_resource(ItemList,'/api/items')
api.add_resource(Item,'/api/item/<string:name>')
api.add_resource(UserRegister,'/api/register')
api.add_resource(User,'/api/user/<int:user_id>')
api.add_resource(UserLogin,'/api/auth' )

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)