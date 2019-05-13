import uuid

from nameko.rpc import rpc
from nameko_redis import Redis


class ListingService:
    name = 'listings'

    redis = Redis('development')

    def _schema(self, **kwargs):
        return {
            'seller_account_id': kwargs.get('seller_account_id', None),
            'product_name': kwargs.get('product_name', None),
            'quantity': kwargs.get('quantity', None),
        }

    @rpc
    def create(self, seller_account_id, product_name, quantity):
        data = self._schema(
            seller_account_id=seller_account_id,
            product_name=product_name,
            quantity=quantity,
        )

        listing_id = uuid.uuid4().hex
        self.redis.set(listing_id, data)

        return listing_id

    @rpc
    def get(self, listing_id):
        listing = self.redis.get(listing_id)
        return listing
