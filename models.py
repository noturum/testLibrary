from pydantic import BaseModel

class Book(BaseModel):
    title: str
    year: int
    author: str

class Department(BaseModel):
    name: str

class Visitor(BaseModel):
    name: str
class BookFilter(BaseModel):
    title:str|None
    author:str|None
    year:int|None
    isAvailable:bool|None