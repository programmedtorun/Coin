from collect import Collect

col = Collect(True, True, True, True)

elliot = col.get_cw_trans_coin_lst("Elliot")

print(elliot)


# cc = col.filter_cc_hash()
# cc_count = 0
# for key in cc.keys():
#     cc_count += 1
# print("cc count is: {}".format(cc_count))
#
# cgg = col.cg_coin_list
#
# cg_count = 0
# for elm in cgg:
#     cg_count += 1
# print("cg count is: {}".format(cg_count))








