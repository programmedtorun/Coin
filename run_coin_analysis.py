from coin_analysis import Analysis



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


anal = Analysis(coin_list_two)
print("************************************************************************************")
# fin_info = anal.load_cmc_hash()['data']
# for coin in fin_info:
#     if coin['symbol'] == 'GRT':
#         print(coin)
list = anal.get_coin_id_list()
social_list = anal.get_social(list)
ndx_list = anal.create_purchase_ndx(social_list)
print(anal.process_vectors(ndx_list))




# master_hash = anal.load_hash()
#
# print(master_hash["BNB"])
# # list = anal.get_coin_id_list()
# # list_with_social = anal.get_social(list)
# # print(list_with_social)
