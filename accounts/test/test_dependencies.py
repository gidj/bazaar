import logging
from typing import Dict

import pytest
from mock import Mock

from accounts.depedencies import REDIS_URI_KEY, NotFoundException, Storage

logger = logging.getLogger(__name__)


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


@pytest.fixture
def account() -> Dict:
    return {
        'id': '',
        'email_address': 'jon.doe@nowhere.net',
        'first_name': 'Jon',
        'last_name': 'Doe',
        'billing_address_id': '',
        'shipping_address_id': '',
    }


@pytest.fixture
def create_account(account):
    def create(**updates):
        _account = account.copy()
        _account.update(updates)
        return _account

    return create


def test_get_fails_on_not_found(storage):
    with pytest.raises(NotFoundException) as exception:
        storage.get("1")
    assert "Account ID 1 does not exist" == exception.value.args[0]


def test_create_account(storage, account):
    account_id = storage.create(account)
    assert account_id is not None


def test_create_account_without_email_raises_error(storage, account):
    account = dict(account)
    del account['email_address']
    with pytest.raises(AssertionError) as error:
        storage.create(account)
    assert error.errisinstance(AssertionError)


def test_create_and_update_account(storage, account):
    account_id = storage.create(account)
    account.update({'first_name': 'John'})
    _account = storage.update(account_id, account)
    assert _account.get('first_name') == 'John'

