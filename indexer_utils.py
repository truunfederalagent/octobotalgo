import requests

BASE_URL = 'https://algoindexer.algoexplorerapi.io/v2/'

def get_asset_transactions_by_id(asset_id, after_time = None):
    url = BASE_URL + f'assets/{asset_id}/transactions'
    if after_time != None:
        encoded_time = after_time.isoformat().replace(':', '%3A').replace('+','%2B')
        url += f'?after-time={encoded_time}'

    return requests.get(url).json()


def get_amount_asset_in_wallet(wallet, asset_id):
    url = BASE_URL + f'accounts/{wallet}'
    data = requests.get(url).json()
    for asset in data['account']['assets']:
        if asset['asset-id'] == int(asset_id):
            return asset['amount']
    return 0


def get_application_by_id(app_id):
    url = BASE_URL + f'applications/{app_id}'
    return requests.get(url).json()


def get_amount_paid_in_round(wallet, round):
    url = BASE_URL + f'accounts/{wallet}/transactions?round={round}'
    txs = requests.get(url).json()
    total = 0
    for tx in txs['transactions']:
        if tx['tx-type'] == 'pay':
            total += tx['payment-transaction']['amount']
    return total