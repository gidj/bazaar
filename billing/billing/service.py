import logging
from typing import Dict

from nameko.rpc import rpc

from billing import depedencies


class BillingService:
    logger = logging.getLogger(__name__)
    name = 'billing'

    storage = depedencies.Storage()

    @rpc
    def create(self, data: Dict):
        assert (data.get('email_address', None))
        _id = self.storage.create(data)
        return _id

    @rpc
    def get(self, billing_id):
        return self.storage.get(billing_id)

    @rpc
    def update(self, billing_id, data: Dict):
        return self.storage.update(billing_id)
