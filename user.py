from Adress import Adress
from Transaction import Transaction

adress_id = 'ZBHy1wiUA3g0PDR743RnDJd7dga4YYn4BynZlwprMwh8ezJK8n2CeihU9yczxLle'
adress_pass = 'iNSwComA9fbY8lIz+0uDqgFJ709IiLBp'
adress_id2 = 'Zugz8FtJBwq+b1wRzEpZCHI/D8RH45jQszMYX6Zc1z/jm5RHAO+miUBPivIxjq7n'
#adress_id2 = '36E97mi2ifHJyPi+K7GGTLTDelfoPW07/snVUi8zFZe2v7++MJOse8dbZqPvkuGm' # miner

transaction = Transaction()
transaction.create(adress_id, adress_pass, 10, 0, adress_id2)