import os
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import insert

load_dotenv()

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, delete, update, text, select, Engine
from sqlalchemy.orm import Session, DeclarativeBase, relationship

DB = os.getenv('DB')
assert DB, 'init db string'


class Base(DeclarativeBase):
    ...


class TBooksOnVisitor(Base):
    __tablename__ ='books_on_visitor'
    id= Column(Integer,autoincrement=True,primary_key=True)
    id_book = Column(ForeignKey('books.id_book',ondelete="CASCADE"))
    id_visitor = Column(ForeignKey('visitors.id_visitor', ondelete="CASCADE"))

class TBooks(Base):
    __tablename__ = 'books'
    id_book = Column(Integer, autoincrement=True, index=True,primary_key=True)
    id_department = Column(ForeignKey('departments.id_department'))
    title = Column(String(40))
    author = Column(String(40))
    year = Column(Integer)
    count = Column(Integer)


class TDepartments(Base):
    __tablename__ = 'departments'
    id_department = Column(Integer, autoincrement=True,primary_key=True)
    name = Column(String(20))


class TVisitors(Base):
    __tablename__ = 'visitors'
    id_visitor = Column(Integer, autoincrement=True,primary_key=True)
    name = Column(String(20), )
    books = relationship('TBooksOnVisitor')


class Database():
    __inst__ = None

    def __new__(cls, *args, **kwargs):
        if not cls.__inst__:
            Base.metadata.create_all(create_engine(DB, echo=False))
            cls.__inst__ = super().__new__(cls)
        return cls.__inst__

    def __init__(self):
        self.__engine: Engine = create_engine(DB, echo=False)
        self.session = Session(self.__engine)

    def insert(self, table, returning=None, **values):
        try:
            if returning:
                returns = self.session.execute(insert(table).values(**values).returning(returning)).fetchone()
                self.session.commit()

                return returns
            else:

                self.session.execute(insert(table).values(**values))
                self.session.commit()
                return True
        except Exception as e:
            print(e)
            self.session.rollback()
            return False

    def update(self, table, filter, returning=None, **values):
        try:
            if returning:
                returns = self.session.execute(update(table).where(*filter).values(**values).returning(returning))
                self.session.commit()
                return returns
            else:
                self.session.execute(update(table).where(*filter).values(**values))
                self.session.commit()
                return True
        except Exception:
            self.session.rollback()
            return False

    def select(self, table, filter=(True,), count=False, one=False):
        if count:
            return self.session.query(table).filter(*filter).count()
        else:
            return self.session.query(table).filter(*filter).one() if one else self.session.query(table).filter(
                *filter).all()

    def delete(self, table, filter: list, returning=None):
        try:
            if returning:
                returns = self.session.execute(delete(table).returning(returning)).fetchone()
                self.session.commit()
                return returns
            else:
                self.session.query(table).filter(*filter).delete()
                self.session.commit()
                return True
        except Exception:
            self.session.rollback()
            return False


if __name__ != "__main__":
    database_controller = Database()
