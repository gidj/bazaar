class ShoppingCart:
    def __init__(self, account_id, listings=None):
        assert(account_id)
        self._account_id = account_id

        if listings is None:
            self._listings = set()
        else:
            self._listings = set(listings)

    def add_listing(self, listing_id):
        self._listings.add(listing_id)

    def remove_listing(self, listing_id):
        self._listings.remove(listing_id)

    def to_dict(self):
        return {
            'account_id' : self._account_id,
            'listings' : list(self._listings),
        }

    @classmethod
    def from_dict(cls, data_dict: dict):
        account_id = data_dict.get('account_id')
        listings = data_dict.get('listings', [])
        return cls(account_id, listings=listings)

