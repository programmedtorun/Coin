import whale_watch

# NFY contract addy, hashes can be found on etherscan block explorer
c_hash = "0x1cbb83ebcd552d5ebf8131ef8c9cd9d9bab342bc"

# Will use a list of contract hashes (500?), will be extremely small cap tokens
ctr_hash_list = []

# note: in the request we will have to figure out the intervals to segment,
# here I'm segmenting every 60 min in the future we will call build_url
# in a loop and create a list of low caps to poll
time_interval = 1400  # in minutes
ether_api = whale_watch.get_ether_api('ES_API_KEY_FILE.json')
bx = whale_watch.get_bloxy_api('BLOXY_API.json')
tw = whale_watch.get_twilio('TWILIO_STUFF.json')
str_url = whale_watch.build_url(time_interval, c_hash, bx)

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
alert_phone_nums = ["+16462284704", "+15712769543"]
# for num in alert_phone_nums:
# whale_watch.send_sms(tw, "hello this is a test", "+15712769543")
new_whale_data = whale_watch.process_token_addy(str_url, 'whale_conf.json', ether_api, tw, alert_phone_nums, time_interval)
print("\n\nnew whale data is")
print(new_whale_data)
whale_watch.close_conf('whale_conf.json', new_whale_data)