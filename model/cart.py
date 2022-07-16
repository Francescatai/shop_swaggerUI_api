import pymysql
from swagger import *
import util
from flask_apispec import doc, use_kwargs, MethodResource, marshal_with 
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


class cart(MethodResource):
##查看購物車##(get)
    @doc(description='查詢購物車內容，不輸入可以查詢全部', tags=['Cart'])
    @use_kwargs(CartListRequest, location="form") 
    @marshal_with(CartGetResponse, code=200)
    @jwt_required() 
    def get(self,**kwargs):
        db, cursor = db_init()

        name = kwargs.get("name") 
        if name == None:
            sql = sql = 'SELECT NAME,PRICE,COUNT,(COUNT*PRICE) TOTAL FROM apishop.cart;'
        elif name !=None:
            sql = f"SELECT NAME,PRICE,COUNT,(COUNT*PRICE) TOTAL FROM apishop.cart WHERE name like '%{name}%';"          

        result = cursor.execute(sql)
        if result == None:
            return util.failure()
        else:  
            all = cursor.fetchall()
            totalprice = 0
            for i in all:
                totalprice += i["COUNT"] * i["PRICE"]
            all.append({"總金額": totalprice})

        db.close()
        return util.success(all)

##更改購物車##(post)
    @doc(description="添加或更新購物車商品", tags=["Cart"])
    @use_kwargs(CartPostRequest, location="form")
    @marshal_with(CartGetResponse, code=200)
    @jwt_required()
    def post(self,**kwargs):
        db, cursor = db_init()

        name=kwargs.get("name")
        count=kwargs.get("count")

        sql = "SELECT * FROM apishop.product WHERE name = '{}';".format(name)
        cursor.execute(sql)
        result = cursor.fetchall()
        if result == ():
            db.close()
            return ({"message": "無此商品"})

        sql = """
        SELECT * FROM apishop.cart WHERE name = '{}'
        """.format(name)
        result = cursor.execute(sql)
        if result == 0:
            sql = """
            INSERT INTO apishop.cart (name,count,price)
            VALUES ('{}','{}',(select price from apishop.product where name='{}'))
            """.format(name,count,name)
        else:
            sql = """
            UPDATE apishop.cart SET count = '{}' WHERE name = '{}';
            """.format(count,name)

        result = cursor.execute(sql)
        db.commit()
        db.close()
        return util.success()
    
    ##刪除購物車##(delete)
    @doc(description='刪除購物車商品', tags=['Cart']) 
    @use_kwargs(CartDeleteRequest, location="form")
    @marshal_with(CartGetResponse, code=200) 
    @jwt_required() 
    def delete(self,name):
        db, cursor = db_init()
        
        sql = "DELETE FROM apishop.cart WHERE name = '{}';".format(name)
        cursor.execute(sql)
        db.commit()
        db.close()
        return util.success()


