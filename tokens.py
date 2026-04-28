from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
import schemas,models
SECRET_KEY = "1f780b8e5c365ab4b787095983a5a28da33880b7117ead97a1a0d535a7e696e0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception, db):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        if username is None:
            raise credentials_exception

        user = db.query(models.User).filter(models.User.username == username).first()

        if user is None:
            raise credentials_exception

        return user

    except jwt.PyJWTError:
        raise credentials_exception