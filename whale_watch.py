import json
import etherscan
import requests
from datetime import datetime, timedelta
from dateutil import tz
import re


# Get API Key for etherscan (needed to get whale's ETH bal)
with open('ES_API_KEY_FILE.json', 'r') as f:
    es_key = json.loads(f.read())
api_key = es_key['ES_API_KEY']
es = etherscan.Client(
    api_key=api_key,
    cache_expire_after=5,
)

# get current eth price (not needed at the moment)
cur_eth_pr = es.get_eth_price()

# NFY contract hash for testing
# contract hashes can be found on the token etherscan pg under contract:
c_hash = "0x1cbb83ebcd552d5ebf8131ef8c9cd9d9bab342bc"

# Will use a list of contract hashes, will be extremely small cap tokens
# list of perhaps 500 (?)
ctr_hash_list = []

# bloxy api - ** CAUTION VERY FEW CALLS IN TRIAL (less than 50)**
api = "ACCbkmobSFuMs"


# builds a request url to bloxy, returns a string
# time_interval is a nubmer in minutes
# ctr_hash is a contract token address
# bloxy_api is the api key
# in the future we can use this function to
# build a list of 500+ contract urls
def build_url(time_interval, ctr_hash, bloxy_api):
    xmg = datetime.utcnow() - timedelta(minutes=time_interval)  # x minutes ago = xmg
    string_xmg = xmg.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    url_en_xmg_utc_time = re.sub(":", "%3A", string_xmg)
    return "https://api.bloxy.info/dex/trades?protocol=Uniswap+v2&" \
           "token={}&from_date={}&" \
           "key={}&format=structure".\
           format(ctr_hash, url_en_xmg_utc_time, bloxy_api)


# takes a utc transaction time and converts to nyc time
def utc_xfr(tx_time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    time = tx_time[:19]  # transaction time
    utc = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)


# takes an individual's eth address and contract decimal precision
# decimal precision is usually 18
def get_whale_eth_bal(tx, dec_prec):
    whale_eth_bal = str(es.get_eth_balance(tx))
    if len(whale_eth_bal) < dec_prec:  # under 0.1 eth
        whale_eth_bal = '0.' + ('0' * (dec_prec - len(whale_eth_bal))) + whale_eth_bal
    elif len(whale_eth_bal) == dec_prec:  # under 1 eth
        whale_eth_bal = '0.' + whale_eth_bal
    elif len(whale_eth_bal) > dec_prec:  # above 1 eth
        whale_eth_bal = whale_eth_bal[0:len(whale_eth_bal) - dec_prec] + '.' + whale_eth_bal[-dec_prec:]
    return whale_eth_bal

# opens whale_conf.json and returns as python dict
def open_conf(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
    return data

# turns python dict into json and writes new file
# should be example of writing over whole file
def close_conf(file_name, data_update):
    file = open(file_name, 'r+')
    file.truncate(0)
    file.close()
    with open(file_name, 'w') as outfile:
        json.dump(data_update, outfile)

def process_token_addy(url, conf_file):
    r = requests.get(url)
    tx_json_data = json.loads(r.text)
    tx_ct = len(tx_json_data)
    print("\ncount of transcations: {}\n".format(tx_ct))
    data = open_conf(conf_file)
    if tx_ct == 0:
        print("no whale buys in last 20 minutes")
        token_list = data["token_list"]
        for token in token_list:
            token["wh_buys_20m"].clear()
        print("closing configuration file")
        close_conf(conf_file, data)
        return data
    else:
        # TODO process whales into whale_conf.json...
        #  what is considered a whale buy?! thinking greater than 15 ETH...
        for dex_tx in tx_json_data:
            if dex_tx["buySymbol"] == "WETH" and dex_tx["amountBuy"] >= 15:
                nyc_time = utc_xfr(dex_tx["tx_time"])
                whale_eth_bal = get_whale_eth_bal(dex_tx["tx_sender"], 18)
                print("{} ETH buy \non {} \nfor ticker {}\n"
                      "whale wallet balance:  {} ETH\nTX HASH: {}\nTX sender: {}".
                      format(dex_tx["amountBuy"],
                             nyc_time,
                             dex_tx["sellSymbol"],
                             whale_eth_bal,
                             dex_tx["tx_hash"],
                             dex_tx["tx_sender"]))
                print("\n************************************************\n")


if __name__ == "__main__":
    print("hello")
