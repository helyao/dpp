# -*- coding: utf-8 -*-
"""
Webpage Monitor Module @ Helyao
-------------------------------------------------
Interfaces:

-------------------------------------------------
Change Logs:
    2017-09-27  create
"""
from flask import Flask
from persist import rdb
from config import config

app = Flask(__name__)

@app.route('/')
def getInProxy():
    return rdb['in'].getProxy()

@app.route('/out')
def getOutProxy():
    return rdb['out'].getProxy()

@app.route('/test')
def test():
    return 'Hello World'

def run():
    app.run(host='0.0.0.0', port=config.API_PORT)

if __name__ == '__main__':
    run()