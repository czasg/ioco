#!/usr/bin/python3
# -*- utf-8 -*-
from flask import Flask

from proxy_pool.database.redis_man import Redis
from proxy_pool.setting import Setting as config

app = Flask(__name__)
redis_client = Redis.from_setting(config)


@app.route('/')
def index(): return 'hello proxy'


@app.route('/proxy')
def get_random_proxy(): return redis_client.random()


@app.route('/proxy/count')
def get_proxy_count(): return str(redis_client.count())


def main():
    app.run()


if __name__ == '__main__':
    main()
