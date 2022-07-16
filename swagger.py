from marshmallow import Schema, fields

###用戶相關###
class UserPostRequest(Schema):
    name = fields.Str(doc="name", required=True)
    gender = fields.Str(doc="gender", required=True)
    birth = fields.Str(doc="birth", required=True)
    account=fields.Str(doc="account", required=True)
    password=fields.Str(doc="password", required=True)
    note = fields.Str(doc="note")

class UserPatchRequest(Schema):
    name = fields.Str(doc="name")
    gender = fields.Str(doc="gender")
    birth = fields.Str(doc="birth")
    account=fields.Str(doc="account", required=True)
    password=fields.Str(doc="password", required=True)
    note = fields.Str(doc="note")

class UserDeleteRequest(Schema):
    name = fields.Str(doc="name")
    account=fields.Str(doc="account", required=True)
    password=fields.Str(doc="password", required=True)


# Response
class UserCommonResponse(Schema):
    message = fields.Str(example="success")


class UserGetResponse(UserCommonResponse):
    data = fields.List(
        fields.Dict(), 
        example={
            "id": 1,
            "name": "name",
            "gender": "male",
            "birth": "1970/01/01",
            "note": ""
        }
    )
    datetime = fields.Str()

class LoginReqest(Schema):
    account = fields.Str(doc="account", required=True)
    password = fields.Str(doc="password", required=True)


###產品相關###
class Productlistrequest(Schema):
    name = fields.Str(doc="name")
    
#response
class ProductGetResponse(Schema):
    data = fields.List(fields.Dict())


###購物車相關###

class CartListRequest(Schema):
    name = fields.Str(example="string") 

class CartPostRequest(Schema):
    name = fields.Str(doc="name", example="string", required=True)
    count = fields.Int(doc="count", example="string", required=True)


class CartDeleteRequest(Schema):
    name = fields.Str(example="string", required=True)

#response
class CartGetResponse(Schema):
    data = fields.List(fields.Dict())


