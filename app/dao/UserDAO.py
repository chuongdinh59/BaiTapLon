from app.models.index import *
import hashlib
def getUserById(user_id):
    return UserModel.query.get(user_id)

def verifyLogin(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return UserModel.query.filter(UserModel.username.__eq__(username.strip()),
                             UserModel.password.__eq__(password)).first()
    return None

