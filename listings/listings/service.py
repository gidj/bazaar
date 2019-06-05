import logging
import uuid
from typing import Dict

from nameko.rpc import rpc
from nameko_redis import Redis

from listings import dependencies


class ListingService:
    logger = logging.getLogger(__name__)
    name = "listings"

    storage = dependencies.Storage()

    @rpc
    def create(self, data: Dict):
        _id = self.storage.create(data)
        return _id

    @rpc
    def get(self, listing_id):
        return self.storage.get(listing_id)

    @rpc
    def update(self, listing_id, **kwargs):
        return self.storage.update(listing_id)
