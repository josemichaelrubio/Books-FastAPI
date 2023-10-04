from typing import Annotated

from fastapi import Depends, HTTPException, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from models import ToDos
from database import SessionLocal
from .auth import get_current_user

router = APIRouter()


# Open a database connection then closing it afterwards
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Opens up db connection as a dependency injection
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# Pydantics post request with body of a to do
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool
    # No id because it is auto generated. SQLacemdy does it for us.


@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(ToDos).filter(ToDos.owner_id == user.get('id')).all()


@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_one(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f'Todo with id {todo_id} does not exist')


@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    todo_model = ToDos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f'Todo with id {todo_id} does not exist')
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f'Todo with id {todo_id} does not exist')
    db.delete(todo_model)
    db.commit()
