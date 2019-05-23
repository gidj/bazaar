import logging
import uuid

from nameko.rpc import rpc
from nameko_redis import Redis

from models import ShoppingCart


class ShoppingCartService:
    logger = logging.getLogger(__name__)
    name = 'shopping_carts'

    redis = Redis('development')

    def _schema(self, **kwargs):
        _data = {
            'id': kwargs.get('id', uuid.uuid4().hex),
            'account_id': kwargs.get('account_id', None),
            'listings': kwargs.get('listings', {}),
        }
        return dict((k, v) for k, v in _data.items() if v)

    @rpc
    def create(self, account_id, listings=None):
        cart = ShoppingCart.create(account_id)
        data = self._schema(**cart.to_dict())
        cart_id = data.get('id')
        self._write_data(cart_id, data)
        return cart_id

    @rpc
    def get(self, cart_id):
        cart = self.redis.hgetall(cart_id)
        self.logger.info(cart)
        return cart

    @rpc
    def add_listing(self, cart_id: str, listing_id: str, quantity: int) -> None:
        data = self.redis.hgetall(cart_id)
        cart = ShoppingCart.from_dict(data)
        cart.add_listing(listing_id, quantity)

        self.logger.info(cart)
        return cart

    def _write_data(self, _id, data):
        self.redis.hmset(_id, data)
        return _id
