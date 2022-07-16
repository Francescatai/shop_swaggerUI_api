import pymysql
import util
from flask_apispec import doc, use_kwargs, MethodResource, marshal_with 
from swagger import *
from flask_jwt_extended import jwt_required 



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

##查看產品清單##
class products(MethodResource):
    @doc(description='不輸入品名直接查詢全部產品清單', tags=['ProductList']) 
    @use_kwargs(Productlistrequest, location="query") 
    @marshal_with(ProductGetResponse, code=200)
    @jwt_required() 
    def get(self, **kwargs):
        db, cursor = db_init()

        name = kwargs.get("name") 
        if name == None:
            sql = "SELECT * FROM apishop.product ;"
        else:
            sql = "SELECT * FROM apishop.product WHERE name = '%{}%';".format(name)          
 
        cursor.execute(sql)
        plist = cursor.fetchall()
        db.close()
        return util.success(plist)
