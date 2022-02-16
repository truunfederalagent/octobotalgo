import datetime, json, requests, asyncio, aiohttp, indexer_utils as idutils
from aiohttp import ClientSession, ClientConnectorError
from twitter_bot import TwitterBot
from octorand import OctoPrime


with open('octos.json') as infile:
    octos = json.loads(infile.read())

twitter = TwitterBot()

def get_encoded_time(time):
    return time.isoformat().replace(':', '%3A').replace('+','%2B')

async def fetch_transactions(url, session, **kwargs):
    try:
        resp = await session.request(method="GET", url=url, **kwargs)
    except ClientConnectorError:
        return (url, 404)
    return await resp.json()

async def make_requests(octos, **kwargs):
    current_time = datetime.datetime.now(datetime.timezone.utc)
    after_time = current_time - datetime.timedelta(minutes=5)

    async with ClientSession() as session:
        tasks = []
        for octo_id in octos:
            tasks.append(
                fetch_transactions(url=f'https://algoindexer.algoexplorerapi.io/v2/assets/{octo_id}/transactions?after-time={get_encoded_time(after_time)}', session=session, **kwargs)
            )
        results = await asyncio.gather(*tasks)

    for resp in results:
        for trans in resp['transactions']:
            if 'inner-txns' in trans and 'group' in trans:
                    for curr_txn in trans['inner-txns']:
                        curr_txn_info = curr_txn["asset-transfer-transaction"]
                        time_info = datetime.datetime.fromtimestamp(curr_txn['round-time'], tz=datetime.timezone.utc)
                        if curr_txn_info['amount'] == 1 and time_info > after_time:
                            wallet = curr_txn_info['receiver']
                            time_info_string = time_info.strftime('%m/%d/%Y %I:%M %p')
                            num, name, app_id, octo_wallet = octos[str(curr_txn_info['asset-id'])]
                            amount_paid = idutils.get_amount_paid_in_round(wallet,trans['confirmed-round']) / 10**6
                            wallet_url = f'https://algoexplorer.io/address/{wallet}'
                            
                            prime = OctoPrime(num, app_id, octo_wallet)   
                            
                            message  = f'{name} purchased by {wallet[:4]}...{wallet[-4:]} for {amount_paid}Ⱥ\n'
                            message += f'{prime.letters}\n'
                            message += f'$OCTO: {prime.octo_remaining}\n'
                            message += f'{time_info_string} UTC\n'
                            message += f'Wallet :{wallet_url}\n'
                            message += f'Prime:{prime.url}'
                            
                            print(twitter.send_tweet(message))


asyncio.run(make_requests(octos))
