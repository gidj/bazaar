import json

from namkeo.rpc import RpcProxy
from nameko.web.handlers import http


class GatewayService:
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
        account = self.account.get(account)
        return json.dumps({'account': account})

    @http('POST', '/accounts')
    def post_account(self, request):
        data = json.loads(request.get_data(as_text=True))
        account = self.account.create(data['account'])
        return account
