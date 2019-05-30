import logging
import uuid
from typing import AnyStr, Dict

from nameko.extensions import DependencyProvider
from redis import StrictRedis as _StrictRedis

from accounts.exceptions import NotFoundException

REDIS_URI_KEY = "REDIS_URIS"


class RedisWrapper:
    logger = logging.getLogger(__name__)

    def __init__(self, redis_client):
        self.redis = redis_client

    def _generate_id(self) -> AnyStr:
        return uuid.uuid4().hex

    def _format_key(self, account_id) -> AnyStr:
        return "accounts:{}".format(account_id)

    def _schema(self, data_dict: Dict) -> Dict:
        return {
            "id": data_dict.get("id"),
            "email_address": data_dict.get("email_address"),
            "first_name": data_dict.get("first_name", None),
            "last_name": data_dict.get("last_name", None),
            "billing_address_id": data_dict.get("billing_address_id", None),
            "shipping_address_id": data_dict.get("shipping_address_id", None),
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

    def get(self, account_id: AnyStr) -> Dict:
        account = self.redis.hgetall(self._format_key(account_id))
        if not account:
            raise NotFoundException("Account ID {} does not exist".format(account_id))
        else:
            return self._schema(account)

    def update(self, account_id: AnyStr, updates: Dict) -> Dict:
        account = self.get(account_id)
        account.update(updates)
        self._write(account_id, account)
        return account


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
