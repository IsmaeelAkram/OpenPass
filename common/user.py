from flaskext.mysql import MySQL
from hashlib import sha512


class User:
    def __init__(self, id: int, name: str, sha512_password: str):
        self.id = id
        self.name = name
        self.sha512_password = sha512_password
        pass

    def json(self):
        return {"id": self.id, "username": self.name}


class Users:
    def __init__(self, users: list[User]):
        self.users = users

    def json(self):
        return [{"id": user.id, "username": user.name} for user in self.users]


def get_users(mysql: MySQL):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return Users([User(user[0], user[1], user[2]) for user in users])


def get_user(mysql: MySQL, name: str):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM users WHERE name=%s", name)
    user = cursor.fetchone()
    return User(user[0], user[1], user[2])


def auth(user: User, password: str):
    return sha512(password.encode("utf-8")).hexdigest() == user.sha512_password
