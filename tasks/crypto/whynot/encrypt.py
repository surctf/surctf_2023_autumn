import os
import random
from Crypto.Util.strxor import strxor

with open('input.txt', 'rb') as r:
    text = r.read()

len_key = random.randint(13, 37)

key = os.urandom(len_key)

key *= len(text)

text *= len_key

cipher_text = strxor(text, key)

with open('output.txt', 'w') as w:
    w.write(cipher_text.hex())