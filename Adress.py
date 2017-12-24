from ecdsa import SigningKey
import base64

def serialize(a):
    return base64.b64encode(a).decode('utf-8')

# tutorial https://github.com/warner/python-ecdsa

class Adress(object):
    def create(self):
        sk = SigningKey.generate()
        vk = sk.get_verifying_key()
        adress_id = serialize(vk.to_string())
        adress_pass = serialize(sk.to_string())

        return (adress_id, adress_pass)