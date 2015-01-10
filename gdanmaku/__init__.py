#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from gevent.monkey import patch_all
patch_all()

import redis
from gevent.wsgi import WSGIServer
from flask import Flask, g
from . import settings
from .channel_manager import ChannelManager

app = Flask(__name__)
app.config.from_object(settings)
redis_host=os.environ['OPENSHIFT_REDIS_HOST']
redis_port=os.environ['OPENSHIFT_REDIS_PORT']
redis_password=os.environ['REDIS_PASSWORD']
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)
#r = redis.StrictRedis(host='localhost', port=6379, db=1)
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


from . import views
from . import api
from . import wechat

def main():

    app.debug = True
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
    host_name = os.environ['OPENSHIFT_GEAR_DNS']
	#http_server = WSGIServer(('', 5000), app)
    #print("Serving at 0.0.0.0:5000")
    http_server = WSGIServer((ip, port), app)
    print("Serving at ip:port")
    http_server.serve_forever()
	#http_server = WSGIServer(('', 5000), app)
    #print("Serving at 0.0.0.0:5000")


# vim: ts=4 sw=4 sts=4 expandtab
