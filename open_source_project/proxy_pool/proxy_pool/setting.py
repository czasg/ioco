class Setting:
    redis_host = 'localhost'
    redis_port = 6379
    redis_score = 10        # 设置基础分数
    redis_key = 'proxy_ip'  # redis key
    redis_min_score = 2     # 最小分数
    redis_pool_size = 500   # 代理词大小
    redis_use_pipe = True   # 使用redis pipeline，提高插入速度
    redis_batch_sep = 100   # 从redis读取数据sep

    proxy_test_url = 'http://fanyi.youdao.com/'  # ... sorry

    async_sem = 10

    allow_status = [200, 302]  # 允许状态码，否则减分

    allow_spider = (
        'xici',
        'iphai',
        'yun',
        'kuai',
    )  # 管理爬虫，暂时只写了四个

    @classmethod
    def get_redis_config(cls):  # 构造redis配置
        return dict(host=cls.redis_host, port=cls.redis_port)


if __name__ == '__main__':
    print(Setting.get_redis_config())
