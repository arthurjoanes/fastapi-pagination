<h1 align="center">
<img alt="logo" src="https://raw.githubusercontent.com/uriyyo/fastapi-pagination/main/docs/img/logo.png">
</h1>

<div align="center">
<img alt="license" src="https://img.shields.io/badge/License-MIT-lightgrey">
<img alt="test" src="https://github.com/uriyyo/fastapi-pagination/workflows/Test/badge.svg">
<img alt="codecov" src="https://codecov.io/gh/uriyyo/fastapi-pagination/branch/main/graph/badge.svg?token=QqIqDQ7FZi">
<a href="https://pepy.tech/project/fastapi-pagination"><img alt="downloads" src="https://pepy.tech/badge/fastapi-pagination"></a>
<a href="https://pypi.org/project/fastapi-pagination"><img alt="pypi" src="https://img.shields.io/pypi/v/fastapi-pagination"></a>
</div>

## Introduction

`fastapi-pagination` adds page-based and cursor-based pagination to FastAPI endpoints.
It provides request parameters, response models and integrations for SQL and NoSQL databases,
including `SQLAlchemy`, `Tortoise ORM` and `PyMongo`.

The library supports synchronous and asynchronous code and requires Python 3.10 or later.

----

See the [documentation](https://uriyyo-fastapi-pagination.netlify.app/) for database integrations and customization.

---

## Installation

```bash
pip install fastapi-pagination
```

## Quickstart

Register pagination with `add_pagination(app)`, annotate the endpoint with `Page[YourModel]`,
and pass the data to `paginate`.

```py
from fastapi import FastAPI
from pydantic import BaseModel, Field

# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination, paginate

app = FastAPI()  # create FastAPI app
add_pagination(app)  # important! add pagination to your app


class UserOut(BaseModel):  # define your model
    name: str = Field(..., example="Steve")
    surname: str = Field(..., example="Rogers")


users = [  # create some data
    UserOut(name="Steve", surname="Rogers"),
    # ...
]


# req: GET /users
@app.get("/users")
async def get_users() -> Page[UserOut]:
    # use Page[UserOut] as return type annotation
    return paginate(users)  # use paginate function to paginate your data
```

The default `paginate` function requires all data in memory. For database queries, use the matching
integration so pagination runs in the database. For example, SQLAlchemy uses
`paginate` from `fastapi_pagination.ext.sqlalchemy`:

```python
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate


@app.get("/users")
def get_users(db: Session = Depends(get_db)) -> Page[UserOut]:
    return paginate(db, select(User).order_by(User.created_at))
```

---

The quickstart generates this OpenAPI schema:

<div align="center">
<img alt="app-example" src="https://raw.githubusercontent.com/uriyyo/fastapi-pagination/main/docs/img/example.png">
</div>
