import logging
from typing import Dict

from nameko.rpc import rpc

from accounts import depedencies


class AccountService:
    logger = logging.getLogger(__name__)
    name = 'accounts'

    storage = depedencies.Storage()

    @rpc
    def create(self, data: Dict):
        assert (data.get('email_address', None))
        _id = self.storage.create(data)
        return _id

    @rpc
    def get(self, account_id):
        return self.storage.get(account_id)

    @rpc
    def update(self, account_id, data: Dict):
        return self.storage.update(account_id)
