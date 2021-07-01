from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from dotenv import load_dotenv
from common.user import get_user, get_users, auth
import os

load_dotenv()

app = Flask(__name__)
mysql = MySQL()
app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_DATABASE_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("MYSQL_PASS")
app.config["MYSQL_DATABASE_DB"] = os.getenv("MYSQL_DB")
mysql.init_app(app)


@app.get("/")
def index_path():
    return "👋", 200


@app.get("/users")
def users_path():
    users = get_users(mysql)
    return jsonify(users.json())


@app.get("/user/<username>")
def get_user_path(username):
    user = get_user(mysql, username)
    return jsonify(user.json())


@app.post("/auth/<username>")
def auth_path(username):
    password = request.get_json()["password"]
    user = get_user(mysql, username)
    authenticated = auth(user, password)
    if authenticated:
        return "OK"
    else:
        return "Failed"


if __name__ == "main":
    app.run()
