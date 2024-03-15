from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field
from app.DataBaseController import TBooks


class Department(BaseModel):
    name: str


class Book(BaseModel):
    id_department: int
    title: str
    year: int
    author: str


class Visitor(BaseModel):
    name: str


class BookFilter(Filter):
    title: str | str = Field(default='*')
    author: str | str = Field(default='*')
    year: int | str = Field(default='*')
    count__gt: int | str = Field(alias='count', default=0)
    isAviable: bool | str = Field(default='*')

    class Constants(Filter.Constants):
        model = TBooks


class GiveBook(BaseModel):
    id_book: int
    id_visitor: int
