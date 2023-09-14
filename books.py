from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'title': "Book 1", 'author': "Author 1", 'genre': "Genre 1"},
    {'title': "Book 2", 'author': "Author 2", 'genre': "Genre 2"},
    {'title': "Book 3", 'author': "Author 3", 'genre': "Genre 3"},
    {'title': "Book 4", 'author': "Author 4", 'genre': "Genre 4"},
    {'title': "Book 5", 'author': "Author 5", 'genre': "Genre 5"},
    {'title': "Book 6", 'author': "Author 6", 'genre': "Genre 6"},
]


@app.get('/books')
async def read_all_books():
    return BOOKS
