from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'title': "Book 2", 'author': 'Author 2', 'genre': "Genre 2"},
    {'title': "Book 2", 'author': "Author 2", 'genre': "Genre 2"},
    {'title': "Book 3", 'author': "Author 3", 'genre': "Genre 3"},
    {'title': "Book 4", 'author': "Author 2", 'genre': "Genre 4"},
    {'title': "Book 5", 'author': "Author 5", 'genre': "Genre 5"},
    {'title': "Book 6", 'author': "Author 6", 'genre': "Genre 6"},
]


@app.get('/books')
async def read_all_books():
    return BOOKS


@app.get('/books/{book_title}')
async def read_all_books(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


@app.get('/books/')
async def read_genre_by_query(genre: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('genre').casefold() == genre.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_genre_by_query(book_author: str, genre: str):
    books_to_return = []
    for book in BOOKS:
        if (book.get('author').casefold() == book_author.casefold() \
                and book.get('genre').casefold() == genre.casefold()):
            books_to_return.append(book)
    return books_to_return
