#!/usr/bin/env python

import math
import os
import subprocess
import copy
import time
from redis import StrictRedis
import json
from functools import wraps
from multiprocessing import Pool
from bottle import (request, run, get, template, static_file, default_app,
                    debug)


redis = StrictRedis(host="localhost")

def cached(function):
    @wraps(function)
    def wrapper(*args, **kwds):
        key = "ping:cache:"+function.__name__
        if redis.exists(key):
            return json.loads(redis.get(key).decode("utf-8"))
        else:
            ret = function(*args, **kwds)
            redis.set(key, json.dumps(ret))
            redis.expire(key, 30)
            return ret
    return wrapper


targets = {}

def update():
    from config import targets as tar
    for group_name in tar:
        group = tar[group_name]
        for name in group:
            if not "host" in group[name]:
                group[name]["host"] = name
    global targets
    targets = tar

update()

DEVNULL = open(os.devnull, 'wb')


def ping(host, timeout=1):
    args = [
        "ping",
        "-c",
        "1",
        "-w",
        str(timeout),
        host
    ]
    ping = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=DEVNULL)
    out, _ = ping.communicate()
    if ping.returncode != 0:
        return -1
    rtt = math.floor(float(str(out).split("\n")[-1].split("/")[-2]))
    return rtt

@get("/")
def route_index():
    return template("index", targets=targets)


@get("/ping")
@cached
def route_ping_all():
    pool = Pool()

    tar = copy.deepcopy(targets)
    for group_name in tar:
        group = tar[group_name]
        for name in group:
            def outer(name, group):
                def save(ret):
                    group[name]["rtt"] = ret
                pool.apply_async(ping, args=[group[name]["host"]], callback=save)
            outer(name, group)

    pool.close()
    pool.join()
    return {"targets": tar}


@get("/i/style")
def route_style():
    return static_file("style.css", root="static")


@get("/i/script")
def route_style():
    return static_file("script.js", root="static")


if __name__ == "__main__":
    run(host='0.0.0.0', port=8080)

app = default_app()
