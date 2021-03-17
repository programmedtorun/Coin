import whale_watch
import schedule
import threading
import time

# TODO: add all coins we want whale watch to monitor (include ETH whale buy thresholds)
# TODO: add logging


# bloxy stuff
# bx = whale_watch.get_bloxy_api('BLOXY_API.json')
# str_url = whale_watch.build_url(time_interval, c_hash, bx)
# whale_data = whale_watch.process_token_addy(str_url, 'whale_conf.json', ether_api, tw, p_nums, time_interval)
# print("\n\nnew whale data is")
# print(whale_data)
# whale_watch.close_conf('whale_conf.json', new_whale_data)

tw = whale_watch.get_twilio('TWILIO_STUFF.json')
alert_phone_nums = ["+16462284704", "+15712769543"]
time_segment = 5
limit = 50000

# run line command --> time python3 whale_watch_app.py > whale_output.txt  2> whale_error.txt &
def flush_logs(error, output):
    open(error, 'w').close()
    open(output, 'w').close()


flush_logs('whale_error.txt', 'whale_output.txt')
print("started")


def job():
    # print("whale_watch running on thread %s" % threading.current_thread())
    print("phones {}, time_segment {}, limit {}".format(alert_phone_nums, time_segment, limit))
    updated_whale_data = whale_watch.process_bitquery(time_segment, limit, 'whale_conf.json', alert_phone_nums, tw)
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
