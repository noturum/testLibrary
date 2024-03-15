import os
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import insert

load_dotenv()

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, delete, update, Engine, Table, select
from sqlalchemy.orm import Session, DeclarativeBase, relationship

DB = os.getenv('DB')
assert DB, 'init db string'


class Base(DeclarativeBase):
    ...


class TBooks(Base):
    __tablename__ = 'books'
    id_book = Column(Integer, autoincrement=True, index=True, primary_key=True)
    id_department = Column(ForeignKey('departments.id_department'))
    title = Column(String(40))
    author = Column(String(40))
    year = Column(Integer)
    count = Column(Integer, default=1)
    department = relationship('TDepartments')


class TDepartments(Base):
    __tablename__ = 'departments'
    id_department = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(20))


books_on_visitors = Table(
    "BooksOnVisitor",
    Base.metadata,
    Column("id_book", Integer, ForeignKey("books.id_book")),
    Column("id_visitor", Integer, ForeignKey("visitors.id_visitor")),
)


class TVisitors(Base):
    __tablename__ = 'visitors'
    id_visitor = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(20), )
    books = relationship('TBooks', secondary='BooksOnVisitor')


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

    def insert(self, table, **values) -> bool:
        """

        :param table: T<> для таблиц
        :param values: поля Т<> = значение
        :return: bool # успех транзакции
        """
        try:

            self.session.execute(insert(table).values(**values))
            self.session.commit()
            return True
        except Exception as e:
            print(e)
            self.session.rollback()
            return False

    def update(self, table, filter: list[bool], **values):
        """

        :param table: T<> для таблиц
        :param filter: лист T<>.value = value
        :param values: поля Т<> = значение
        :return: bool # успех транзакции
        """
        try:

            self.session.execute(update(table).where(*filter).values(**values))
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False

    def select(self, table, filter=[True], count=False, one=False):
        """

        :param table: T<>
        :param filter: лист T<>.value = value
        :param count: флаг для вывода колва
        :param one:  вернуть певый
        :return:
        """
        if count:
            return self.session.query(table).filter(*filter).count()
        else:
            return self.session.query(table).filter(*filter).one() if one else self.session.query(table).filter(
                *filter).all()

    def delete(self, table, filter: list):
        """

                :param table: T<> для таблиц
                :param filter: лист T<>.value = value
        """
        try:
            self.session.query(table).filter(*filter).delete()
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False


if __name__ != "__main__":
    database_controller = Database()
