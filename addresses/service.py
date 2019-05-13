from nameko.rpc import rpc
from nameko_redis import Redis

import uuid

class AddressService:
    name = 'addresses'

    redis = Redis('development')

    def _schema(self, **kwargs):
        return {
            'street_1': kwargs.get('street_1', None),
            'street_2': kwargs.get('street_2', None),
            'city': kwargs.get('city', None),
            'province': kwargs.get('province', None),
            'postal_code': kwargs.get('postal_code', None),
            'country': kwargs.get('country', None),
        }

    @rpc
    def create(self, street_1, street_2, city, province, postal_code, country):
        address_id = uuid.uuid4().hex

        data = self._schema(
            street_1=street_1,
            street_2=street_2,
            city=city,
            province=province,
            postal_code=postal_code,
            country=country,
        )

        self.redis.set(address_id, data)
        return address_id

    @rpc
    def get(self, address_id):
        address = self.redis.get(address_id)
        return address
