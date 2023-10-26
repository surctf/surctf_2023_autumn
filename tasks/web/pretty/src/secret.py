import datetime
import random
import string

random.seed(int(datetime.datetime.utcnow().timestamp()))
secret = ''.join([random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(32)])
