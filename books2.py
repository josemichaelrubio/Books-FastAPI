from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publication_date: int

    def __init__(self, id, title, author, description, rating, publication_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publication_date = publication_date


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    publication_date: int

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'New Book',
                'author': 'New Author',
                'description': 'D',
                'rating': 5,
                'publication_date': 2023
            }

        }


BOOKS = [
    Book(id=1, title="Python Cookbook", author="N1", description="Python Cookbook D", rating=5, publication_date=2023),
    Book(id=2, title="Python Cookbook 2", author="N2", description="Python Cookbook 2 D", rating=4,
         publication_date=2023),
    Book(id=3, title="Python Cookbook 3", author="N3", description="Python Cookbook 3 D", rating=4,
         publication_date=-100),
    Book(id=4, title="Python Cookbook 4", author="N4", description="Python Cookbook 4 D", rating=3,
         publication_date=1999),
    Book(id=5, title="Python Cookbook 5", author="N4", description="Python Cookbook 5 D", rating=1,
         publication_date=1999),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

@app.get("/books/publication-date/")
async def get_book_by_publication_date(publication_date: int):
    books_to_return = []
    for book in BOOKS:
        if book.publication_date == publication_date:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/rating/")
async def read_book_by_rating(rating: int= Query(gt=-1, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_by_id(new_book))


def find_book_by_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book


@app.put("/books/{book_id}/update")
async def update_book(book_id: int, book_request: BookRequest):
    book_change = False
    for book in BOOKS:
        if book.id == book_id:
            book.title = book_request.title
            book.author = book_request.author
            book.description = book_request.description
            book.rating = book_request.rating
            book.publication_date = book_request.publication_date
            book_change = True
    if not book_change:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
async def delete_book_by_id(book_id: int= Path(gt=0)):
    book_change = False
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)
            book_change = True
            return book
    if not book_change:
        raise HTTPException(status_code=404, detail="Book not found")
