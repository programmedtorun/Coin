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
    "HOT",
    "ORN",
    "GRT",
    "RUNE"
]


anal = Analysis(coin_list_two)
list = anal.get_coin_id_list()
list_with_social = anal.get_social(list)
print(list_with_social)
