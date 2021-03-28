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

alert_phone_nums = ["+15712769543", "+16462284704"]


# twilio API
def get_twil():
    tw_file = "{}/API_FILES/TWILIO_STUFF.json".format(cur_path)
    return ww.get_twilio(tw_file)


# Get API Key
def get_api_key(rel_path):
    ether_file = "{}/{}".format(cur_path, rel_path)
    with open(ether_file, 'r') as f:
        es_key = json.loads(f.read())

    return es_key['ES_API_KEY']


def get_es(api_key):
    return etherscan.Client(
        api_key=api_key,
        cache_expire_after=5)


def op(rel_path):
    uni_json = "{}/{}".format(cur_path, rel_path)
    return ww.open_conf(uni_json)


def check_wallets(wah, api_key, tw, alert_phone_nums):
    es = get_es(api_key)
    for whale in wah:
        whale_eth = ww.get_whale_eth_bal(wah[whale]["addy"], 18, es)
        req = "https://api.etherscan.io/api?module=account&action=txlist&address={}&apikey={}" \
            .format(wah[whale]["addy"], api_key)
        res = requests.get(req)
        tx_list = json.loads(res.text)['result']
        tx_list_len = len(tx_list)
        print("tx_whale_ct: {}, tx_list_len: {}\n---------------".format(wah[whale]["tx_count"], tx_list_len))
        if wah[whale]["tx_count"] < tx_list_len:  # do only if new transactions are present
            tx_hash_list = []
            uni_tx_ct = 0
            num_tx_to_check = tx_list_len - wah[whale]["tx_count"]
            for tx in tx_list[-num_tx_to_check:]:  # check only most recent transactions
                if tx['to'] == "0x7a250d5630b4cf539739df2c5dacb4c659f2488d":  # if uniswap transaction
                    uni_tx_ct += 1
                    tx_hash_list.append("https://etherscan.io/tx/{}".format(tx['hash']))
            addition = ""
            for tx_link in tx_hash_list:  # add all tx hashes
                addition += "\n{}\n-".format(tx_link)
            message = "Whale {} has made {} purchase(s) on Uniswap!!\n" \
                      "his ETH bal: {}\netherscan wallet link: {}\ntx details:{}" \
                      .format(wah[whale]["ytb_name"], uni_tx_ct, whale_eth[:6], wah[whale]["etherscan_link"], addition)
            print("message:\n{}\n***************************************************".format(message))
            for num in alert_phone_nums:
                ww.send_sms(tw, message, num)
            wah[whale]["tx_count"] = tx_list_len  # update whale's tx count after processing
        whale_uni_file = '{}/json_data/whale_uni_app.json'.format(cur_path)
        ww.close_conf(whale_uni_file, wah)


tw = get_twil()
api_key = get_api_key('API_FILES/ES_API_KEY_FILE.json')
whale_addys_hash = op('json_data/whale_uni_app.json')  # use relative path


# scheduling section
def job():
    check_wallets(whale_addys_hash, api_key, tw, alert_phone_nums)


schedule.every(5).minutes.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
