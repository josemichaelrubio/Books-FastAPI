from typing import Annotated

from fastapi import Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from models import Users
from database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

# TODO: here is where I left off. Add hash functionality to this router

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


class UserRequest(BaseModel):
    username: str
    hashed_password: str


@router.get('/users/{user_id}', status_code=status.HTTP_200_OK)
async def read_user(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    user_model = db.query(Users).filter(Users.id == user_id).filter(Users.id == user.get('id')).first()
    if user_model is not None:
        return user_model
    raise HTTPException(status_code=404, detail=f'User with id {user_id} does not exist')


@router.put("/users/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user_password(user: user_dependency, db: db_dependency, user_request: UserRequest,
                               user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    user_model = db.query(Users).filter(Users.id == user_id).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f'Todo with id {user_id} does not exist')
    user_model.username = user_request.username
    user_model.hashed_password = user_request.hashed_password
    db.add(user_model)
    db.commit()
