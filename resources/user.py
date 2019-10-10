import sqlite3
from blacklist import BLACKLIST
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_claims,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
    )
from flask_restful import Resource, reqparse
from models.user import UserModel



class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',required=True, type=str, help="This field cannot be blank")
    parser.add_argument('password',type=str,default='password')

    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message':'User already exists'}, 400
        
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User was created successfully"}, 201

class User(Resource):
    
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    
    @classmethod
    @jwt_required
    def delete(cls,user_id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message':'You don\'t have admin privileges'}, 401
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message':'User was deleted'}

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',required=True, type=str, help="This field cannot be blank")
    parser.add_argument('password',type=str,default='password')

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        
        return {'message':'Invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] # JTI is the JWT ID, a unique identifier for a JWT
        BLACKLIST.add(jti)
        return {'message':'You are logged out'}, 200

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh=False)
        return {
            'access_token': new_token
        }, 200