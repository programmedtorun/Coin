import etherscan
import json
import requests

# experimentation file for etherscan api
# needs https://pypi.org/project/etherscan/

# Get API Key
# with open('ES_API_KEY_FILE.json', 'r') as f:
#     es_key = json.loads(f.read())
#
# api_key = es_key['ES_API_KEY']
#
# es = etherscan.Client(
#     api_key=api_key,
#     cache_expire_after=5,
# )
#
# eth_price = es.get_eth_price()
#
# print(eth_price)
#
# # get someone's eth balance
# eth_balance = es.get_eth_balance('0x9c7f37a2e0496236374085b9d7aec2c0206b5500')
#
#
# transactions = es.get_transactions_by_address('0x7a250d5630b4cf539739df2c5dacb4c659f2488d')
#
# for trans in transactions:
#     tx_hash = trans['hash']
#     print(tx_hash)
#     res = requests.get(
#         "https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={}&apikey={}".format(tx_hash,
#                                                                                                                api_key))
#     print(json.loads(res.text))
#     print("\n***************************\n")
#
# token_transations = es.get_token_transactions(
#     contract_address='0x7a250d5630b4cf539739df2c5dacb4c659f2488d',
# )
# print(token_transations)

payload = {"query":'query ($network: EthereumNetwork!,$limit: Int!,$offset: Int!$from: ISO8601DateTime,$till: ISO8601DateTime){                    ethereum(network: $network){                      dexTrades(options:{desc: ["block.height","tradeIndex"], limit: $limit, offset: $offset},                        date: {since: $from till: $till }                        ) {                          block {                            timestamp {                              time (format: "%Y-%m-%d %H:%M:%S")                            }                           height                          }                          tradeIndex                          protocol                          exchange {                            fullName                          }                          smartContract {                            address {                              address                              annotation                            }                          }                          buyAmount                          buyCurrency {                            address                            symbol                          }                          sellAmount                          sellCurrency {                            address                            symbol                          }                          transaction {                            hash                          }                      }                    }                  }',"variables":'{"limit":100,"offset":10,"network":"ethereum","from":"2021-03-11","till":null,"dateFormat":"%Y-%m-%d"}'}





resp = requests.post("https://graphql.bitquery.io/", data=payload)
print(resp.content)

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
