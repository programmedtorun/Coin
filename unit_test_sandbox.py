from collect import Collect
from coin_analysis import Analysis
import urllib
import requests
from pycoingecko import CoinGeckoAPI
import csv

# use this file for simple testing purposes
anal = Analysis([])

# run to get fresh data
low_caps = anal.get_financials(200000, 5000000, 200000)

anal.write_low_caps_to_json('low_caps.json', low_caps)
