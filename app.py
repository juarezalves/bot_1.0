
from flask import Flask

App = Flask(__name__)

@pp.route("/")
def index():
    return "Olá mundo!"

@App.rout("/teste")
def index_nome:
    return "Olá methucu!"

if __name__ == "__main__":
    App.run(debug=True)