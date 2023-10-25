from Crypto.Util.number import getPrime, bytes_to_long

flag = bytes_to_long(b'redacted')

p = getPrime(1024)
q = getPrime(1024)

n = p * q
phi = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, phi)
x = pow(p, 2) - pow(q, 2)

c = pow(flag, e, n)

print(f'{n = }')
print(f'{e = }')
print(f'{c = }')
print(f'{x = }')
