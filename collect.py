from pycoingecko import CoinGeckoAPI
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
from collections import Counter

class CoinGecko(object):

      CoinGecko = CoinGeckoAPI();
      
      def __INIT(self):

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

transcript_obj = YouTubeTranscriptApi.get_transcript("cl0iNTQUsBU")
transcript = ""
for di in transcript_obj:
    transcript += di["text"].lower()
    transcript += " "
transcript = transcript.split()

coin_list = cg.get_coins_list()
coin_name_list = []
for coin in coin_list:
    coin_name_list.append(coin["name"].lower())
    # coin_name_list.append(coin["symbol"].lower()) # maybe we do not include symbol (coin ticker) because many common words here i.e. "but"
    coin_name_list.append(coin["id"].lower())
common_words = set(transcript) & set(coin_name_list)

l_common_words = list(common_words)
print("common words are: ")
print(l_common_words)

word_freq = []
for w in transcript:
    word_freq.append(transcript.count(w))
words_plus_freq = list(zip(transcript, word_freq))

print("******************")
print("frequency of common word said in video")
for common_word in l_common_words:
    index = transcript.index(common_word)
    print(words_plus_freq[index])

