import functools
from multiprocessing import Value, Lock

import jwt
from flask import redirect, url_for, request
from jwt import DecodeError
from datetime import datetime, timedelta

from secret import secret
from config import Config

cfg = Config()


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


def increase_counter(c: Value):
    def _increase_counter(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            with c.get_lock():
                c.value += 1

            return f(*args, **kwargs)

        return wrapper

    return _increase_counter


def ip_stats_mw(l: Lock, s: set):
    def _ip_stats(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            with l:
                s.add(request.remote_addr)
            return f(*args, **kwargs)

        return wrapper

    return _ip_stats
