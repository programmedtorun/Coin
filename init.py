from pycoingecko import CoinGeckoAPI
import json



cg = CoinGeckoAPI()

dict = cg.get_search_trending()

for key in dict:
    print(key, '->', dict[key])

for key in dict:
    if key == "coins":
        print("------------------")
        print("Top 7 searched coins: ")
        count = 1
        for dict_2 in dict[key]:
            print("Info for coin #{}:\n{}".format(count, dict_2))
            print("")
            count += 1

# j_obj = json.loads(json_data)
#
# j_fmt_str = json.dumps(j_obj)
# print(j_fmt_str)
