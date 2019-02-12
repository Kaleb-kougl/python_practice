from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from user import UserRegister
from security import authenticate, identity
from items import Items, Item

app = Flask(__name__)
app.secret_key = "Kaleb"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # creates a new endpoint called '/auth'

api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items/")
api.add_resource(UserRegister, "/register")

# this is so that if we import from this file it would auto kick up the server
if __name__ == "__main__":
    app.run(port=5000, debug=True)
