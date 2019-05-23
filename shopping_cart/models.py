import uuid
from typing import Dict


class ShoppingCart:
    def __init__(self, cart_id=None, listing_id=None, quantity=None, listings: Dict = None):
        self._id = cart_id or uuid.uuid4().hex
        self._listings = dict()

        if listing_id is not None:
            assert (quantity)
            self._listings[listing_id] = int(quantity)

        if listings is not None:
            self._listings.update(listings)

    def add_listing(self, listing_id, quantity) -> int:
        assert (quantity > 0)
        current_quantity = self._listings.get(listing_id, 0)
        self._listings[listing_id] = current_quantity + int(quantity)
        return self._listings.get(listing_id)

    def remove_listing(self, listing_id, quantity=None) -> int:
        new_quantity = 0
        if quantity is not None:
            assert (quantity > 0)
            current_quantity = self._listings.get(listing_id, 0)
            new_quantity = current_quantity - int(quantity)
            if new_quantity <= 0:
                self._listings.remove(listing_id)
        return new_quantity

    def to_dict(self):
        return {
            'id': self._id,
            'listings': self._listings,
        }

    @classmethod
    def from_listing(cls, listing_id: str, quantity: int) -> 'ShoppingCart':
        return cls(listing_id, quantity)

    @classmethod
    def from_dict(cls, data_dict: Dict) -> 'ShoppingCart':
        cart_id = data_dict.get('id')
        listings = data_dict.get('listings', {})
        return cls(cart_id=cart_id, listings=listings)
