import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


# inheritance
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        row = self.find_by_name(name)
        if row:
            return {"item": {"name": row[0], "price": row[1]}}, 200
        return {"message": "Item not found"}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        return row

    def post(self, name):
        row = self.find_by_name(name)
        if row:
            return {"Message": "An item with name {} already exists".format(name)}, 400
        # if no errors then load the data
        data = Item.parser.parse_args()
        print(data["price"])

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (name, data["price"]))

        connection.commit()
        connection.close()

        return {"name": name, "price": data["price"]}, 201

    @jwt_required()
    def delete(self, name):
        row = self.find_by_name(name)
        if row is None:
            return {"Message": "No item with name {} exists".format(name)}, 404

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {"Message": "{} was deleted from the db".format(name)}, 200

    """
    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item
    """


class Items(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items"

        result = cursor.execute(query)

        connection.commit()

        if result:
            index = 0
            data = {}
            for row in result:
                data[index] = row
                index += 1
            connection.close()
            return data
        return {"message": "No items in the db"}
