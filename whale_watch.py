import json

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
        print("{} ETH buy on {} for ticker {}\nTX HASH: {}".format(dex_tx["amountBuy"],
                                                                   dex_tx["tx_time"],
                                                                   dex_tx["sellSymbol"],
                                                                   dex_tx["tx_hash"]))
