from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

import models
from models import ToDos
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Open a database connection then closing it afterwards
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Opens up db connection as a dependency injection
db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/', status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(ToDos).all()

@app.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_one(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f'Todo with id {todo_id} does not exist')
