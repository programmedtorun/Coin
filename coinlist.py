import json

'''
contains generic information about each coin. Needed to tie this
entire ball of wax together. It's in a JSON config, and read into a
python dictionary of dictionaries. Stuff like coin name, ticker,
category etc. NOT dynamic market information though. Thats acquired
every hour and changes. This is anything that is mostly static about
the coin. Since it's JSON it can be modified without concern about
changing the schema globally.
'''
class CoinList()

      Data = {}
      
      def __init__(self, coinJsonFile):
      	        with open(filename) as f:
		Data = json.load(f)

      def coins(self):
      	  return Data;

  def coin(self, ticker):
	      return Data[ticker];
      	  
