
# import math
# from pylab import *

# years = 30 * 365 * 24 * 60 * 60
# block_time = 60 * 5
# blocks_count = years // block_time
# print(blocks_count)

# x = range(1, blocks_count)
# y = [round(50 / (i // 4032 + 1), 9) for i in x]

# s = 0
# for j in y:
#     s += j * 4032
# print(s)

# plot(x, y)
# show()
# exit()

from Transaction import Transaction
import json

blockchain_data = 'blockchain.dat'

try:
    f = open(blockchain_data, 'r')
    blocks = f.read()
    f.close()
    blocks = json.loads(blocks)

except Exception:
    print('err load blockchain')


# find adresses
adresses = {}
for block in blocks:
    adresses[block['transaction']['from']] = 1
    adresses[block['transaction']['to']] = 1
    adresses[block['miner_adress']] = 1

# calc balance
for adr in adresses:
    balance = Transaction.get_balance(adr, blocks)
    print(adr + ' ' + str(balance))


