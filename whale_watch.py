import json
import etherscan
import requests

# Get API Key
with open('ES_API_KEY_FILE.json', 'r') as f:
    es_key = json.loads(f.read())

api_key = es_key['ES_API_KEY']

es = etherscan.Client(
    api_key=api_key,
    cache_expire_after=5,
)

eth_price = es.get_eth_price()





# NFY contract hash for testing
ctr_hash = "0x1cbb83ebcd552d5ebf8131ef8c9cd9d9bab342bc"

# Will use a list of contract hashes, will be extremely small cap tokens
# list of perhaps 500 (?)
ctr_hash_list = []

bloxy_api = "ACCbkmobSFuMs"
r = requests.get("https://api.bloxy.info/dex/trades?protocol=Uniswap+v2&token={}"
                 "&key={}&format=structure".format(ctr_hash, bloxy_api))
tx_json_data = json.loads(r.text)
print("count of transcations: {}".format(len(tx_json_data)))
for dex_tx in tx_json_data:
    if dex_tx["buySymbol"] == "WETH" and dex_tx["amountBuy"] >= 15:
        whale_eth_bal = es.get_eth_balance(dex_tx["tx_sender"])
        print("{} ETH buy \non {} \nfor ticker {}\n "
              "whale wallet balance:  ${}\nTX HASH: {}\nTX sender: {}".format(dex_tx["amountBuy"],
                                                                              dex_tx["tx_time"],
                                                                              dex_tx["sellSymbol"],
                                                                              whale_eth_bal,
                                                                              dex_tx["tx_hash"],
                                                                              dex_tx["tx_sender"]))


