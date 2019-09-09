# WebCrack

## 工具简介

WebCrack是一款web后台弱口令/万能密码批量爆破、检测工具。

不仅支持如discuz，织梦，phpmyadmin等主流CMS

并且对于绝大多数小众CMS甚至个人开发网站后台都有效果

在工具中导入后台地址即可进行自动化检测。

## 开发文档

https://yzddmr6.tk/2019/09/09/webcrack-release/


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

## 警告！

**请勿用于非法用途！否则自行承担一切后果**

## Debug记事本

[Debug记事本](debug.md)


