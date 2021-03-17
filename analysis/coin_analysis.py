import requests
import json


class Analysis(object):

    # coin_list should not be too long!!
    def __init__(self, coin_list, base_path):
        self.coin_list = coin_list
        self.base_path = base_path
        self.cmc_json = "{}/json_data/cmc_master_list.json".format(base_path)
        self.cc_json = "{}/json_data/cc_master_list.json".format(base_path)
        print(self.base_path)

    # returns coin list as a string for easy printing.
    def return_coin_list(self):
        str_list = "[" + self.coin_list[0]
        for coin in self.coin_list[1:]:
            str_list += ", " + coin
        str_list = str_list + "]"
        return str_list

    # returns crypto compare API Key
    def cc_api_key(self):
        cc_file = "{}/API_FILES/CC_API_KEY_FILE.json".format(self.base_path)
        with open(cc_file, 'r') as f:
            cc_api_keys = json.loads(f.read())
        return cc_api_keys['CC_API_KEY']

    def cmc_api_key(self):
        cmc_file = "{}/API_FILES/CMC_API_KEY_FILE.json".format(self.base_path)
        with open(cmc_file, 'r') as f:
            cmc_api_keys = json.loads(f.read())
        return cmc_api_keys['CMC_API_KEY']

    # ret hash of all coins on cmc
    def cmc_full_hash(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=5000"
        api_key = self.cmc_api_key()
        res = requests.get(url, headers={"X-CMC_PRO_API_KEY": api_key})
        text_res = res.text
        return json.loads(text_res)

    # should be recreated to have most up-to-date information (for testing use load_cmc_hash())
    def create_cmc_hash_file(self):
        file = open(self.cmc_json, 'r+')
        file.truncate(0)
        file.close()
        cmc_hash = self.cmc_full_hash()
        with open(self.cmc_json, 'w') as outfile:
            json.dump(cmc_hash, outfile)

    # loads coin has from file to in mem python dict
    def load_cmc_hash(self):
        with open(self.cmc_json, 'r') as json_file:
            data = json.load(json_file)
        return data

    # creates a .json file locally of cc_full_hash. use only periodically
    def create_cc_hash_file(self):
        file = open(self.cc_json, 'r+')
        file.truncate(0)
        file.close()
        hash = self.cc_full_hash()
        with open(self.cc_json, 'w') as outfile:
            json.dump(hash, outfile)

    # loads coin has from file to in mem python dict
    def load_cc_hash(self):
        with open(self.cc_json, 'r') as json_file:
            data = json.load(json_file)
        return data

    # returns a list of dicts symbol = symbol, cc_id = cc_id
    def get_coin_id_list(self):
        cc_hash = self.load_cc_hash()
        id_list = []
        for coin in self.coin_list:
            id_list.append({"symbol": coin, "cc_id": cc_hash[coin]['Id']})
        return id_list

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

    # returns a list of dicts, {"symbol": symbol, "cc_id": cc_id, "social": {social data dict}}
    def get_social(self, coin_id_list):
        api_key = self.cc_api_key()
        for coin in coin_id_list:
            res = requests.get("https://min-api.cryptocompare.com/data/social/coin/latest?api_key={}&coinId={}".format(api_key, coin["cc_id"]))
            text_res = res.text
            j_res = json.loads(text_res)
            coin["social_data"] = j_res
        return coin_id_list

    # between low and high mk cap and at least vol_thresh
    def get_financials(self, low, high, vol_thresh):
        self.create_cmc_hash_file()

        data = self.load_cmc_hash()['data']

        low_caps = {}
        # Get low market cap coins:
        for coin in data:
            mk_cap = coin['quote']['USD']['market_cap']
            vol = coin['quote']['USD']['volume_24h']
            # print(coin['quote']['USD']['market_cap'])
            if mk_cap < high and mk_cap != 0 and mk_cap > low and vol > vol_thresh:
                low_caps[coin['symbol']] = {'max_supply': coin['max_supply'],
                                            'circulating_supply': coin['circulating_supply'],
                                            'vol_24hr': vol,
                                            'market_cap': coin['quote']['USD']['market_cap']
                                            }
        ct = 0
        for coin in low_caps:
            ct += 1
            print("{} mk cp --> {}".format(coin, low_caps[coin]['market_cap']))
        print("count is:   {}".format(ct))
        print("loading and returning financials in memory ")
        return low_caps

    def write_low_caps_to_json(self, file_name, low_caps):
        file = open(file_name, 'r+')
        file.truncate(0)
        file.close()
        with open(file_name, 'w') as outfile:
            json.dump(low_caps, outfile, default=str)

    # returns list of dicts i.e. [{cc_id: , cc_symbol: , social_points: , market_cap: ,
    #                             volume_24h: , percent_change_1h: ,
    #                             percent_change_24h: , percent_change_7d: }]
    def create_purchase_ndx(self, social_list):
        final_data = []
        financial_info = self.load_cmc_hash()['data']
        symbols_in_social_list = []
        for coin in social_list:
            symbols_in_social_list.append(coin["symbol"])

        for coin in social_list:
            for coin_f in financial_info:
                if coin['symbol'] == coin_f['symbol']:
                    final_data.append({"cc_id": coin['cc_id'],
                                       "cc_symbol": coin['symbol'],
                                       "social_points": coin['social_data']['Data']['General']['Points'],
                                       "market_cap": coin_f['quote']['USD']['market_cap'],
                                       "volume_24h": coin_f['quote']['USD']['volume_24h'],
                                       "percent_change_1h": coin_f['quote']['USD']['percent_change_1h'],
                                       "percent_change_24h": coin_f['quote']['USD']['percent_change_24h'],
                                       "percent_change_7d": coin_f['quote']['USD']['percent_change_7d'],
                                       "percent_change_30d": coin_f['quote']['USD']['percent_change_30d'],
                                       "buy_level": 0
                                       })
        return final_data

    # Gives buy recommendation, ranking first coin = best buy, last coin = worst buy
    def process_vectors(self, ndx_list):
        for coin in ndx_list:
            social_normalizer = (coin["social_points"] * coin["volume_24h"]) / coin["market_cap"]
            if 15 > coin['percent_change_24h'] > -5:
                coin['buy_level'] = coin['buy_level'] + 5
            if 10 > coin['percent_change_1h'] > -3:
                coin['buy_level'] = coin['buy_level'] + 5
            if coin["percent_change_7d"] > 0:
                coin['buy_level'] = coin['buy_level'] + 2
            if coin["percent_change_30d"] < 120:
                coin['buy_level'] = coin['buy_level'] + 5

            if 399999999 < coin["market_cap"] <= 500000000:
                coin['buy_level'] = coin['buy_level'] + 1
            elif 299999999 < coin["market_cap"] <= 400000000:
                coin['buy_level'] = coin['buy_level'] + 2
            elif 199999999 < coin["market_cap"] <= 300000000:
                coin['buy_level'] = coin['buy_level'] + 3
            elif 99999999 < coin["market_cap"] <= 200000000:
                coin['buy_level'] = coin['buy_level'] + 4
            elif 49999999 < coin["market_cap"] <= 100000000:
                coin['buy_level'] = coin['buy_level'] + 6
            elif coin["market_cap"] <= 50000000:
                coin['buy_level'] = coin['buy_level'] + 9

            if social_normalizer >= 100000:
                coin['buy_level'] = coin['buy_level'] + 5
            elif 99999 >= social_normalizer >= 50000:
                coin['buy_level'] = coin['buy_level'] + 4
            elif 49999 >= social_normalizer >= 20000:
                coin['buy_level'] = coin['buy_level'] + 3
            elif 19999 >= social_normalizer >= 10000:
                coin['buy_level'] = coin['buy_level'] + 2
            elif 9999 >= social_normalizer >= 1000:
                coin['buy_level'] = coin['buy_level'] + 1
        return sorted(ndx_list, key=lambda i: i['buy_level'])
