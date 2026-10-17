import pytest

from tests.base import async_sync_testsuite, async_testsuite, sync_testsuite


@pytest.fixture(scope="session")
def database_mode_resource(is_async_db):
    return "async" if is_async_db else "sync"


@async_testsuite
class TestFirstAsyncSuite:
    def test_resource_uses_async_mode(self, database_mode_resource):
        assert database_mode_resource == "async"


@sync_testsuite
class TestSecondSyncSuite:
    def test_resource_uses_sync_mode(self, database_mode_resource):
        assert database_mode_resource == "sync"


@async_sync_testsuite
class TestThirdCombinedSuite:
    def test_resource_matches_selected_mode(self, database_mode_resource, is_async_db):
        assert database_mode_resource == ("async" if is_async_db else "sync")
