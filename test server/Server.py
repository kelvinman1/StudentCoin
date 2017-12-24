from threading import Thread
import time
import json
import socket
import base64
import random
import hashlib
from Transaction import *

buffer_size = 1024 * 10 # 10kB
server_delay = 1
miner_delay = 1
blockchain_data = 'blockchain.dat'
count_nodes_to_send = 10

def convert_base(num, to_base=10, from_base=10):
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]

class MyThread(Thread):
    def __init__(self, name, func, arr = []):
        Thread.__init__(self)
        self.name = name
        self.func = func
        self.arr = arr
    
    def run(self):
        if (len(self.arr) > 0):
            self.func(self.arr)
        else:
            self.func()

class Server(object):
    def __init__(self, miner_adress):
        self.miner_adress = miner_adress
        self.transactions = []
        self.difficulty = self.get_difficulty()
        self.blockchain = []
        self.foundBlocks = {}
        
        self.sha1 = hashlib.sha1()

        self.load_blockchain()

        syncThread = MyThread('1', self.sync)
        syncThread.start()

        minerThread = MyThread('2', self.miner)
        minerThread.start()

    def get_difficulty(self):
        return 117584694937785764043395930552242964531886593

    def prepare_message(self, msg):
        transaction = json.loads(msg)
        if 'block_num' in transaction:
            print('found block')
            print(transaction)
            self.foundBlocks[transaction['block_num']] = True
        else:
            # check sign
            message = {}
            for i in ['from', 'to', 'count', 'fee']:
                message[i] = transaction[i]
            msg = json.dumps(message)
            sign = base64.b64decode(transaction['sign'])
            rez = Transaction.verify(transaction['from'], msg, sign)
            if (rez == 1):
                balance = Transaction.get_balance(message['from'], self.blocks)
                if (message['count'] + message['fee'] <= balance):
                    message['sign'] = transaction['sign']
                    self.transactions.append(message)
                else:
                    print('small balance (' + message['from'] + ', ' + str(balance) + ')')

    def sync(self):
        UDP_PORT = 5068
        sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        try:
            sock.bind( ('0.0.0.0', UDP_PORT) )
            self.port = UDP_PORT
            while True:
                data = sock.recv(buffer_size)
                self.prepare_message(data)
                time.sleep(server_delay)
        except OSError:
            # only test code
            print('changing port')
            self.port = UDP_PORT + 1
            sock.bind( ('0.0.0.0', UDP_PORT + 1) )
            while True:
                data = sock.recv(buffer_size)
                self.prepare_message(data)
                time.sleep(server_delay)

    def send_block(self, block, block_index):
        block['block_num'] = block_index
        msg = json.dumps(block)
        Transaction.send(msg, self.port)

    def load_blockchain(self):
        try:
            f = open(blockchain_data, 'r')
            self.blocks = f.read()
            f.close()
            self.blocks = json.loads(self.blocks)
        except Exception:
            print('err load blockchain')

    def save_blocks_helper(self):
        tmp = json.dumps(self.blocks)
        sw = open(blockchain_data, 'w')
        sw.write(tmp)
        sw.close()

    def save_blocks(self):
        saveThread = MyThread('3', self.save_blocks_helper)
        saveThread.start()

    def add_block(self, block):
        self.blocks.append(block)
        self.save_blocks()

    def get_hash_last_block(self):
        if (len(self.blocks) > 0):
            block = json.dumps({})
            self.sha1.update(block.encode('utf-8'))
            hash = self.sha1.hexdigest()
            return hash
        return ''

    def delete_last_transaction(self):
        if (len(self.transactions) != 1):
            self.transactions = self.transactions[1:len(self.transactions)]
        else:
            self.transactions = []

    def create_block(self):
        transaction = self.transactions[0]
        t = time.time()
        self.foundBlocks[len(self.blocks)] = False
        while True:
            for offset in range(0, 100):
                if self.foundBlocks[len(self.blocks)]:
                    print('block is Found')
                    self.delete_last_transaction()
                    return
                timestamp = time.time()
                bust = random.randint(0, 100000000000)
                block = {
                    'miner_adress': self.miner_adress,
                    'hash_last_block': self.get_hash_last_block(),
                    'timestamp': timestamp + offset,
                    'difficulty': self.difficulty,
                    'bust': bust,
                    'transaction': transaction
                }
                dump = json.dumps(block)
                self.sha1.update(dump.encode('utf-8'))
                hash = self.sha1.hexdigest()
                digit = convert_base(hash, 10, 16)
                print(digit)
                if (self.difficulty > int(digit)):
                    self.send_block(block, len(self.blocks))
                    self.add_block(block)
                    self.delete_last_transaction()
                    print('minutes: ' + str((time.time() - t) / 60))
                    return

    def miner(self):
        while True:
            if (len(self.transactions) > 0):
                self.transactions.sort(key = lambda x: x['fee'])
                self.create_block()
            time.sleep(miner_delay)

server = Server('36E97mi2ifHJyPi+K7GGTLTDelfoPW07/snVUi8zFZe2v7++MJOse8dbZqPvkuGm')