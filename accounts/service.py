import uuid

from nameko.rpc import rpc
from nameko_redis import Redis


class AccountService:
    name = 'accounts'

    redis = Redis('development')

    def _schema(self, **kwargs):
        return {
            'id': uuid.uuid4().hex,
            'email_address': kwargs.get('email_address', None),
            'first_name': kwargs.get('first_name', None),
            'last_name': kwargs.get('last_name', None),
            'billing_address_id': kwargs.get('billing_address_id', None),
            'shipping_address_id': kwargs.get('shipping_address_id', None),
        }

    @rpc
    def create(self, email_address):
        assert (email_address)
        data = self._schema(email_address=email_address)
        self.redis.set(data.get('id'), data)
        return data.get('id')

    @rpc
    def get(self, account_id):
        account = self.redis.get(account_id)
        return account
