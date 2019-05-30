import pytest
from mock import Mock

from listings.dependencies import Storage
from listings.exceptions import NotFoundException


@pytest.fixture
def storage(config):
    provider = Storage()
    provider.container = Mock(config=config)
    provider.setup()
    provider.start()
    return provider.get_dependency({})


def test_get_failes_on_not_found(storage):
    pass
