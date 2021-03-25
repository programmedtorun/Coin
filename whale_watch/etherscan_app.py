import etherscan
import json
import requests
from datetime import datetime, timedelta
import re


# Get API Key
with open('/Users/patrickskelley/Desktop/Programming/Projects/Coin2/Coin/API_FILES/ES_API_KEY_FILE.json', 'r') as f:
    es_key = json.loads(f.read())

api_key = es_key['ES_API_KEY']
es = etherscan.Client(
    api_key=api_key,
    cache_expire_after=5,
)

whale_addys = {"addy" : "0xFf6992fDa98A9452E2EB0487e17533f428BE6bDC", "ytb_name" : "suppo", "tx_count" : 0}

whale_eth = es.get_eth_balance(whale_addys["addy"])
eth_usd = es.get_eth_price()['ethusd']

req = "https://api.etherscan.io/api?module=account&action=" \
    "txlistinternal&address={}&sort=asc&apikey={}".format(whale_addys["addy"], api_key)
res = requests.get(req)
tx_list = json.loads(res.text)['result']
tx_list_len = len(tx_list)
if whale_addys["tx_count"] < tx_list_len:
    tx_hash_list = []
    num_tx_to_check = tx_list_len - whale_addys["tx_count"]
    for tx in tx_list[num_tx_to_check:]:
        if tx['from'] == "0x7a250d5630b4cf539739df2c5dacb4c659f2488d":
            tx_hash_list.append(tx['hash'])


print("\n\n************************************\n\n")




# for trans in transactions:
#     tx_hash = trans['hash']
#     print(tx_hash)
#     res = requests.get(
#         "https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={}&apikey={}".format(tx_hash,
#                                                                                                                api_key))
# # get list of internal transactions by address.
#     print(json.loads(res.text))
#     print("\n***************************\n")
#
# token_transations = es.get_token_transactions(
#     contract_address='0x7a250d5630b4cf539739df2c5dacb4c659f2488d',
# )
# print(token_transations)

# res = requests.get("https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={}&page=1&offset=100&sort=asc&apikey={}".format("0x1cbb83ebcd552d5ebf8131ef8c9cd9d9bab342bc", api_key))
# json_data = json.loads(res.text)
# result = json_data["result"]
# json_formatted_str = json.dumps(result, indent=2)
#
# # print(json_formatted_str)
#
# tx_hash = "0x4389ab0df3e50b1eb0aa8b2f21ee01ab133dc1f72a012aa2f30b6c872b634bc9"
# get_tx_by_hash = requests.get("https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={}&apikey={}".format(tx_hash, api_key))
#
# tx_json_data = json.loads(get_tx_by_hash.text)
# print(tx_json_data)
