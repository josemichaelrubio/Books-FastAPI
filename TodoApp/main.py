from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

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


@app.get('/')
async def read_all(db: db_dependency):
    return db.query(ToDos).all()
