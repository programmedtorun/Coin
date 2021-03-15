from collect import Collect
from coin_analysis import Analysis
import urllib
import requests
from pycoingecko import CoinGeckoAPI
import csv

# use this file for simple testing purposes
anal = Analysis([])

# run to get fresh data
anal.get_financials()
