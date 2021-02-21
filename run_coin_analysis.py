from coin_analysis import Analysis
from collect import Collect
import urllib
import requests
from pycoingecko import CoinGeckoAPI
import csv
import json
import time

coin_list = [
    "INJ",
    "FTM",
    "POLS",
    "PAID",
    "MKR",
    "ANKR",
    "BMI",
    "YFI",
    "RVN",
    "UNI",
    "DODO",
    "1INCH",
    "ZIL",
    "HOT",
    "ORN",
    "GRT",
    "RUNE"
]
coin_list_two = [
    "DODO",
    "ZIL",
    "ORN",
    "GRT"
]
print("Collecting hot coins to analyze...")
time.sleep(2)
print("...........")
time.sleep(2)
col = Collect(True, True, True, True)
top_seven_list = []
for coin in col.get_top_seven_symbol():
    top_seven_list.append(coin['symbol'])
collect_statuses = col.get_status_updates()
recent_status_list = list(collect_statuses.keys())
coins_to_analyze = list(set(top_seven_list) & set(recent_status_list)) + list(set(top_seven_list) - set(recent_status_list))
print("analyzing {} coins..".format(len(coins_to_analyze)))
time.sleep(2)
print("...........")
print("coins to analyze are: {}".format(coins_to_analyze))
time.sleep(1.5)
print("************************************************************************************")
anal = Analysis(coins_to_analyze)
print("pulling in data...")
time.sleep(1.5)
print("writing files...")
anal.create_cmc_hash_file()
anal.create_cc_hash_file()
time.sleep(1.5)
print(".......................")
print("reading files and creating lists to be analyzed...")
time.sleep(1)
list = anal.get_coin_id_list()
social_list = anal.get_social(list)
print("creating indexed list and processing vectored list")
ndx_list = anal.create_purchase_ndx(social_list)
final_list_rank = anal.process_vectors(ndx_list)
print(final_list_rank)
time.sleep(2)
print("coins to buy are as follows:")
print("************************************************************")
number = len(final_list_rank)
for coin in final_list_rank:
    print("Coin #{}, symbol: {}, buy score: {}, market_cap: {}".format(number, coin['cc_symbol'], coin['buy_level'], coin['market_cap']))
    number -= 1
    print("###########################")
# fin_info = anal.load_cmc_hash()['data']
# for coin in fin_info:
#     if coin['symbol'] == 'GRT':
#         print(coin)






# master_hash = anal.load_hash()
#
# print(master_hash["BNB"])
# # list = anal.get_coin_id_list()
# # list_with_social = anal.get_social(list)
# # print(list_with_social)
