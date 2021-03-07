import json
import etherscan
import requests
from datetime import datetime
from dateutil import tz

# Get API Key for etherscan
with open('ES_API_KEY_FILE.json', 'r') as f:
    es_key = json.loads(f.read())
api_key = es_key['ES_API_KEY']
es = etherscan.Client(
    api_key=api_key,
    cache_expire_after=5,
)

# get current eth price
cur_eth_pr = es.get_eth_price()

# NFY contract hash for testing
# contract hashes can be found on the token etherscan pg under contract:
ctr_hash = "0x1cbb83ebcd552d5ebf8131ef8c9cd9d9bab342bc"

# Will use a list of contract hashes, will be extremely small cap tokens
# list of perhaps 500 (?)
ctr_hash_list = []

# time zone stuff
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

# bloxy api - ** CAUTION VERY FEW CALLS IN TRIAL (less than 50)**
bloxy_api = "ACCbkmobSFuMs"

# note: in the request we will have to figure out the intervals to segment!
r = requests.get("https://api.bloxy.info/dex/trades?protocol=Uniswap+v2&token={}"
                 "&key={}&format=structure".format(ctr_hash, bloxy_api))
tx_json_data = json.loads(r.text)
print("count of transcations: {}".format(len(tx_json_data)))

#  what is considered a whale buy?! thinking greater than 15 ETH, but idk
for dex_tx in tx_json_data:
    if dex_tx["buySymbol"] == "WETH" and dex_tx["amountBuy"] >= 15:
        time = dex_tx["tx_time"][:19]  # transaction time
        utc = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        nyc_time = utc.astimezone(to_zone)
        whale_eth_bal = str(es.get_eth_balance(dex_tx["tx_sender"]))
        dec_prec = 18
        if len(whale_eth_bal) < dec_prec:  # under 0.1 eth
            whale_eth_bal = '0.' + ('0' * (dec_prec - len(whale_eth_bal))) + whale_eth_bal
        elif len(whale_eth_bal) == dec_prec:  # under 1 eth
            whale_eth_bal = '0.' + whale_eth_bal
        elif len(whale_eth_bal) > dec_prec:  # above 1 eth
            whale_eth_bal = whale_eth_bal[0:len(whale_eth_bal) - dec_prec] + '.' + whale_eth_bal[-dec_prec:]
        print("{} ETH buy \non {} \nfor ticker {}\n"
              "whale wallet balance:  {} ETH\nTX HASH: {}\nTX sender: {}".format(dex_tx["amountBuy"],
                                                                              nyc_time,
                                                                              dex_tx["sellSymbol"],
                                                                              whale_eth_bal,
                                                                              dex_tx["tx_hash"],
                                                                              dex_tx["tx_sender"]))
        print("\n************************************************\n")


