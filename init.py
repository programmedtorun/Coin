from pycoingecko import CoinGeckoAPI


cg = CoinGeckoAPI()

trend = cg.get_search_trending()

# coins key is what we need in trend
for key in trend:
    print(key, '->', trend[key])

print("------------------")
print("Top 7 searched coins: ")
count = 1
for coin_dict in trend["coins"]:
    print("Info for coin #{}:\n{}".format(count, coin_dict))
    print("")
    count += 1

print("*************************")
# not really very useful
one_inch = cg.get_coin_history_by_id(id='1inch', date='01-12-2020')
for blah in one_inch:
    print("{} --> {}".format(blah, one_inch[blah]))

print("*************************")
# could be useful gives list of arrays for price comparison
mk_ch = cg.get_coin_market_chart_by_id(id='1inch', vs_currency='usd', days=20)
for price_pair in mk_ch["prices"]:
    print(price_pair)

print("*************************")

