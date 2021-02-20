from collect import Collect
import urllib
import requests
from pycoingecko import CoinGeckoAPI
import csv
import json


class Analysis(object):

    # coin_list should not be too long!!
    def __init__(self, coin_list):
        self.coin_list = coin_list

    # returns coin list as a string for easy printing.
    def return_coin_list(self):
        str_list = "[" + self.coin_list[0]
        for coin in self.coin_list[1:]:
            str_list += ", " + coin
        str_list = str_list + "]"
        return str_list

    # returns crypto compare API Key
    def cc_api_key(self):
        with open('CC_API_KEY_FILE.json', 'r') as f:
            cc_api_keys = json.loads(f.read())
        return cc_api_keys['CC_API_KEY']

    # creates a .json file locally of cc_full_hash, use periodically
    def create_hash_file(self):
        file = open("cc_master_list.json", "r+")
        file.truncate(0)
        file.close()
        hash = self.cc_full_hash()
        with open('cc_master_list.json', 'w') as outfile:
            json.dump(hash, outfile)

    # loads coin has from file to in mem python dict
    def load_hash(self):
        with open('cc_master_list.json') as json_file:
            return json.load(json_file)

    # ret hash of all coins on cc marked 'trading.' keys are coin tickers
    def cc_full_hash(self):
        key = self.cc_api_key()
        res = requests.get("https://min-api.cryptocompare.com/data/all/coinlist?api_key={}".format(key))
        text_res = res.text
        j_res = json.loads(text_res)
        hash = j_res["Data"]
        keys_to_del = []
        for key in hash:
            if not hash[key]["IsTrading"]:
                keys_to_del.append(key)
        for key in keys_to_del:
            del hash[key]
        return hash

    def get_social(self, coin_id):
        key = cc_api()
        res = requests.get("https://min-api.cryptocompare.com/data/social/coin/latest?api_key={}&coinId={}".format(key, coin_id))
        text_res = res.text
        j_res = json.loads(text_res)
        print(j_res)

    # would like to get alt rank of luna
    # def luna(self):
    #     res = requests.get("https://lunarcrush.com/markets?rpp=50&ob=alt_rank")
    #     print(res)

