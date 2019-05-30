import pytest

from listings.dependencies import REDIS_URI_KEY


@pytest.fixture
def redis_config():
    return {REDIS_URI_KEY: {'development': "redis://user@localhost:6379/11"}}


@pytest.fixture
def config(rabbit_config, redis_config):
    config = rabbit_config.copy()
    config.update(redis_config)
    return config
