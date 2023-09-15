from fastapi import FastAPI, Body

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
async def read_books(book_title: str):
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


@app.post('/books/create_book')
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put('/books/update_book')
async def update_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book


@app.delete('/books/delete_book/{book_title}')
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


# fetch all books from a specific author
@app.get('/author/{book_author}')
async def read_author_books(book_author: str):
    for book in BOOKS:
        author_books = []
        if book.get('author').casefold() == book_author.casefold():
            author_books.append(book)
        return author_books
