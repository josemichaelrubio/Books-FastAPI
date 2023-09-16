from fastapi import FastAPI

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

