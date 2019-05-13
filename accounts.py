from nameko.rpc import rpc


class AccountService:
    name = 'account_service'

    @rpc
    def get_account(self, account_id):
        return { 'account_id': account_id }
