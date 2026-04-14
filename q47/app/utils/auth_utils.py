import bcrypt
import jwt


def hash_password(password):
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt())

def check_password(password,hashed_password):
    return bcrypt.checkpw(password.encode(),hashed_password)

def generate_access_token(payload):
    return jwt.encode(payload,"This_is_my_highly_secret_key",["HS256"])
