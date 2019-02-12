import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        findUser = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(findUser, (username,))
        userRow = result.fetchone()
        if userRow:
            # passes them as positional arguments
            user = cls(*userRow)
        else:
            user = None

        connection.close()

        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        findUser = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(findUser, (_id,))
        userRow = result.fetchone()
        if userRow:
            # passes them as positional arguments
            user = cls(*userRow)
        else:
            user = None

        connection.close()

        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data["username"]):
            return {"message": "A user with that username already exists"}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        # NULL as the id because it will auto_increment
        query = "INSERT INTO users VALUES(NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"]))

        connection.commit()
        connection.close()

        return {"message": "user created successfully"}, 201
