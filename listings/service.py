import uuid

from nameko.rpc import rpc
from nameko_redis import Redis


class ListingService:
    name = 'listings'

    redis = Redis('development')

    def _schema(self, **kwargs):
        _data = {
            'id': kwargs.get('id', uuid.uuid4().hex),
            'seller_account_id': kwargs.get('seller_account_id', None),
            'product_name': kwargs.get('product_name', None),
            'quantity': kwargs.get('quantity', None),
            'price': kwargs.get('price', None),
        }

        return dict((k, v) for k, v in _data.items() if v is not None)

    @rpc
    def create(self, **kwargs):
        data = self._schema(**kwargs)
        listing_id = data.get('id')
        self.redis.hmset(listing_id, data)
        return listing_id

    @rpc
    def get(self, listing_id):
        listing = self.redis.hgetall(listing_id)
        return listing
