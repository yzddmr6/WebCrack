from urllib.parse import urlparse
from conf.config import *
import requests
from bs4 import BeautifulSoup as BS
import re
from generator.header import get_random_headers
import logs.log as Log
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Parser:
    id = 0
    url = ''
    post_path = ''
    resp_content = ''
    form_content = ''
    username_keyword = ''
    password_keyword = ''
    data = ''
    cms = ''

    def __init__(self, url):
        self.url = url
        self.requests_proxies = crackConfig["requests_proxies"]

    def run(self):
        try:
            self.get_resp_content()
            self.cms_parser()
            self.form_parser()
            self.check_login_page()
            self.captcha_parser()
            self.post_path_parser()
            self.param_parser()
        except Exception as e:
            Log.Error(f"[-] {self.url} Parse Error: " + str(e))
            return False
        return True

    def get_resp_content(self):
        res = requests.get(self.url, timeout=crackConfig["timeout"], verify=False, headers=get_random_headers(),
                           proxies=self.requests_proxies)
        res.encoding = res.apparent_encoding
        self.resp_content = res.text

    def cms_parser(self):
        for cms in cmsConfig.values():
            keyword = cms["keywords"]
            if keyword and (keyword in self.resp_content):
                Log.Info(f"[*] {self.url} 识别到cms: {cms['name']}")
                if cms['alert']:
                    Log.Info(f"[*] {self.url} {cms['note']}")
                self.cms = cms

    def form_parser(self):
        html = self.resp_content
        result = re.findall(".*<form (.*)</form>.*", html, re.S)
        if result:
            form_data = '<form ' + result[0] + ' </form>'
            form_soup = BS(form_data, "lxml")
            self.form_content = form_soup.form
        else:
            raise Exception("Can not get form")

    def check_login_page(self):
        login_keyword_list = parserConfig["login_keyword_list"]
        for login_keyword in login_keyword_list:
            if login_keyword in str(self.form_content).lower():
                return True
        raise Exception("Maybe not login pages")

    def captcha_parser(self):
        captcha_keyword_list = parserConfig["captcha_keyword_list"]
        for captcha in captcha_keyword_list:
            if captcha in self.resp_content.lower():
                raise Exception(f"{captcha} in login page")

    def post_path_parser(self):
        url = self.url
        content = self.form_content
        form_action = str(content).split('\n')[0]
        soup = BS(form_action, "lxml")
        res = urlparse(url)
        try:
            action_path = soup.form['action']
        except:
            self.post_path = url  # 当form中没有action字段时，默认地址为url
            return

        if action_path.startswith('http'):  # action为绝对路径
            path = action_path
        elif action_path.startswith('/'):  # action为根路径
            root_path = res.scheme + '://' + res.netloc
            path = root_path + action_path
        elif action_path == '':  # action为空
            path = url
        else:  # action为同目录下相对路径
            relative_path = url.rstrip(url.split('/')[-1])
            path = relative_path + action_path
        if not path:
            raise Exception("Can not get post path")
        self.post_path = path

    def param_parser(self):
        content = self.form_content
        data = {}
        username_keyword = ''
        password_keyword = ''
        username_keyword_list = parserConfig["username_keyword_list"]
        password_keyword_list = parserConfig["password_keyword_list"]
        for input_element in content.find_all('input'):
            if input_element.has_attr('name'):
                parameter = input_element['name']
            else:
                parameter = ''
            if input_element.has_attr('value'):
                value = input_element['value']
            else:
                value = parserConfig["default_value"]
            if parameter:
                data[parameter] = value

        # 提取username_keyword,password_keyword
        for parameter in data:
            if not username_keyword and parameter != password_keyword:
                for keyword in username_keyword_list:
                    if keyword in parameter.lower():
                        username_keyword = parameter
                        break
            if not password_keyword and parameter != username_keyword:
                for keyword in password_keyword_list:
                    if keyword in parameter.lower():
                        password_keyword = parameter
                        break

        # 弹出reset
        for i in ['reset']:
            for r in list(data.keys()):
                if i in r.lower():
                    data.pop(r)

        if username_keyword and password_keyword:
            self.username_keyword = username_keyword
            self.password_keyword = password_keyword
            self.data = data
        else:
            raise Exception("Can not get login parameter")
