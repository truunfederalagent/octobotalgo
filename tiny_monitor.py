import os
from tinyman.v1.client import TinymanClient
from algosdk.v2client import algod

class TinyMonitor(object):

    def __init__(self, asset_id):
        self.USER_ADDRESS = os.environ.get('ALGO_ADDRESS')
        self.USER_SECRET = os.environ.get('ALGO_SECRET')
        self.API_KEY = os.environ.get('ALGO_API')
        self. VALIDATOR_ID = 552635992
        self.asset_id = asset_id

        self.algod_address = os.environ.get('ALGOD_ADDRESS')
        self.algod_client = algod.AlgodClient(self.API_KEY, self.algod_address)

        self.client = TinymanClient(self.algod_client, self.VALIDATOR_ID , user_address=self.USER_ADDRESS)
        self.ASSET = self.client.fetch_asset(self.asset_id)
        self.ALGO = self.client.fetch_asset(0)

    def get_asset_quote_price(self, amount = 1, per_algo = False):
        pool = self.client.fetch_pool(self.ASSET, self.ALGO)
        if per_algo:
            quote = pool.fetch_fixed_input_swap_quote(self.ALGO(amount * 10**6), slippage=0.01)
        else:
            quote = pool.fetch_fixed_input_swap_quote(self.ASSET(amount * 10**self.ASSET.decimals), slippage=0.01)

        return quote.amount_out.amount / 10**6

    