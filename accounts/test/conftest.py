from typing import Dict

import pytest

from accounts.depedencies import REDIS_URI_KEY


@pytest.fixture
def redis_config():
    return {REDIS_URI_KEY: {"development": "redis://user@localhost:6379/11"}}


@pytest.fixture
def config(rabbit_config, redis_config):
    config = rabbit_config.copy()
    config.update(redis_config)
    return config


@pytest.fixture
def account() -> Dict:
    return {
        "id": "",
        "email_address": "jon.doe@nowhere.net",
        "first_name": "Jon",
        "last_name": "Doe",
        "billing_address_id": "",
        "shipping_address_id": "",
    }


@pytest.fixture
def create_account(account):
    def create(**updates):
        _account = account.copy()
        _account.update(updates)
        return _account

    return create


