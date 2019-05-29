import pytest
from mock import Mock

from accounts.depedencies import REDIS_URI_KEY, Storage, NotFoundException


@pytest.fixture
def redis_config():
    return {REDIS_URI_KEY: {'development': "redis://user@localhost:6379/11"}}


@pytest.fixture
def config(rabbit_config, redis_config):
    config = rabbit_config.copy()
    config.update(redis_config)
    return config


@pytest.fixture
def storage(config):
    provider = Storage()
    provider.container = Mock(config=config)
    provider.setup()
    provider.start()
    return provider.get_dependency({})


def test_get_fails_on_not_found(storage):
    with pytest.raises(NotFoundException) as exception:
        storage.get("1")
    assert "Account ID 1 does not exist" == exception.value.args[0]
