import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http

import logging


class GatewayService:
    logger = logging.getLogger(__class__.name)
    name = 'gateway'

    addresses_rpc = RpcProxy('addresses')
    accounts_rpc = RpcProxy('accounts')

    @http('GET', '/addresses/<string:address_id>')
    def get_address(self, request, address_id):
        address = self.addresses_rpc.get(address_id)
        return json.dumps({'address': address})

    @http('POST', '/addresses')
    def post_address(self, request):
        data = json.loads(request.get_data(as_text=True))
        address_id = self.addresses_rpc.create(data['address'])
        return address_id

    @http('GET', '/accounts/<string:account_id>')
    def get_account(self, request, account):
        account = self.accounts_rpc.get(account)
        return json.dumps({'account': account})

    @http('POST', '/accounts')
    def post_account(self, request):
        data = json.loads(request.get_data(as_text=True))
        self.logger.info(data)
        account_id = self.accounts_rpc.create(data['account'])
        return account_id
