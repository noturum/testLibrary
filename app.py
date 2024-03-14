
from models import Visitor, Department, Book, BookFilter
from DataBaseController import database_controller as db, TVisitors, TBooks, TDepartments

from fastapi import FastAPI

app = FastAPI()


@app.get("/visitors/count_books")
async def read_root():
    visitors = db.select(TVisitors)
    return [{visitor.name: len(visitor.books) for visitor in visitors}]


@app.get("/visitors/{visitor_id}")
async def get_visitor(visitors_id: int):
    visitor = db.select(TVisitors, [TVisitors.id_visitor == visitors_id], one=True)
    return visitor


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
    if db.insert(TBooks, title=book.title, year=book.year, author=book.author):
        return {"status": "ok"}
    else:
        return {"status": "error"}
@app.post('/books')
def filter_book(filter:BookFilter):
    return '12'