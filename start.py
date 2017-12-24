from Adress import Adress
from Transaction import Transaction
import sys

# adress = Adress()
# (adress_id, adress_pass) = adress.create()
# print('from: ' + adress_id)
# print('pass: ' + adress_pass)
# (adress_id2, adress_pass2) = adress.create()
# print('\n')
# print('to: ' + adress_id2)
# print('2: ' + adress_pass2)
# print('\n')

if len(sys.argv) > 1 and sys.argv[1] == '1':
    f = open('blockchain.dat', 'w')
    f.write('[]')
    f.close()

root_adr   = 'Zugz8FtJBwq+b1wRzEpZCHI/D8RH45jQszMYX6Zc1z/jm5RHAO+miUBPivIxjq7n'
person_adr = 'ZBHy1wiUA3g0PDR743RnDJd7dga4YYn4BynZlwprMwh8ezJK8n2CeihU9yczxLle'
miner_adr  = '36E97mi2ifHJyPi+K7GGTLTDelfoPW07/snVUi8zFZe2v7++MJOse8dbZqPvkuGm'

adress_id = 'Zugz8FtJBwq+b1wRzEpZCHI/D8RH45jQszMYX6Zc1z/jm5RHAO+miUBPivIxjq7n'
adress_pass = '/o49l/oesdaB6cM0Ckf1mPY6SFSqMrlK'
adress_id2 = 'ZBHy1wiUA3g0PDR743RnDJd7dga4YYn4BynZlwprMwh8ezJK8n2CeihU9yczxLle'

transaction = Transaction()
transaction.create(adress_id, adress_pass, 10, 0, adress_id2)