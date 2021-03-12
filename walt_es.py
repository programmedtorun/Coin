#!/bin/python3

import json
import etherscan
import requests

API_KEY = '7AHYYFHS91RFIRZFYWJB83Z1XU8XPGCN37'

es = etherscan.Client(api_key = API_KEY)

Uniswap2_Contract = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'


transactions = es.get_transactions_by_address(Uniswap2_Contract)

print(json.dumps(transactions, indent=2))

es = requests.get("https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=%s&page=1&offset=100&sort=asc&apikey=%s" % (Uniswap2_Contract, API_KEY))