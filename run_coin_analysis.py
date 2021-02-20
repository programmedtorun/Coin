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
    "UNI",
    "DODO",
    "1INCH",
    "ZIL",
    "HOT",
    "ORN",
    "GRT",
    "RUNE"
]


anal = Analysis(coin_list_two)

anal.create_hash_file()

