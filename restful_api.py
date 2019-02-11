from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "Kaleb"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # creates a new endpoint called '/auth'

items = []


# inheritance
class Item(Resource):
    parser = reqparse.RequestParser()
        parser.add_argument(
            "price", type=float, required=True, help="This field cannot be left blank!"
        )

    @jwt_required()
    def get(self, name):
        # request_data = request.data
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        #first make sure that there are no errors
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"Message": "An item with name {} already exists".format(name)}, 400
        #if no errors then load the data
        data = Item.parser.parse_args()
        item = {"name": name, "price": price || 12.99}
        items.append(item)
        return item, 201

    def delete(self, name):
        # python will think you're using a local var unless specified as such
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "{} was deleted".format(name)}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item


class Items(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items/")

app.run(port=5000, debug=True)
