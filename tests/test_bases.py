from typing import Generic, TypeVar

import pytest
from fastapi import Query

from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage, AbstractParams, BaseRawParams, RawParams
from fastapi_pagination.cursor import CursorParams

T = TypeVar("T")
C = TypeVar("C")


@pytest.mark.parametrize(
    ("total", "size", "pages"),
    [
        (0, 1, 0),
        (100, 100, 1),
        (101, 100, 2),
        (9007199254740993, 1, 9007199254740993),
        (9007199254740993, 2, 4503599627370497),
        (9223372036854775807, 100, 92233720368547759),
        (10**400, 100, 10**398),
    ],
    ids=["empty", "exact-page", "partial-page", "large-total", "large-remainder", "int64-max", "beyond-float"],
)
def test_page_count_preserves_integer_precision(total, size, pages):
    page = Page[int].create([], Params(size=size), total=total)

    assert page.total == total
    assert page.pages == pages


def test_zero_size():
    class CustomParams(Params):
        size: int | None = Query(0)

    class CustomPage(Page[T], Generic[T]):
        size: int | None = None

        __params_type__ = CustomParams

    res = CustomPage[int].create(
        [],
        CustomParams(),
        total=0,
    )

    assert res.dict() == {
        "items": [],
        "page": 1,
        "pages": 0,
        "size": 0,
        "total": 0,
    }


def test_invalid_params_cast():
    with pytest.raises(ValueError, match=r"^Not a 'limit-offset' params$"):
        CursorParams().to_raw_params().as_limit_offset()

    with pytest.raises(ValueError, match=r"^Not a 'cursor' params$"):
        Params().to_raw_params().as_cursor()


def test_params_cast():
    p = CursorParams().to_raw_params()

    assert p.as_cursor() is p

    p = Params().to_raw_params()

    assert p.as_limit_offset() is p


def test_page_type_is_not_reinited():
    class _Params(AbstractParams):
        def to_raw_params(self) -> BaseRawParams:
            return RawParams()

    assert _Params.__page_type__ is None

    class _FirstPage(AbstractPage[int]):
        __params_type__ = _Params

    assert _FirstPage.__params_type__ is _Params
    assert _Params.__page_type__ is _FirstPage

    class _SecondPage(AbstractPage[int]):
        __params_type__ = _Params

    assert _SecondPage.__params_type__ is _Params

    # page is not re-inited for params
    assert _Params.__page_type__ is _FirstPage

    _Params.set_page(_SecondPage)

    assert _Params.__page_type__ is _SecondPage
    assert _SecondPage.__params_type__ is _Params

    _FirstPage.set_params(_Params)

    assert _FirstPage.__params_type__ is _Params
    assert _Params.__page_type__ is _FirstPage
    assert _SecondPage.__params_type__ is _Params
