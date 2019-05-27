import logging
import uuid

from nameko.rpc import rpc
from nameko_redis import Redis


class AccountService:
    logger = logging.getLogger(__name__)
    name = 'accounts'

    redis = Redis('development')

    def _schema(self, **kwargs):
        _data = {
            'id': kwargs.get('id', uuid.uuid4().hex),
            'email_address': kwargs.get('email_address', None),
            'first_name': kwargs.get('first_name', None),
            'last_name': kwargs.get('last_name', None),
            'billing_address_id': kwargs.get('billing_address_id', None),
            'shipping_address_id': kwargs.get('shipping_address_id', None),
        }

        return dict((k, v) for k, v in _data.items() if v is not None)

    @rpc
    def create(self, **kwargs):
        assert (kwargs.get('email_address', None))
        data = self._schema(**kwargs)
        self.redis.hmset(data.get('id'), data)
        return data.get('id')

    @rpc
    def get(self, account_id):
        self.logger.info(account_id)
        account = self.redis.hgetall(account_id)
        return account
