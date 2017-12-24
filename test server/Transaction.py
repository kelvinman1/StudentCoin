from ecdsa import SigningKey, VerifyingKey
import base64
import json
import socket

def deserialize(a):
    return base64.b64decode(a.encode('utf-8'))

class Transaction(object):
    @staticmethod
    def get_balance(adress_id, blocks = False):
        root_balance = 'Zugz8FtJBwq+b1wRzEpZCHI/D8RH45jQszMYX6Zc1z/jm5RHAO+miUBPivIxjq7n'
        balance = 0
        if root_balance == adress_id:
            balance = 10
            print('root')

        if (blocks == False):
            blockchain_data = 'blockchain.dat'
            try:
                f = open(blockchain_data, 'r')
                blocks = f.read()
                f.close()
                blocks = json.loads(blocks)
            except Exception:
                print('err load blockchain')
                return 0

        for i in range(0, len(blocks)):
            block = blocks[i]
            if (block['transaction']['to'] == adress_id):
                balance += block['transaction']['count']
            elif (block['transaction']['from'] == adress_id):
                balance -= block['transaction']['count']

            if (block['miner_adress'] == adress_id):
                balance += block['transaction']['fee']
                balance += round(50 / (i // 4032 + 1), 9)
        print(balance)
        return balance

    @staticmethod
    def verify(adress_id, message, signature):
        vk2 = VerifyingKey.from_string(deserialize(adress_id))
        try:
            assert vk2.verify(signature, message.encode('utf-8'))
        # except BadSignatureError:
        #     return 3
        except Exception:
            return 0
        else:
            return 1

    @staticmethod
    def send(transaction, port = 0):
        UDP_IP = "127.0.0.1"
        UDP_PORT = 5068
        MESSAGE = transaction.encode('utf-8')
        
        print("UDP target IP:", UDP_IP)
        print("UDP target port:", UDP_PORT)
        print("message:", MESSAGE)
        
        sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        
        if port != UDP_PORT:
            sock.sendto( MESSAGE, (UDP_IP, UDP_PORT) )

        # only test code
        if port != UDP_PORT + 1:
            sock.sendto( MESSAGE, (UDP_IP, UDP_PORT+1) )

    def create(self, adress_id, adress_pass, count, fee, new_adress_id):
        balance = Transaction.get_balance(adress_id)
        if (count + fee > balance):
            print('small balance (' + adress_id + ', ' + str(balance) + ')')
            return

        transaction = {
            'from': adress_id,
            'to': new_adress_id, 
            'count': count,
            'fee': fee
        }
        
        sk_string = deserialize(adress_pass)
        sk2 = SigningKey.from_string(sk_string)
        message = json.dumps(transaction)
        signature = sk2.sign(message.encode('utf-8'))

        transaction['sign'] = base64.b64encode(signature).decode('utf-8')
        rez = self.verify(adress_id, message, signature)
        if (rez == 0):
            print('signing error')
        elif (rez == 1):
            print('signing success, sending...')
            self.send(json.dumps(transaction))