import flask
from flask_restful import Api
from model.user import User, Login, Register
from model.product import products
from model.cart import cart
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin 
from flask_apispec.extension import FlaskApiSpec 
from flask_jwt_extended import JWTManager 
from flask import Flask,render_template 


app = flask.Flask(__name__,template_folder='D:/python/api/ws/templates')


api = Api(app)

app.config["DEBUG"] = True
app.config["JWT_SECRET_KEY"]="secret_key"
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='APISHOP PROJECT',
        version='DV102',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)





#ShopGuide URL(商城導覽)
@app.route('/')
def index():
        return render_template('index.html')


# Register URL(用戶註冊)
api.add_resource(Register, "/register",methods=['POST'])
docs.register(Register)

# Login URL(用戶登入並取得token)
api.add_resource(Login, "/login")
docs.register(Login)

# User URL(更改用戶資訊)
api.add_resource(User, "/user")
docs.register(User) 

# Cart URL(購物車)
api.add_resource(cart, "/cart")
docs.register(cart)

# Product URL(產品)
api.add_resource(products, "/product")
docs.register(products)



if __name__ == "__main__":
    jwt = JWTManager().init_app(app)
    app.run(debug=True, port=5000, host="localhost")