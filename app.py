from common.exceptions import UserNotFoundError
from flask import Flask, jsonify, request, Response
from flaskext.mysql import MySQL
from dotenv import load_dotenv
from common.user import get_user, get_users, auth
from common.exceptions import UserNotFoundError
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


@app.get("/users/<username>")
def get_user_path(username):
    try:
        user = get_user(mysql, username)
        return jsonify(user.json())
    except UserNotFoundError:
        return "User not found", 400


@app.post("/auth")
def auth_path():
    json = request.get_json()
    username = json["username"]
    password = json["password"]

    try:
        user = get_user(mysql, username)
    except UserNotFoundError:
        return "User not found", 400

    authenticated = auth(user, password)
    if authenticated:
        return Response(status=200)
    else:
        return Response(status=401)


if __name__ == "__main__":
    app.run()
