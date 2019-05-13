from nameko.rpc import rpc


class AddressService:
    name = 'address_service'

    @rpc
    def create(self, street_1, street_2, city, province, postal_code, country):
        return

    @rpc
    def get(self, address_id):
        return { 'address_id': address_id }
