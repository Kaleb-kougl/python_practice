from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


# inheritance
class Item(Resource):
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


class Items(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items/")

app.run(port=5000, debug=True)
