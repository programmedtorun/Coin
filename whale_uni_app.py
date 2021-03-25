import etherscan
import json
import requests
from datetime import datetime, timedelta
import whale_watch.whale_watch as ww
import schedule
import threading
import time
import pathlib

cur_path = pathlib.Path(__file__).parent.absolute()

# twilio API
tw_file = "{}/API_FILES/TWILIO_STUFF.json".format(cur_path)
tw = ww.get_twilio(tw_file)
alert_phone_nums = ["+16462284704", "+15712769543"]

# Get API Key
ether_file = "{}/API_FILES/ES_API_KEY_FILE.json".format(cur_path)
with open(ether_file, 'r') as f:
    es_key = json.loads(f.read())

api_key = es_key['ES_API_KEY']
es = etherscan.Client(
    api_key=api_key,
    cache_expire_after=5,
)
uni_json = "{}/json_data/whale_uni_app.json".format(cur_path)
whale_addys = ww.open_conf(uni_json)

whale_eth = ww.get_whale_eth_bal(whale_addys["addy"], 18, es)
eth_usd = es.get_eth_price()['ethusd']

req = "https://api.etherscan.io/api?module=account&action=" \
      "txlistinternal&address={}&sort=asc&apikey={}".format(whale_addys["addy"], api_key)
res = requests.get(req)
tx_list = json.loads(res.text)['result']
tx_list_len = len(tx_list)
if whale_addys["tx_count"] < tx_list_len:
    tx_hash_list = []
    num_tx_to_check = tx_list_len - whale_addys["tx_count"]
    print("num_tx_check: {}".format(num_tx_to_check))
    for tx in tx_list[num_tx_to_check:]:
        if tx['from'] == "0x7a250d5630b4cf539739df2c5dacb4c659f2488d":
            tx_hash_list.append(tx['hash'])

    # addition = ""
    # for hash in tx_hash_list:
    #     addition += "hash: {}\n".format(hash)
    message = "Whale {} has made {} purchase(s) on Uniswap!!\nhis ETH bal: {}\ncheck recent tx here: {}"\
              .format(whale_addys["ytb_name"], num_tx_to_check, whale_eth, whale_addys["etherscan_link"])
    for num in alert_phone_nums:
        ww.send_sms(tw, message, num)
    whale_addys["tx_count"] = tx_list_len

ww.close_conf(uni_json, whale_addys)
