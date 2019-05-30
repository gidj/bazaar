import decimal
import logging
import uuid
from typing import AnyStr, Dict

from nameko.extensions import DependencyProvider
from redis import StrictRedis as _StrictRedis

from .exceptions import NotFoundException


REDIS_URI_KEY = "REDIS_URIS"


class RedisWrapper:
    logger = logging.getLogger(__name__)

    def __init__(self, redis_client):
        self.redis = redis_client

    def _generate_id(self) -> AnyStr:
        return uuid.uuid4().hex

    def _format_key(self, listing_id) -> AnyStr:
        return "listings:{}".format(listing_id)

    def _schema(self, data_dict: Dict) -> Dict:
        return {
            "id": data_dict.get("id"),
            "seller_account_id": data_dict.get("seller_account_id"),
            "product_name": data_dict.get("product_name"),
            "quantity": data_dict.get("quantity", 0),
            "price": data_dict.get("price", decimal.Decimal(0)),
        }

    def _write(self, _id: str, data_dict: Dict):
        d = self.redis.hmset(self._format_key(_id), self._schema(data_dict))
        self.logger.info(d)

    def create(self, data: Dict) -> AnyStr:
        _id = self._generate_id()
        data["id"] = _id
        self._write(_id, data)
        return _id

    def get(self, listing_id: AnyStr) -> Dict:
        listing = self.redis.hgetall(self._format_key(listing_id))
        if not listing:
            raise NotFoundException("Listing ID {} does not exist".format(listing_id))
        else:
            return self._schema(listing)

    def update(self, listing_id: AnyStr, updates: Dict) -> Dict:
        listing = self.get(listing_id)
        listing.update(updates)
        self._write(listing_id, listing)
        return listing


class Storage(DependencyProvider):
    def __init__(self, key='development', **options):
        self.key = key
        self.client = None
        self.options = {
            'decode_responses': True,
        }
        self.options.update(options)

    def setup(self):
        redis_uris = self.container.config[REDIS_URI_KEY]
        self.redis_uri = redis_uris[self.key]

    def start(self):
        self.client = _StrictRedis.from_url(self.redis_uri, **self.options)

    def stop(self):
        self.client = None

    def kill(self):
        self.client = None

    def get_dependency(self, worker_ctx):
        wrapper = RedisWrapper(self.client)
        return wrapper
