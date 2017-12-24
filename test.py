import hashlib, random, time, json

def convert_base(num, to_base=10, from_base=10):
    # first convert to decimal number
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    # now convert decimal to 'to_base' base
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]

block_time = 5 * 60
start = time.time()
finish = start + block_time

print(start)
print(finish)

#exit()

hash_arr = []
obj = json.loads('{"miner_adress": "XIhhtD5BprFlsnObmDyxL5xc5QUCX4uKn6839Y4DBpKsnZRMtmhdeMDfVtkKRIZn", "hash_last_block": "hashaaaaaaaaa", "timestamp": 1513948552.0508235, "difficulty": 50, "bust": 87700948419, "transaction": {"from": "XIhhtD5BprFlsnObmDyxL5xc5QUCX4uKn6839Y4DBpKsnZRMtmhdeMDfVtkKRIZn", "to": "yMqqoiz28LIvvyvJ2VDFOHbd2ggASSTiEBssUSkC9QRZ7Fy3p6LCySh/ok4yWqH0", "count": 10, "fee": 0, "sign": "wnERxJEqC5OWxOGBwelJx0CgDSDpv3T6iFmsK2AOiMG8mSisXKbHieDvVJHwxwyQ"}}')

print(obj)

a = -1

while True:
    a += 1

    obj['bust'] = str(a)
    msg = json.dumps(obj)

    m = hashlib.sha1()
    m.update(msg.encode('utf-8'))
    hash = m.hexdigest()

    digit = convert_base(hash, 10, 16)
    print(digit)
    hash_arr.append(int(digit))

    if (time.time() > finish):
        break

print(len(hash_arr))
print(a)
hash_arr.sort()
print(hash_arr[0])