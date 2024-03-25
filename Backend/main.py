from flask import Flask

app = Flask(__name__)


@app.route("/load", methods=['POST'])
def load():
    return "Data loaded successfully!"
