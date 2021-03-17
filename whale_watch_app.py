import whale_watch.whale_watch as ww
import schedule
import threading
import time
import pathlib

cur_path = pathlib.Path(__file__).parent.absolute()

# configure whale_watch_app's query calls with time_segment and limit and phone numbers to alert
tw_file = "{}/API_FILES/TWILIO_STUFF.json".format(cur_path)
tw = ww.get_twilio(tw_file)
alert_phone_nums = ["+16462284704", "+15712769543"]
time_segment = 5
limit = 50000


# run line command --> time python3 whale_watch_app.py > whale_watch/whale_output.txt  2> whale_watch/whale_error.txt &
def flush_logs(error, output):
    open(error, 'w').close()
    open(output, 'w').close()


error_file = "{}/whale_watch/whale_error.txt".format(cur_path)
output_file = "{}/whale_watch/whale_output.txt".format(cur_path)
flush_logs(error_file, output_file)
print("started.... whale watch, first sightings in 5 minutes...")


def job():
    # print("whale_watch running on thread %s" % threading.current_thread())
    conf = "{}/whale_watch/whale_conf.json".format(cur_path)
    updated_whale_data = ww.process_bitquery(time_segment, limit, conf, alert_phone_nums, tw)
    ww.close_conf(conf, updated_whale_data)


# Function not used, ask Walt if multi threading is needed
# reference https://schedule.readthedocs.io/en/stable/
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


schedule.every(5).minutes.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)


# bloxy stuff (not used currently, bitquery has replaced our use of bloxy rest api)
# bx = whale_watch.get_bloxy_api('BLOXY_API.json')
# str_url = whale_watch.build_url(time_interval, c_hash, bx)
# whale_data = whale_watch.process_token_addy(str_url, 'whale_conf.json', ether_api, tw, p_nums, time_interval)
# print("\n\nnew whale data is")
# print(whale_data)
# whale_watch.close_conf('whale_conf.json', new_whale_data)
