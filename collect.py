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
import time


class Collect(object):

    # defines the api's that we want to pull in
    def __init__(self, coingecko=False, tw=False, youtube=False, cryptocompare=False):
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
            self.cg_coin_list = self.cg.get_coins_list()
        else:
            self.cg_coin_list = []
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
        self.words_not_good_coins = ["MISS", "FOR", "ON", "YOU", "BEST", "IN", "WHO", "TIME", "OF",
                                     "NEXT", "EVENT", "ARE", "ME", "LOT", "MORE", "AND", "LIVE", "TODAY", "ONE"]

    # TODO fix weird bug - multiple 'UNI' keys perhaps will only use cryptocompare API though
    def delete_extra_uni(self):
        idx_to_del = []
        ct = 0
        c_list = self.cg_coin_list
        for coin in c_list:
            if coin['id'] == "unicorn-token" or coin['id'] == 'universe-token':
                idx_to_del.append(ct)
                print("appending index: {}".format(ct))
            ct += 1
        for blah in idx_to_del:
            print("index to delete is: ")
            del c_list[blah]
        return c_list

    # returns a json object, not right this second, now returning python dict for testing
    # we might just use cryptocompare for dynamic config creation instead of coin gecko
    def collect_all(self, tweet_count):
        py_obj = {}
        master_list = self.delete_extra_uni()
        tweeted_coins = self.get_coins_in_recent_tweets(tweet_count)  # returns a list of coins coin tweeters have tweeted last (arg) tweets
        for coin in master_list:
            # can not make the below requests
            # because of rate limit! need to cut down on the
            # number of coins we analyze..
            if (coin['symbol'].upper() in tweeted_coins) or (coin['name'].upper() in tweeted_coins) or (coin['id'].upper() in tweeted_coins):
                py_obj[coin['symbol'].upper()] = {"cg_id": coin['id'],
                                                  "tweeted": True
                                                  # "cg_detail": self.cg.get_coin_by_id(coin['id']),
                                                  # "cg_status_update": self.cg.get_coin_status_updates_by_id(coin['id'])
                                                  }
            else:
                py_obj[coin['symbol'].upper()] = {"cg_id": coin['id'],
                                                  "tweeted": False
                                                  # "cg_detail": self.cg.get_coin_by_id(coin['id']),
                                                  # "cg_status_update": self.cg.get_coin_status_updates_by_id(coin['id'])
                                                  }
        rank_dict = self.get_top_seven_symbol() # adding key, value if it's a top coingecko searched coin
        for item in rank_dict:
            py_obj[item['symbol']]['market_cap_rank'] = item['market_cap_rank']
            py_obj[item['symbol']]['top_coin_score'] = item['top_coin_score']
        status_dict = self.get_status_updates() # adding status (again only if sw release or partnership announcment
        for item in status_dict.keys():
            py_obj[item]['status_dict'] = status_dict[item]
        # TODO add more additions to this json object. tweets, youtube, cryptocompare
        # now i am returning a python dict for testing, however this be converted into json via something like
        # json.dumps(py_obj)
        return py_obj

    # note category has 'general', 'software release' and 'partnership'
    # we can infer that software release and partnership are good news
    # removing 'general' category until we figure out if it is really good news, could be bad...
    def get_status_updates(self): # added to collect_all
        final_status_updates = {}
        status_updates = self.cg.get_status_updates()["status_updates"]
        for status in status_updates: # I think we only care about status updates that have a symbol (some don't and they are probably project updates that have yet to launch
            if ('symbol' in status['project']) and (status['category'] != 'general'):
                final_status_updates[status['project']['symbol'].upper()] = status
        return final_status_updates

    # returns a list of the top 7 searched coins on coingecko
    # score key has a value from 0 to 6, 0 is the top searched coin
    # {'symbol': market_cap_rank, "score": 4}
    def get_top_seven_symbol(self): # added to collect_all
        if not self.coingecko:
            return []
        else:
            trend = self.cg.get_search_trending()
            top_seven = []
            for coin in trend["coins"]:
                top_seven.append({"symbol": coin["item"]["symbol"].upper(), "market_cap_rank": coin["item"]["market_cap_rank"],
                                  "top_coin_score": coin["item"]["score"]})
            return top_seven

    # Removes coins from get_cc_hash() that are not trading, as of this message around 1220 coins
    def filter_cc_hash(self):
        hash = self.get_cc_hash()
        keys_to_del = []
        for key in hash:
            if not hash[key]["IsTrading"]:
                keys_to_del.append(key)
        for key in keys_to_del:
            del hash[key]
        return hash

    # will return a dictionary where the keys are coin symbols
    # the value is very useful coin information
    # to get coin Id call this function example:
    # inj_id = get_cc_hash()["INJ"]["Id"]
    def get_cc_hash(self):
        if not self.cryptocompare:
            return {}
        else:
            res = requests.get(
                "https://min-api.cryptocompare.com/data/all/coinlist?api_key={}".format(self.cc_api_keys['CC_API_KEY']))
            text_res = res.text
            j_res = json.loads(text_res)
            return j_res["Data"]

    # Creates a twitter Status obj see docs:
    # https://python-twitter.readthedocs.io/en/latest/_modules/twitter/models.html#Status
    # this returns 1 list of every one in key_coin_twitter_accts each list element is one word
    def get_tw_status_list(self, tweet_count):
        all_tweets = []
        for tweeter in self.key_coin_twitter_accts:
            tweets = self.twitter_api.GetUserTimeline(screen_name=tweeter, count=tweet_count)
            tweets = [tweet.text.split() for tweet in tweets]
            flat_list = [item.upper() for sublist in tweets for item in sublist]
            all_tweets.extend(flat_list)
        return all_tweets

    def get_coins_in_recent_tweets(self, tweet_count): # added to collect_all
        tweet_list = self.get_tw_status_list(tweet_count)
        filtered_hash = list(self.filter_cc_hash().keys())
        full_coin_list = []
        for coin in self.cg_coin_list:
            if coin['symbol'].upper() in filtered_hash:
                full_coin_list.append(coin['id'].upper())
                full_coin_list.append(coin['symbol'].upper())
                full_coin_list.append(coin['name'].upper())
        dollar_coin_list = [("$" + coin) for coin in full_coin_list]
        hashtag_coin_list = [("#" + coin) for coin in full_coin_list]
        dollar_f_hash_lst = [("$" + coin) for coin in filtered_hash]
        hashtag_f_hash_lst = [("#" + coin) for coin in filtered_hash]
        added_list = filtered_hash + full_coin_list + dollar_coin_list + \
                    hashtag_coin_list + dollar_f_hash_lst + hashtag_f_hash_lst
        final_list = list(set(added_list) - set(self.words_not_good_coins))
        return list(set(tweet_list) & set(final_list))


    # will get all social data for ONE COIN, must use crypto compare (cc) coin ids
    def get_social(self, coin_id):
        res = requests.get("https://min-api.cryptocompare.com/data/social/coin/latest?api_key={}&coinId={}".format(
            cc_api_keys['CC_API_KEY'], coin_id))
        text_res = res.text
        j_res = json.loads(text_res)
        print(j_res)


# TODO need to add below methods (general behavior to Collect class
# returns dfi aggregate data not really needed at the moment i don't think
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

# returns array of arrays price of asset vs currency
def get_mk_chart(symbol, vs_currency, num_days, cgapi):
    mk_chart = cgapi.get_coin_market_chart_by_id(id='1inch', vs_currency='usd', days=20)
    return mk_chart["prices"]


# api key and coin tubers' urls
#key = ytd_api_keys['API_KEY_ID']
# et_URL = "https://www.googleapis.com/youtube/v3/search?" \
#          "key={}&" \
#          "channelId=UCMtJYS0PrtiUwlk6zjGDEMA&part=snippet,id&order=date&maxResults=20".format(key)
# mg_URL = "https://www.googleapis.com/youtube/v3/search?" \
#          "key={}&" \
#          "channelId=UCytNzxSmUqEBychgoKoQssw&part=snippet,id&order=date&maxResults=20".format(key)
# it_URL = "https://www.googleapis.com/youtube/v3/search?" \
#          "key={}&" \
#          "channelId=UCrYmtJBtLdtm2ov84ulV-yg&part=snippet,id&order=date&maxResults=20".format(key)
# sm_URL = "https://www.googleapis.com/youtube/v3/search?" \
#          "key={}&" \
#          "channelId=UCCmJln4C_CszIusbJ_MHmfQ&part=snippet,id&order=date&maxResults=20".format(key)
#
# coin_tubers = {"Elliot": et_URL, "Martini": mg_URL, "Ivan": it_URL, "Suppoman": sm_URL}


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
    coin_list = self.cg_coin_list
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
