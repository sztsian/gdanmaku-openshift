#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import os

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass

from gevent.monkey import patch_all
patch_all()

import redis
from gevent.wsgi import WSGIServer
from flask import Flask, g
import settings
import channel_manager

app = Flask(__name__)
app.config.from_object(settings)
redis_host=os.environ['OPENSHIFT_REDIS_HOST']
redis_port=os.environ['OPENSHIFT_REDIS_PORT']
redis_password=os.environ['REDIS_PASSWORD']
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)
chan_mgr = ChannelManager(app, r)
with app.app_context():
    chan_mgr.new_channel("demo", desc=u"演示频道, 发布、订阅均无需密码")


@app.before_request
def set_channel_manager():
    g.channel_manager = chan_mgr
    try:
        r.ping()
    except:
        r.connection_pool.reset()
    g.r = r


import views
import api
import wechat

#def main():
app.debug = True
ip = os.environ['OPENSHIFT_PYTHON_IP']
port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
host_name = os.environ['OPENSHIFT_GEAR_DNS']
http_server = WSGIServer((ip, port), app)
print("Serving at ip:port")
http_server.serve_forever()


# vim: ts=4 sw=4 sts=4 expandtab
