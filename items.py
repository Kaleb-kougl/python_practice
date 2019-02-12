import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


# inheritance
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        return row

    @classmethod
    def insert_item(cls, name, price):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (name, price))

        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        row = self.find_by_name(name)
        if row:
            return {"item": {"name": row[0], "price": row[1]}}, 200
        return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        row = self.find_by_name(name)
        if row:
            return {"Message": "An item with name {} already exists".format(name)}, 400
        # if no errors then load the data
        data = Item.parser.parse_args()
        try:
            Item.insert_item(name, data["price"])
        except:
            return {"message": "something went wrong inserting the item"}, 500

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

    @jwt_required()
    def put(self, name):
        row = self.find_by_name(name)
        data = Item.parser.parse_args()
        if row is None:
            try:
                Item.insert_item(name, data["price"])
            except:
                return {"message": "Something went wrong inserting the item"}, 500
        else:
            try:
                self.update_item(data["price"], name)
            except:
                return {"message": "Something wen wrong trying to update the item"}, 500
        return {"name": name, "price": data["price"]}, 201

    @classmethod
    def update_item(cls, price, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (price, name))
        connection.commit()
        connection.close()


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
