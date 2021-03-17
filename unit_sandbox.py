from whale_watch.whale_watch import add_sym_to_ctr_to_whale_conf
from analysis import *
import pathlib

cur_path = pathlib.Path(__file__).parent.absolute()


# use this file for modifying whale_conf and searching for low caps.

# uncomment and run to get fresh data
analysis = Analysis([])
# low_caps = analysis.get_financials(200000, 5000000, 200000)

# analysis.write_low_caps_to_json('low_caps.json', low_caps) #  low_caps.json not currently used. additions are manual

# Uncomment these lines to update whale_conf.json with your additions
# ww_conf = "{}/whale_watch/whale_conf.json".format(cur_path)
# add_sym_to_ctr_to_whale_conf(ww_conf)
