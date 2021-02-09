from pycoingecko import CoinGeckoAPI
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
from collections import Counter
import requests
import json


key_file = 'YTD_API.json'
api_keys = {}
with open(key_file, 'r') as f:
    api_keys = json.loads(f.read())



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

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
key = api_keys['API_KEY_ID']
et_URL = "https://www.googleapis.com/youtube/v3/search?" \
         "key={}&" \
         "channelId=UCMtJYS0PrtiUwlk6zjGDEMA&part=snippet,id&order=date&maxResults=20".format(key)
mg_URL = "https://www.googleapis.com/youtube/v3/search?" \
         "key={}&" \
         "channelId=UCytNzxSmUqEBychgoKoQssw&part=snippet,id&order=date&maxResults=20".format(key)
it_URL = "https://www.googleapis.com/youtube/v3/search?" \
         "key={}&" \
         "channelId=UCrYmtJBtLdtm2ov84ulV-yg&part=snippet,id&order=date&maxResults=20".format(key)
sm_URL = "https://www.googleapis.com/youtube/v3/search?" \
         "key={}&" \
         "channelId=UCCmJln4C_CszIusbJ_MHmfQ&part=snippet,id&order=date&maxResults=20".format(key)
coin_tubers = {"Elliot": et_URL, "Martini": mg_URL, "Ivan": it_URL, "Suppoman": sm_URL}
all_vid_info = {}  # coin tuber's last video id dictionary = {name: last_video_id}
ch_v = json.loads(requests.get(coin_tubers["Elliot"]).text)
# Look at coin tuber's youtube channel and get the id of their last video
for tuber in coin_tubers:
    res = requests.get(coin_tubers[tuber])
    text_res = res.text
    channel_vids = json.loads(text_res)
    latest_vid = channel_vids["items"][1]  # latest video doesn't have subtitles!:/!will have to get 2nd latest([1])...
    ct_vid_info = {}
    all_vid_info[tuber] = ct_vid_info
    ct_vid_info["vid_name"] = latest_vid["snippet"]["title"]
    ct_vid_info["video_id"] = latest_vid["id"]["videoId"]

# Once we have the video's id, we can parse the transcript of the video
for tuber in all_vid_info:
    print("\n\n\n")
    print("Text for {}'s 2nd latest video -------------------> \n title: {}\n".format(tuber, all_vid_info[tuber]["vid_name"]))
    transcript_obj = YouTubeTranscriptApi.get_transcript(all_vid_info[tuber]["video_id"])
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
    print("------------------------------------------------------------------------------")