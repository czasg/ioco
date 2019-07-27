import os
import argparse
import logging
import traceback

from importlib import import_module
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

current_path = os.path.dirname(os.path.abspath(__file__))
module = {
    'spider_module': 'proxy_pool.spider.spider_man',
    'checker_module': 'proxy_pool.check.checker_man',
    'api_module': 'proxy_pool.api.api_man',
}

if __name__ == '__main__':
    try:
        parse = argparse.ArgumentParser(description='Proxy Pool')
        parse.add_argument('func', help='指定模块')
        parse.add_argument("--log", "-m", help="输出到日志文件", action="store_true")
        args = parse.parse_args()
        func, log = args.func, args.log
        if log:
            hdr = TimedRotatingFileHandler(os.path.join(current_path, "proxy_pool.log"),
                                           when="d", backupCount=3)
            formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
            hdr.setFormatter(formatter)
            logger.addHandler(hdr)
        if not func.startswith(('spider', 'checker', 'api')):
            raise Exception('Error Module')
        path = [path for name, path in module.items() if name.startswith(func)][0]
        module = import_module(path)
        getattr(module, 'main')()
    except:
        logger.error(traceback.format_exc())
