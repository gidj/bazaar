import uuid

from nameko.rpc import rpc
from nameko_redis import Redis

from models import ShoppingCart

class ShoppingCartService:
    name = 'shopping_carts'

    redis = Redis('development')

    @rpc
    def create(self, account_id, listings=None):
        cart_id = uuid.uuid4().hex

        cart = ShoppingCart(account_id, listings=listings)
        self.redis.set(cart_id, cart.to_dict())

        return cart_id

    @rpc
    def get(self, account_id):
        account = self.redis.get(account_id)
        return account

