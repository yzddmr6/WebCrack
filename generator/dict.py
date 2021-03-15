import re
from conf.config import *


def gen_dict(url):
    username_list, password_list = gen_base_dict()
    if generatorConfig["dict_config"]["domain_dict"]["enable"]:
        domain_user_dict, domain_pass_dict = gen_domain_dict(url)
        if domain_user_dict and domain_pass_dict:
            username_list.extend(domain_user_dict)
            password_list.extend(domain_pass_dict)
    if username_list and password_list:
        return username_list, password_list
    else:
        raise Exception("[-] 字典生成失败！")


def gen_sqlin_dict():
    sqlin_user_dict = generatorConfig["dict_config"]["sqlin_dict"]["payload_list"]
    sqlin_pass_dict = sqlin_user_dict
    return sqlin_user_dict, sqlin_pass_dict


def gen_base_dict():
    base_username_list = generatorConfig["dict_config"]["base_dict"]["username_list"].copy()
    base_password_list = generatorConfig["dict_config"]["base_dict"]["password_list"].copy()
    return base_username_list, base_password_list


def gen_domain_dict(url):
    domain_user_dict = []
    domain_pass_dict = []
    tmp_dict = []
    suffix_list = generatorConfig["dict_config"]["domain_dict"]["suffix_list"]
    list1 = url.split('/')
    host = list1[2].split(":")[0]
    compile_ip = re.compile(
        '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
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
            domain_pass_dict.append(part)
        for u in range(i):  # 生成url字典2
            list3 = list2[u]
            if len(list3) < 5:
                continue
            tmp_dict.append(list3)
        for i in tmp_dict:
            for suffix in suffix_list:
                u = i + suffix
                domain_pass_dict.append(u)
        return domain_user_dict, domain_pass_dict
    else:
        return False, False
