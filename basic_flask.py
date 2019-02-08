from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome home!"


app.run(port=5000)
