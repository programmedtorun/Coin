import whale_watch
import schedule
import threading
import time

# ether_api = whale_watch.get_ether_api('ES_API_KEY_FILE.json')
# TODO: add all coins we want whale watch to monitor (include ETH whale buy thresholds)
# TODO: add logging

# bloxy stuff
# bx = whale_watch.get_bloxy_api('BLOXY_API.json')
# str_url = whale_watch.build_url(time_interval, c_hash, bx)
# (OPEN CONF FILE ITERATE THROUGH TOKENS AND PROCESS THEIR ADDYS: via building list of ctr hashes
# then iterate through the list to build each url and have a list of urls, then iterate thr urls and process token adds)
# uncomment to run
# for num in alert_phone_nums:
# whale_watch.send_sms(tw, "hello this is a test", "+15712769543")
# new_whale_data = whale_watch.process_token_addy(str_url, 'whale_conf.json', ether_api, tw, alert_phone_nums, time_interval)
# print("\n\nnew whale data is")
# print(new_whale_data)
# whale_watch.close_conf('whale_conf.json', new_whale_data)
#________________________________________________________________________________
tw = whale_watch.get_twilio('TWILIO_STUFF.json')
alert_phone_nums = ["+16462284704", "+15712769543"]

def job():
    # print("whale_watch running on thread %s" % threading.current_thread())
    updated_whale_data = whale_watch.process_bitquery(5, 10000, 'whale_conf.json', alert_phone_nums, tw)
    whale_watch.close_conf('whale_conf.json', updated_whale_data)

# Function not used, ask Walt if multi threading is needed
# reference https://schedule.readthedocs.io/en/stable/
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)







