from secret import secret
from flask import Flask, request, url_for, redirect, render_template, make_response
from middleware import increase_counter, is_beta_allowed, ip_stats_mw
from multiprocessing import Value, Lock
from bs4 import BeautifulSoup as bs
from datetime import datetime
from lxml import etree
from config import Config
from uuid import uuid4
import jwt
import json
import autopep8

cfg = Config()
app = Flask(__name__)

AUTO_PEP8_OPTIONS = {
    "max_line_length": 72,
    "recursive": True,
    "aggressive": 3
}

REQUESTS_COUNTER: Value = Value("i", 0)

ip_stats = set()
ip_stats_lock = Lock()


@app.route("/")
@increase_counter(REQUESTS_COUNTER)
@ip_stats_mw(ip_stats_lock, ip_stats)
def index():
    return redirect(url_for("pretty_json"))


@app.route("/pretty_json", methods=["GET", "POST"])
@increase_counter(REQUESTS_COUNTER)
@ip_stats_mw(ip_stats_lock, ip_stats)
def pretty_json():
    pretty_format = "JSON"
    post_url = url_for("pretty_json")

    if request.method == "POST":
        ugly_data = ""
        pretty_data = ""
        try:
            ugly_data = request.form.get("ugly_data")
            ugly_json = json.loads(ugly_data)
            pretty_data = json.dumps(ugly_json, indent=2)
        except Exception as e:
            print(e)
            pretty_data = "Errors in ugly data, check formatting"
        finally:
            return render_template("pretty.html",
                                   pretty_format=pretty_format,
                                   post_url=post_url,
                                   ugly_data=ugly_data,
                                   pretty_data=pretty_data)

    return render_template("pretty.html", pretty_format=pretty_format, post_url=url_for("pretty_json"))


@app.route(cfg.PTBC, methods=["GET"])
@increase_counter(REQUESTS_COUNTER)
@ip_stats_mw(ip_stats_lock, ip_stats)
def get_beta_cookie():
    resp = make_response(redirect(url_for("pretty_json")))
    resp.set_cookie("bc", jwt.encode({"uid": str(uuid4()), "is_beta": True}, secret, algorithm="HS256"))
    return resp


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


@app.route("/pretty_python", methods=["GET", "POST"])
@increase_counter(REQUESTS_COUNTER)
@ip_stats_mw(ip_stats_lock, ip_stats)
def pretty_python():
    pretty_format = "Python"
    post_url = url_for('pretty_python')

    if request.method == "POST":
        ugly_data = ""
        pretty_data = ""
        try:
            ugly_data = request.form.get("ugly_data")
            pretty_data = autopep8.fix_code(ugly_data, options=AUTO_PEP8_OPTIONS)
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


@app.route("/pretty_html", methods=["GET", "POST"])
@increase_counter(REQUESTS_COUNTER)
@ip_stats_mw(ip_stats_lock, ip_stats)
def pretty_html():
    pretty_format = "HTML"
    post_url = url_for('pretty_html')

    if request.method == "POST":
        ugly_data = ""
        pretty_data = ""
        try:
            ugly_data = request.form.get("ugly_data")
            soup = bs(ugly_data)
            pretty_data = soup.prettify()
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


@app.route("/not_beta", methods=["GET"])
@increase_counter(REQUESTS_COUNTER)
@ip_stats_mw(ip_stats_lock, ip_stats)
def not_beta():
    view = request.args.get("view")
    return render_template("not_beta.html", view=view)


@app.errorhandler(404)
@ip_stats_mw(ip_stats_lock, ip_stats)
def page_not_found(e):
    return render_template('404.html'), 404


start_time: datetime


def current_time():
    global start_time
    return datetime.now().strftime("%H:%M:%S %d.%m.%y")


def run_time():
    global start_time
    return (datetime.utcnow() - start_time).seconds


@app.context_processor
def inject_stats():
    global start_time, REQUESTS_COUNTER
    return dict(run_time=run_time(), current_time=current_time(), requests_count=REQUESTS_COUNTER.value,
                uniq_users_count=len(ip_stats))


start_time = datetime.utcnow()

if __name__ == "__main__":
    print("path to beta cook:", cfg.PTBC)
    print(start_time)
    print(start_time.timestamp())
    app.run("0.0.0.0", debug=False)
