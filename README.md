# WebCrack

## 工具简介

WebCrack是一款web后台弱口令/万能密码批量爆破、检测工具。

不仅支持如discuz，织梦，phpmyadmin等主流CMS

并且对于绝大多数小众CMS甚至个人开发网站后台都有效果

在工具中导入后台地址即可进行自动化检测。


## 开发文档

https://yzddmr6.tk/posts/webcrack-release/

## 工具特点

* 多重判断机制，减少误报

* 随机UA 随机X-Forwarded-For 随机Client-IP

* 可以通过域名生成动态字典

* 可以探测系统是否存在因为设计缺陷而造成的万能密码漏洞

* 支持自定义爆破参数


## 使用方法

下载项目
```
git clone https://github.com/yzddmr6/WebCrack
```

安装依赖
```
pip install -r requirements.txt
```

运行脚本
```
>python3 webcrack.py

*****************************************************
*                                                   *
****************    Code By yzddMr6   ***************
*                                                   *
*****************************************************

File or Url:

```

>输入文件名则进行批量爆破，输入URL则进行单域名爆破。

开始爆破

![image](https://user-images.githubusercontent.com/46088090/64511415-d9e64980-d316-11e9-8b19-0487c8bf14fe.png)


爆破的结果会保存在同目录下`web_crack_ok.txt`文件中

![image](https://user-images.githubusercontent.com/46088090/64511693-6a248e80-d317-11e9-9d0c-6114cb194d37.png)


## 自定义配置文件

```
[
    {
        "name":"这里是cms名称",
        "keywords":"这里是cms后台页面的关键字,是识别cms的关键",
        "captcha":"1为后台有验证码，0为没有。因为此版本并没有处理验证码，所以为1则退出爆破",
        "exp_able":"是否启用万能密码模块爆破",
        "success_flag":"登录成功后的页面的关键字",
        "fail_flag":"请谨慎填写此项。如果填写此项，遇到里面的关键字就会退出爆破，用于dz等对爆破次数有限制的cms",
        "alert":"若为1则会打印下面note的内容",
        "note":"请保证本文件是UTF-8格式，并且请勿删除此说明"
    }
]
```

## 警告！

**请勿用于非法用途！否则自行承担一切后果**

## Debug记事本

[Debug记事本](debug.md)


