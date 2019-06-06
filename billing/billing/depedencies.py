import logging
import uuid
from typing import AnyStr, Dict

from nameko.extensions import DependencyProvider
from redis import StrictRedis as _StrictRedis

from billing.exceptions import NotFoundException

REDIS_URI_KEY = "REDIS_URIS"


class RedisWrapper:
    logger = logging.getLogger(__name__)

    def __init__(self, redis_client):
        self.redis = redis_client

    def _generate_id(self) -> AnyStr:
        return uuid.uuid4().hex

    def _format_key(self, billing_id) -> AnyStr:
        return "billing:{}".format(billing_id)

    def _schema(self, data_dict: Dict) -> Dict:
        return {
            "id": data_dict.get("id"),
            "method": data_dict.get("method"),
            "account_number": data_dict.get("account_number"),
            "billing_address_id": data_dict.get("billing_address_id", None),
        }

    def _write(self, _id: str, data_dict: Dict):
        d = self.redis.hmset(self._format_key(_id), self._schema(data_dict))
        self.logger.info(d)

    def create(self, data: Dict) -> AnyStr:
        assert data.get("email_address", None)
        _id = self._generate_id()
        data["id"] = _id
        self._write(_id, data)
        return _id

    def get(self, billing_id: AnyStr) -> Dict:
        billing = self.redis.hgetall(self._format_key(billing_id))
        if not billing:
            raise NotFoundException("Payment Method ID {} does not exist".format(billing_id))
        else:
            return self._schema(billing)

    def update(self, billing_id: AnyStr, updates: Dict) -> Dict:
        billing = self.get(billing_id)
        billing.update(updates)
        self._write(billing_id, billing)
        return billing


class Storage(DependencyProvider):
    def __init__(self, key="development", **options):
        self.key = key
        self.client = None
        self.options = {"decode_responses": True}
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
