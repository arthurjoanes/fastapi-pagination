from contextlib import aclosing

import pytest
from sqlalchemy import event, text

from tests.ext.conftest import sa_engine


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("async_mode", [False, True], ids=["sync", "async"])
async def test_engine_teardown_disposes_pool(tmp_path, async_mode):
    if async_mode:
        pytest.importorskip("sqlalchemy.ext.asyncio")

    driver = "sqlite+aiosqlite" if async_mode else "sqlite"
    resource = sa_engine.__wrapped__(f"{driver}:///{tmp_path / 'engine.sqlite'}", async_mode)
    disposed = []

    async with aclosing(resource):
        engine = await anext(resource)
        sync_engine = engine.sync_engine if async_mode else engine
        event.listen(sync_engine, "engine_disposed", disposed.append)

        if async_mode:
            async with engine.connect() as connection:
                assert (await connection.execute(text("SELECT 1"))).scalar() == 1
        else:
            with engine.connect() as connection:
                assert connection.execute(text("SELECT 1")).scalar() == 1

    assert disposed == [sync_engine]
