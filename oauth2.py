from datetime import datetime, timedelta, timezone
from fastapi import  Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import schemas
from database import get_db
import models
from config import settings


oAuth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.token_expire_minute)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_access_token(token:str,credential_exceptions):

    try:

        payload = jwt.decode(token,settings.secret_key, algorithms= [settings.algorithm])

        id = payload.get("user_id")

        if id is None:
            raise credential_exceptions

        token_data = schemas.TokenData(id=id)
    
    except jwt.PyJWTError:
        raise credential_exceptions

    return token_data

def get_current_user(token: str = Depends(oAuth2_scheme), db= Depends(get_db)):

    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token,credentials_exception)

    user = db.query(models.users).filter(models.users.id == token.id).first()

    return user

