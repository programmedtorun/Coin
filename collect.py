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
import twitter


class Collect(object):

    # defines the api's that we want to pull in
    def __init__(self, coingecko=false, tw=false, youtube=false, cryptocompare=false):
        self.coingecko = coingecko
        self.tw = tw
        self.youtube = youtube
        self.cryptocompare = cryptocompare
        if youtube:
            with open('YTD_API.json', 'r') as f:
                self.ytd_api_keys = json.loads(f.read())
        if cryptocompare:
            with open('CC_API_KEY_FILE.json', 'r') as f:
                self.cc_api_keys = json.loads(f.read())
        if coingecko:
            self.cg = CoinGeckoAPI()
        if tw:
            self.key_coin_twitter_accts = ["elliotrades",
                                           "MartiniGuyYT",
                                           "IvanOnTech",
                                           "elonmusk",
                                           "michael_saylor",
                                           "MichaelSuppo",
                                           "boxmining",
                                           "AdamHODL",
                                           "CryptosR_Us"
                                           ]
            with open('TW_KEY_FILE.json', 'r') as f:
                self.tw_api_keys = json.loads(f.read())
            self.twitter_api = twitter.Api(consumer_key=self.tw_api_keys["TW_API_KEY"],
                                           consumer_secret=self.tw_api_keys["TW_SECRET_KEY"],
                                           access_token_key=self.tw_api_keys["TW_ACCESS_TOKEN_KEY"],
                                           access_token_secret=self.tw_api_keys["TW_ACCESS_TOKEN_SECRET"])




# Creates a twitter Status obj see docs:
# https://python-twitter.readthedocs.io/en/latest/_modules/twitter/models.html#Status
def get_status_list(twitter_user, tweet_count, tw_api):
    return tw_api.GetUserTimeLine(screen_name=twitter_user, count=tweet_count)


# takes CoinGeckoAPI() obj
# returns a list of the top 7 searched coins on coingecko
# returned coins are dicts
# {
# 'id': 'string',
# 'name': 'string',
# 'symbol': 'string',
# 'market_cap_rank': int,
# 'thumb': 'string',
# 'large': 'string',
# 'score': int
# }

def get_top_seven_symbol(cgapi):
    trend = cgapi.get_search_trending()
    top_seven = []
    for coin in trend["coins"]:
        top_seven.append(coin["item"])
    return top_seven

# returns dfi aggregate data
def get_defi_data(cgapi):
    return cgapi.get_global_decentralized_finance_defi()


# returns list of dicts

# {
# 'description': 'string',
# 'category': 'string',
# 'created_at': '2021-02-03T17:54:34.274Z',
# 'user': 'string',
# 'user_title': 'string',
# 'pin': boolean,
# 'project': dict --> {'type': 'string', 'id': 'string', 'name': 'string', 'symbol': 'string', 'image': dict}
# }

# note category has 'general', 'software release' and 'partnership'
# we can infer that software release and partnership are good news
def get_status_updates(cgapi):
    return cgapi.get_status_updates()["status_updates"]


# will return a dictionary where the keys are coin symbols
# the value is very useful coin information
# to get coin Id call this function example:
# inj_id = get_cc_hash()["INJ"]["Id"]
def get_cc_hash():
    res = requests.get("https://min-api.cryptocompare.com/data/all/coinlist?api_key={}".format(cc_api_keys['CC_API_KEY']))
    text_res = res.text
    j_res = json.loads(text_res)
    return j_res["Data"]


# will get all social data for a coin, must use crypto compare (cc) coin ids
def get_social(coin_id):
    res = requests.get("https://min-api.cryptocompare.com/data/social/coin/latest?api_key={}&coinId={}".format(cc_api_keys['CC_API_KEY'], coin_id))
    text_res = res.text
    j_res = json.loads(text_res)
    print(j_res)


# returns array of arrays price of asset vs currency
def get_mk_chart(symbol, vs_currency, num_days, cgapi):
    mk_chart = cgapi.get_coin_market_chart_by_id(id='1inch', vs_currency='usd', days=20)
    return mk_chart["prices"]


# api key and coin tubers' urls
key = ytd_api_keys['API_KEY_ID']
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


# Look at coin tuber's youtube channel and get the id of their *second* to last video
# get video info - returns dict
def get_vid_info(ct):
    all_vid_info = {}
    for tuber in ct:
        res = requests.get(ct[tuber])
        text_res = res.text
        channel_vids = json.loads(text_res)
        latest_vid = channel_vids["items"][1]  # latest video doesn't have subtitles!:/!will have to get 2nd latest([1])
        ct_vid_info = {}
        all_vid_info[tuber] = ct_vid_info
        ct_vid_info["vid_name"] = latest_vid["snippet"]["title"]
        ct_vid_info["video_id"] = latest_vid["id"]["videoId"]
    return all_vid_info


# Once we have the video's id, we can parse the transcript of the video
# takes a tuber's name and a hash of all tubers video info - return value from get_vid_info()
def create_transcrpt_arry(tuber_name, all_vids):
    transcript_obj = YouTubeTranscriptApi.get_transcript(all_vids[tuber_name]["video_id"])
    transcript = ""
    for di in transcript_obj:
        transcript += di["text"].lower()
        transcript += " "
    return transcript.split()


def get_coin_list():
    coin_list = cg.get_coins_list()
    coin_name_list = []
    for coin in coin_list:
        # coin_name_list.append(coin["symbol"].lower()) # maybe we do not include symbol (ticker) many common words
        coin_name_list.append(coin["name"].lower())
        coin_name_list.append(coin["id"].lower())
    return coin_name_list


# get the common words (cw) between the two lists from
# create_transcript_arry() and get_coin_list()
# generates a list of tupples with 2 values, common word and frequency said word appears in transcript
def get_cw_trans_coin_lst(transcript, coin_name_list):
    common_words = set(transcript) & set(coin_name_list)

    cw_list = list(common_words)

    word_freq = []
    for wd in transcript:
        word_freq.append(transcript.count(wd))
    words_plus_freq = list(zip(transcript, word_freq))

    tupple_list_of_freq = []
    for common_word in cw_list:
        index = transcript.index(common_word)
        tupple_list_of_freq.append(words_plus_freq[index])
    return tupple_list_of_freq
