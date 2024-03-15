from app.models import Visitor, Department, Book, BookFilter, GiveBook
from app.DataBaseController import database_controller as db, TVisitors, TBooks, TDepartments, books_on_visitors, select
from fastapi_filter import FilterDepends

from fastapi import FastAPI

app = FastAPI()


@app.get("/visitors/count_books")
async def read_root():
    visitors = db.select(TVisitors)
    return [{visitor.name: len(visitor.books) for visitor in visitors}]


@app.get("/visitors/{visitor_id}")
async def get_visitor(visitor_id: int):
    visitor = db.select(TVisitors, [TVisitors.id_visitor == visitor_id], one=True)
    return {"name": visitor.name, 'books': visitor.books}


@app.post('/books/give')
def give_book(data: GiveBook):
    book = db.select(TBooks, [TBooks.id_book == data.id_book], one=True)
    if book.count > 0:
        db.insert(books_on_visitors, id_book=data.id_book, id_visitor=data.id_visitor)
        db.update(TBooks, [TBooks.id_book == book.id_book], count=book.count - 1)
        return {"status": "ok"}
    else:
        return {"status": "not a book"}


@app.post('/visitors')
async def add_visitor(visitor: Visitor):
    if db.insert(TVisitors, name=visitor.name):
        return {"status": "ok"}
    else:
        return {"status": "error"}


@app.post('/departments')
async def add_department(department: Department):
    if db.insert(TDepartments, name=department.name):
        return {"status": "ok"}
    else:
        return {"status": "error"}


@app.get('/departments')
async def get_department():
    return {"deparment": db.select(TDepartments)}


@app.post('/books')
async def add_book(book: Book):
    if db.insert(TBooks, title=book.title,
                 year=book.year,
                 author=book.author,
                 id_department=book.id_department):
        return {"status": "ok"}
    else:
        return {"status": "error"}


@app.get('/books')
def filter_book(filter: BookFilter = FilterDepends(BookFilter)):
    if filter.isAviable == 'True':
        filter.__delattr__('isAviable')
        filter.__setattr__('count__gt', 0)
    [filter.__delattr__(field[0]) for field in filter if field[1] == '*']
    query = filter.filter(select(TBooks))
    books = db.session.execute(query).all()

    return {'res': [book[0] for book in books]}
