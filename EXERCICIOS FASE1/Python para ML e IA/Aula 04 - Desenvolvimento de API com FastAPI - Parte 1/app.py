from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configuração do banco de dados SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


if __name__ == "__main__":
    app.run(debug=True)
