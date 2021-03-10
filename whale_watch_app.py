import whale_watch
import json
import etherscan


# Get API Key for etherscan (needed to get whale's ETH bal)
with open('ES_API_KEY_FILE.json', 'r') as f:
    es_key = json.loads(f.read())
api_key = es_key['ES_API_KEY']
es = etherscan.Client(
    api_key=api_key,
    cache_expire_after=5,
)

# get current eth price (not needed at the moment)
# cur_eth_pr = es.get_eth_price()

# NFY contract hash for testing
# contract hashes can be found on the token etherscan pg under contract:
c_hash = "0x1cbb83ebcd552d5ebf8131ef8c9cd9d9bab342bc"

# Will use a list of contract hashes, will be extremely small cap tokens
# list of perhaps 500 (?)
ctr_hash_list = []

# bloxy api - ** CAUTION VERY FEW CALLS IN TRIAL (less than 50)**
api = "ACCbkmobSFuMs"




# note: in the request we will have to figure out the intervals to segment,
# here I'm segmenting every 60 min in the future we will call build_url
# in a loop and create a list of low caps to poll
str_url = whale_watch.build_url(60, c_hash, api)


# TODO:
# TODO: add text alerting
# TODO: format buy info for message
# TODO: add logging
# TODO: add all coins we want whale watch to monitor (include ETH whale buy thresholds)
# TODO: add looping mechanism for processing all requests(each request is to a different contract address)
# TODO: add job scheduling
# TODO: buy bloxy api for 1 month to test


# (OPEN CONF FILE ITERATE THROUGH TOKENS AND PROCESS THEIR ADDYS: via building list of ctr hashes
# then iterate through the list to build each url and have a list of urls, then iterate thr urls and process token adds)
# uncomment to run
# new_whale_data = whale_watch.process_token_addy(str_url, 'whale_conf.json')
# print("\n\nnew whale data is")
# print(new_whale_data)
# whale_watch.close_conf('whale_conf.json', new_whale_data)