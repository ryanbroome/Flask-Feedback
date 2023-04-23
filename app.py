from flask import Flask, request, jsonify, render_template
from models import db, connect_db
import bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///resource_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super-sized-secret"

connect_db(app)


@app.route("/")
def show_base():
    return render_template("base.html")
