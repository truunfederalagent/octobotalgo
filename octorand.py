import requests, base64, indexer_utils as idutil
from algosdk import logic
import assets


class OctoPrime(object):
    
    def __init__(self, num, app_id, wallet):       
        state = idutil.get_application_by_id(app_id)['application']['params']['global-state']
        for param in state:
            key = base64.b64decode(param['key']).decode('utf-8')
            if key == 'Params':
                self.letters = base64.b64decode(param['value']['bytes']).decode('utf-8')
   
        self.octo_remaining = idutil.get_amount_asset_in_wallet(wallet, assets.OCTORAND) / 10**6
        self.url = f'https://octorand.com/prime/gen1/{num}'