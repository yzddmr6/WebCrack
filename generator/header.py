import random
from conf.config import *

useragent_list = generatorConfig["headers_config"]["useragent_list"]
enable = generatorConfig["headers_config"]["enable"]


def get_random_headers():  # 生成随机headers
    if enable:
        UA = random.choice(useragent_list)
        a = str(random.randint(1, 255))
        b = str(random.randint(1, 255))
        c = str(random.randint(1, 255))
        random_XFF = '127.' + a + '.' + b + '.' + c
        random_CI = '127.' + c + '.' + a + '.' + b
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': UA,
            'X-Forwarded-For': random_XFF,
            'Client-IP': random_CI,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            "Referer": "http://www.baidu.com/",
            'Content-Type': 'application/x-www-form-urlencoded'}
    else:
        headers = generatorConfig["rand_headers_config"]["default_headers"]

    return headers
