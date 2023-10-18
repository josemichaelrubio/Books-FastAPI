from typing import Annotated

from fastapi import Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from models import Users
from database import SessionLocal

from .auth import get_current_user

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = '59b320002b11581c550a250b771a6ed7763314c563bcc5f5db615a206fff3ad8'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

router = APIRouter(prefix='/users',
                   tags=['users']
                   )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class PhoneNumberRequest(BaseModel):
    phone_number: str


class UserRequest(BaseModel):
    password: str


@router.get('/current', status_code=status.HTTP_200_OK)
async def read_current_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/update_phone_number', status_code=status.HTTP_202_ACCEPTED)
async def update_phone_number(user: user_dependency, db: db_dependency, phone_request: PhoneNumberRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    phone_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if phone_model is None:
        raise HTTPException(status_code=404, detail=f'User does not exist')
    phone_model.phone_number = phone_request.phone_number
    db.add(phone_model)
    db.commit()


@router.put("/users", status_code=status.HTTP_202_ACCEPTED)
async def update_user_password(user: user_dependency, db: db_dependency, user_request: UserRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f'User does not exist')
    user_model.hashed_password = bcrypt_context.hash(user_request.password)
    db.add(user_model)
    db.commit()
