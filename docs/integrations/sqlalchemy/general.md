`sqlalchemy` is one of the most popular database libraries for Python.
It is an ORM (Object Relational Mapper) that abstracts the database layer and provides a Pythonic way
to interact with the database. SQLAlchemy supports a wide range of databases, including
SQLite, MySQL, PostgreSQL, and Oracle.

`fastapi-pagination` provides `paginate` for synchronous queries and `apaginate` for asynchronous queries.

## Installation

Install the SQLAlchemy integration:

```bash
pip install "fastapi-pagination[sqlalchemy]"
```

For `apaginate`, also install [SQLAlchemy's asyncio extra](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#asyncio-platform-installation-notes-including-apple-m1)
and an asynchronous driver. For example, SQLite uses `aiosqlite`:

```bash
pip install "SQLAlchemy[asyncio]" aiosqlite
```

The `asyncio` extra supplies `greenlet`, which SQLAlchemy's asynchronous engine and session require.
Pass an `AsyncSession` or `AsyncConnection` to `apaginate` and await its result.

## Synchronous example

```py
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, Session, mapped_column

from fastapi_pagination import set_params, set_page, Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate

engine = create_engine("sqlite:///:memory:")


class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(default=None, primary_key=True)

    name: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()


with Session(engine) as session:
    Base.metadata.create_all(session.bind)

    session.add_all(
        [
            User(name="John", age=25),
            User(name="Jane", age=30),
            User(name="Bob", age=20),
        ],
    )
    session.commit()

set_page(Page[User])
set_params(Params(size=10))

page = paginate(session, select(User))
print(page.model_dump_json(indent=4))
```
