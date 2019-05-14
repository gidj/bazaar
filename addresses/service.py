from nameko.rpc import rpc
from nameko_redis import Redis

import uuid
import logging


class AddressService:
    logger = logging.getLogger(__name__)
    name = 'addresses'

    redis = Redis('development')

    def _schema(self, **kwargs):
        _data = {
            'id': kwargs.get('id', uuid.uuid4().hex),
            'street_1': kwargs.get('street_1', None),
            'street_2': kwargs.get('street_2', None),
            'city': kwargs.get('city', None),
            'province': kwargs.get('province', None),
            'postal_code': kwargs.get('postal_code', None),
            'country': kwargs.get('country', None),
        }

        return dict((k, v) for k, v in _data.items() if v is not None)

    @rpc
    def create(self, **kwargs):
        data = self._schema(**kwargs)
        self.redis.hmset(data.get('id'), data)
        return data.get('id')

    @rpc
    def get(self, address_id):
        self.logger.info(address_id)
        address = self.redis.hgetall(address_id)
        return address
