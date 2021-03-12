import json
import etherscan
import requests
from datetime import datetime, timedelta
from dateutil import tz
import re
from twilio.rest import Client
import os
import time


# returns twilio client
def get_twilio(file):
    with open(file, 'r') as f:
        tw_keys = json.loads(f.read())
    os.environ['TW_SID'] = tw_keys['SID']
    os.environ['TW_AUTH_TOKEN'] = tw_keys['AUTH_TOKEN']
    os.environ['MSG_SVC_SID'] = tw_keys['MSG_SVC_SID']
    tw = Client(tw_keys['SID'], tw_keys['AUTH_TOKEN'])
    return tw

# bloxy api - ** CAUTION VERY FEW CALLS IN TRIAL (less than 50)**
def get_bloxy_api(file):
    with open(file, 'r') as f:
        bx_key = json.loads(f.read())
    return bx_key['API_KEY']

# Get API Key for etherscan (needed to get whale's ETH bal)
def get_ether_api(file):
    with open(file, 'r') as f:
        es_key = json.loads(f.read())
    api_key = es_key['ES_API_KEY']
    es = etherscan.Client(
        api_key=api_key,
        cache_expire_after=5,
    )
    return es

def send_sms(tw_client, msg, number):
    ms_sid = os.environ['MSG_SVC_SID']
    tw_client.messages.create(
        messaging_service_sid=ms_sid,
        body=msg,
        to=number
    )

# NFY contract hash for testing
# contract hashes can be found on the token etherscan pg under contract:
c_hash = "0x1cbb83ebcd552d5ebf8131ef8c9cd9d9bab342bc"

# Will use a list of contract hashes, will be extremely small cap tokens
# list of perhaps 500 (?)
ctr_hash_list = []

# for BLOXY REST API
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
def utc_xfr_bloxy(tx_time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    time = tx_time[:19]  # transaction time
    utc = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    return str(utc.astimezone(to_zone))

def utc_xfr_bitquery(bk_time):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    bk_time = bk_time  # transaction time
    utc = datetime.strptime(bk_time, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    return str(utc.astimezone(to_zone))

# takes an individual's eth address and contract decimal precision
# decimal precision is usually 18
def get_whale_eth_bal(tx, dec_prec, es):
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
        json.dump(data_update, outfile, default=str)

# creates/makes the bitquery request to get DEX trades
# time_interval in minutes
# limit is a number that limits the query response
# writes to a filename (for now, will be done in memory in the future)
def get_bitquery_data(time_interval, limit): # , filename
    pre = datetime.utcnow() - timedelta(minutes=time_interval)
    from_time = pre.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    variables = "{\"limit\":" + str(
        limit) + ",\"offset\":10,\"network\":\"ethereum\",\"from\":\"" + from_time + "\",\"till\":null,\"dateFormat\":\"%Y-%m-%dT%H:%M:%S.000Z\"}"
    payload = {
        "query": 'query ($network: EthereumNetwork!,$limit: Int!,$offset: Int!$from: ISO8601DateTime,$till: ISO8601DateTime){ethereum(network: $network){dexTrades(options:{desc: ["block.height","tradeIndex"], limit: $limit, offset: $offset},date: {since: $from till: $till }) {block {timestamp {time (format: "%Y-%m-%d %H:%M:%S")}height}                          tradeIndex                          protocol                          exchange {                            fullName                          }                          smartContract {                            address {                              address                              annotation                            }                          }                          buyAmount                          buyCurrency {                            address                            symbol                          }                          sellAmount                          sellCurrency {                            address                            symbol                          }                          transaction {                            hash                          }                      }                    }                  }',
        "variables": variables}

    resp = requests.post("https://graphql.bitquery.io/", data=payload)

    return resp

# token_conf = json file that has all tokens we care about
def process_token_addy_bitquery(time_interval, limit, token_conf):
    bit_query = get_bitquery_data(time_interval, limit)
    bit_query_json = json.loads(bit_query.text)
    tokens = open_conf(token_conf)
    for token in tokens:
        tokens[token]["recent_wh_buys"].clear() # always clear out latest tokens list
    dex_trades = bit_query_json["data"]["ethereum"]["dexTrades"]

    for trade in dex_trades:
        alt_symbol = trade["sellCurrency"]["symbol"]
        if alt_symbol == "WETH":  # record could be buy or sell, so forcing it to be the alt-coin, and NOT "WETH"
            alt_symbol = trade["buyCurrency"]["symbol"]


        if alt_symbol in tokens:
            if trade["buyCurrency"]["symbol"] == "WETH" and trade["buyAmount"] > tokens[alt_symbol]["eth_whale_thresh"]: #
                print(trade["sellCurrency"]["symbol"])
                print("thresh: {}".format(tokens[alt_symbol]["eth_whale_thresh"]))

                nyc_time = utc_xfr_bitquery(trade["block"]["timestamp"]["time"])
                # not getting wallet balance in the bitquery MVP (response only has token
                # contract addresses and transaction addresses, I know we could get the
                # balance from the transaction using the etherscan api,
                # but not sure how useful it is at the moment...
                # whale_eth_bal = get_whale_eth_bal()

                # tx_dict = {"symbol": dex_tx["sellSymbol"], "tx_time": nyc_time,
                #            "amount_buy": dex_tx["amountBuy"], "tx_hash": dex_tx["tx_hash"],
                #            "wh_wallet_bal": whale_eth_bal, "tx_sender": dex_tx["tx_sender"]}
                #
                # # adding whale data to config
                # tokens[dex_tx["sellSymbol"]]["recent_wh_buys"].append(tx_dict)
                # tokens[dex_tx["sellSymbol"]]["all_wh_buys"].append(tx_dict)
                #
                # # print info whale to console TODO: add logging
                # message = "A whale sighting!!! \n{} ETH buy \non {} \nfor ticker {}\nwwb: " \
                #           "{} ETH\n".format(dex_tx["amountBuy"], nyc_time, dex_tx["sellSymbol"], whale_eth_bal)
                #
                # # print whale to console
                # print(message + "\n*********************\n")

        #     print("bought {} symbol".format(symbol))

    # close_conf(filename, resp.text)
    # print(json.dumps(json.loads(resp.text), indent=4))
# Takes url and config file
# returns a processed config file (python dict)
# return value should be arg to close_conf() to write data
def process_token_addy(url, conf_file, es, tw, numbers, time_interval):
    r = requests.get(url)
    tx_json_data = json.loads(r.text)
    tx_ct = len(tx_json_data)
    print("\nTotal count of transcations: {}\n".format(tx_ct))
    tokens = open_conf(conf_file)
    symbol = tx_json_data[0]["sellSymbol"]
    if symbol == "WETH": # first record could be buy or sell, so forcing it to be the alt-coin and NOT "WETH"
        symbol = tx_json_data[0]["buySymbol"]
    for token in tokens:
        tokens[token]["recent_wh_buys"].clear() # always clear out latest tokens list
    if tx_ct == 0:
        print("no whale buys in last 20 minutes")
        return tokens
    else:
        for dex_tx in tx_json_data:
            if dex_tx["buySymbol"] == "WETH" and dex_tx["amountBuy"] >= tokens[dex_tx["sellSymbol"]]["eth_whale_thresh"]:

                nyc_time = utc_xfr_bloxy(dex_tx["tx_time"])
                whale_eth_bal = get_whale_eth_bal(dex_tx["tx_sender"], 18, es)
                time.sleep(0.5)

                tx_dict = {"symbol": dex_tx["sellSymbol"], "tx_time" : nyc_time,
                           "amount_buy" : dex_tx["amountBuy"], "tx_hash" : dex_tx["tx_hash"],
                           "wh_wallet_bal" :  whale_eth_bal, "tx_sender" : dex_tx["tx_sender"]}

                # adding whale data to config
                tokens[dex_tx["sellSymbol"]]["recent_wh_buys"].append(tx_dict)
                tokens[dex_tx["sellSymbol"]]["all_wh_buys"].append(tx_dict)

                # print info whale to console TODO: add logging
                message = "A whale sighting!!! \n{} ETH buy \non {} \nfor ticker {}\nwwb: " \
                          "{} ETH\n".format(dex_tx["amountBuy"], nyc_time, dex_tx["sellSymbol"], whale_eth_bal)

                # print whale to console
                print(message + "\n*********************\n")
        buys = tokens[symbol]["recent_wh_buys"]
        # all_buys = tokens[symbol]["all_wh_buys"]
        buys_info = ""
        b_ct = 1
        for buy in buys:
            tx_tm = str(buy["tx_time"])[:19][5:]
            amt = str(buy["amount_buy"])[:6]
            wwb = str(buy["wh_wallet_bal"])[:7]
            addition = "\nBUY {} ->\ntime: {}\namt: {}\nwwb: {}\n".format(b_ct, tx_tm, amt, wwb)
            buys_info += addition
            b_ct += 1
        # commented out code for sending all buys because it will make the text too long.
        # for buy in all_buys:
        #     addition = " |tx_time: {}\namt: {}\nwwb: {}| "\
        #                .format(buy["tx_time"], buy["amount_buy"],buy["wh_wallet_bal"])
        #     all_buys_info += addition
        message = "Whale sighting!! sm: {}, {} buys in {}min!\nETH Thresh: {}\n" \
                  "Buys info: \n{}\n"\
                  .format(symbol, len(buys), time_interval, tokens[symbol]["eth_whale_thresh"], buys_info)
        # send sms to Walt and Patrick
        for num in numbers:
            send_sms(tw, message, num)
        return tokens


if __name__ == "__main__":
    print("hello")
