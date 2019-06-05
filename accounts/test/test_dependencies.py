import logging

import pytest
from mock import Mock

from accounts.depedencies import NotFoundException, Storage

logger = logging.getLogger(__name__)


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


def test_create_account(storage, account):
    account_id = storage.create(account)
    assert account_id is not None


def test_create_account_without_email_raises_error(storage, account):
    account = dict(account)
    del account["email_address"]
    with pytest.raises(AssertionError) as error:
        storage.create(account)
    assert error.errisinstance(AssertionError)


def test_create_and_update_account(storage, account):
    account_id = storage.create(account)
    account.update({"first_name": "John"})
    _account = storage.update(account_id, account)
    assert _account.get("first_name") == "John"
