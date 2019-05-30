import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http

import logging


class GatewayService:
    logger = logging.getLogger(__name__)
    name = 'gateway'

    addresses_rpc = RpcProxy('addresses')
    accounts_rpc = RpcProxy('accounts')
    listings_rpc = RpcProxy('listings')

    # Accounts stuff
    @http('GET', '/accounts/<string:account_id>')
    def get_account(self, request, account_id):
        account = self.accounts_rpc.get(account_id)
        if 'billing_address_id' in account:
            account['billing_address_id'] = self.addresses_rpc.get(account.get('billing_address_id'))
        return json.dumps({'account': account})

    @http('POST', '/accounts')
    def post_account(self, request):
        data = json.loads(request.get_data(as_text=True))
        self.logger.info(data)
        account_id = self.accounts_rpc.create(data)
        return json.dumps({'account': {'id': account_id}})

    # Addresses stuff
    @http('GET', '/addresses/<string:address_id>')
    def get_address(self, request, address_id):
        address = self.addresses_rpc.get(address_id)
        return json.dumps({'address': address})

    @http('POST', '/addresses')
    def post_address(self, request):
        data = json.loads(request.get_data(as_text=True))
        address_id = self.addresses_rpc.create(**data)
        return json.dumps({'address': {'id': address_id}})

    # Listing stuff
    @http('GET', '/listings/<string:listing_id>')
    def get_listing(self, request, listing_id):
        listing = self.listings_rpc.get(listing_id)
        self.logger.info(listing)
        return json.dumps({'listing': listing})

    @http('POST', '/listings')
    def post_listing(self, request):
        data = json.loads(request.get_data(as_text=True))
        listing_id = self.listings_rpc.create(**data)
        return json.dumps({'listing': {'id': listing_id}})
