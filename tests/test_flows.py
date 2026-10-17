import pytest

from fastapi_pagination import set_page
from fastapi_pagination.cursor import CursorPage, CursorParams
from fastapi_pagination.flow import flow_expr, run_async_flow, run_sync_flow
from fastapi_pagination.flows import generic_flow


@pytest.mark.parametrize("callable_data", [False, True], ids=["dictionary", "callable"])
def test_cursor_flow_does_not_mutate_additional_data(callable_data):
    metadata = {"label": "shared"}
    additional_data = (lambda _: metadata) if callable_data else metadata

    with set_page(CursorPage[int]):
        page = run_sync_flow(
            generic_flow(
                cursor_flow=flow_expr(lambda _: ([1], {"next_": "next"})),
                total_flow=flow_expr(lambda: 2),
                params=CursorParams(size=1),
                additional_data=additional_data,
            )
        )

    assert page.items == [1]
    assert page.next_page == "bmV4dA%3D%3D"
    assert metadata == {"label": "shared"}


@pytest.mark.asyncio
async def test_async_cursor_flow_does_not_mutate_callback_result():
    metadata = {"label": "shared"}

    async def additional_data(_):
        return metadata

    with set_page(CursorPage[int]):
        page = await run_async_flow(
            generic_flow(
                cursor_flow=flow_expr(lambda _: ([1], {"next_": "next"})),
                total_flow=flow_expr(lambda: 2),
                params=CursorParams(size=1),
                additional_data=additional_data,
                async_=True,
            )
        )

    assert page.items == [1]
    assert page.next_page == "bmV4dA%3D%3D"
    assert metadata == {"label": "shared"}
