from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "Kaleb"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # creates a new endpoint called '/auth'

items = []


# inheritance
class Item(Resource):
    @jwt_required()
    def get(self, name):
        # request_data = request.data
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"Message": "An item with name {} already exists".format(name)}, 400
        item = {"name": name, "price": 12.00}
        items.append(item)
        return item, 201

    def delete(self, name):
        # python will think you're using a local var unless specified as such
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "{} was deleted".format(name)}

    def put(self, name):
        data = request.json()
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
