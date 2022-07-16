import pymysql
from flask import jsonify
from swagger import *
import util
from flask_apispec import doc, use_kwargs, MethodResource, marshal_with 
from flask_jwt_extended import create_access_token,jwt_required 
from datetime import timedelta




def db_init():
    db = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        port=3307,
        db='apishop'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

def get_access_token(account):
    global token
    token = create_access_token(
        identity={"account": account},
        expires_delta=timedelta(days=1)
    )
    return token



##註冊帳戶##
class Register(MethodResource):
    @doc(description='創建帳戶',tags=['Register'])
    @use_kwargs(UserPostRequest,location="form")
    @marshal_with(UserGetResponse,code=200)
    def post(self,**kwargs):
        db, cursor = db_init()


        user = {
            'name': kwargs['name'],
            'gender': kwargs['gender'],
            'birth': kwargs.get('birth') or '1900-01-01',
            'note': kwargs.get('note'),
            'account': kwargs.get('account'),
            'password': kwargs.get('password')
        }
        sql = """

            INSERT INTO apishop.user (name,gender,birth,account,password,note)
            VALUES ('{}','{}','{}','{}','{}','{}');

            """.format(
                user['name'], user['gender'],user['birth'], user['account'], user['password'],  user['note'])
            
            
        result = cursor.execute(sql)

        db.commit()
        db.close()

        if result ==1:
            return util.success()
        return util.failure({"message":"註冊失敗"})

##登入帳戶##
class Login(MethodResource):
    @doc(description='登入帳戶', tags=['Login'])
    @use_kwargs(LoginReqest, location="form")
    def post(self, **kwargs):
        db, cursor = db_init()
        account, password = kwargs["account"], kwargs["password"]
        sql = f"SELECT * FROM apishop.user WHERE account = '{account}' AND password = '{password}';"
        cursor.execute(sql)
        user = cursor.fetchall()
        db.close()

        if user !=None:
            token = get_access_token(account)
            data = {
                "message": f"Welcome back {user[0]['name']}",
                "token": token}
            return util.success(data)
        
        return util.failure({"message":"登入失敗"})

##用戶資料修改與刪除##
class User(MethodResource):
    @doc(description='更改用戶資料',tags=['UserInfo'])
    @use_kwargs(UserPatchRequest,location="form")
    @marshal_with(UserGetResponse,code=200)
    @jwt_required()
    def patch(self,account,password,**kwargs):
        db, cursor = db_init()
 
        user = {
            'name': kwargs.get('name'),
            'gender': kwargs.get('gender'),
            'birth': kwargs.get('birth'),
            'note': kwargs.get('note'),
            'account': kwargs.get('account'),
            'password': kwargs.get('password')
        }

        query = []
        for key, value in user.items():
            if value is not None:
                query.append(f"{key} = '{value}'")
        query = ",".join(query)
      
        sql = """
            UPDATE apishop.user
            SET {}
            WHERE account = {} and password={};
        """.format(query, account,password)

        result = cursor.execute(sql)
        message = "success" if result == 1 else "failure"
        db.commit()
        db.close()

        return jsonify({"message": message})

    @doc(description='刪除用戶',tags=['UserInfo'])
    @use_kwargs(UserDeleteRequest,location="form")
    @marshal_with(UserCommonResponse,code=200)
    @jwt_required
    def delete(self, account,password,**kwargs):
        db, cursor = db_init()

        user = {
            'name': kwargs.get('name'),
            'account': kwargs.get('account'),
            'password': kwargs.get('password')
        }

        sql = f'DELETE FROM apishop.user WHERE account = {account} and password={password};'
        result = cursor.execute(sql)
        message = "success" if result == 1 else "failure"
        db.commit()
        db.close()

        if result ==1:
            return util.success()
        return util.failure()

