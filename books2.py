from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)


BOOKS = [
    Book(id=1, title="Python Cookbook", author="N1", description="Python Cookbook D", rating=5),
    Book(id=2, title="Python Cookbook 2", author="N2", description="Python Cookbook 2 D", rating=4),
    Book(id=3, title="Python Cookbook 3", author="N3", description="Python Cookbook 3 D", rating=4),
    Book(id=4, title="Python Cookbook 4", author="N4", description="Python Cookbook 4 D", rating=3),
    Book(id=5, title="Python Cookbook 5", author="N4", description="Python Cookbook 5 D", rating=1),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_by_id(new_book))


def find_book_by_id(book: Book):
    if len(BOOKS) == 0:
        book.id = Books[-1].id + 1
    else:
        book.id = 1
    return book
