#!/usr/bin/env python
# -*-coding:utf8-*-
#############################################################################################################
#
# File      ：   utils.py
# Author    ：   luliying
# Brief     ：   define setup and teardown works for each testcase class
# 
# Version   ：   1.0.2
# Date      ：   29 Oct 2015
# 
# History   ：   
#                1.0.2  luliying   2015.10.29  add EAP220/Firefox HTTP headers
#                       luliying   2015.10.28  add cls.dutMode
#                1.0.1  luliying   2015.10.26  modify reboot function, add reset function
#                1.0.0  chenqinbo  2015.08.21  create the file, add class EAPLoginSession
#
#############################################################################################################


import requests
import hashlib
import unittest
import json
import sys
import time
import ConfigParser
import os


# 读配置文件
cf = ConfigParser.ConfigParser()
cf.read("dut.ini")
username = cf.get("basic", "USERNAME")
password = cf.get("basic", "PASSWORD")
ip       = cf.get("basic", "IP")

# MD5加密
passwordMD5 = hashlib.md5(password.encode("utf8")).hexdigest().upper()

# 伪装头部
header_firefox = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "http://" + ip + "/",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache"
                }

header_eap220 = {"Referer": "http://" + ip + "/"}


# 父类，做每类测试的前置和收尾工作
class EAPLoginSession(unittest.TestCase):

    # 被子类调用，测试前登录
    @classmethod
    def setUpClass(cls):
        print "\nTesting: " + cls.__name__
        s = requests.session()
        # EAP120/220获取Cookie
        res = s.get("http://%s/"%(ip))
        # EAP320获取Cookie
        res = s.get("http://%s/data/login.json"%(ip))
        cls.dutMode = res.json()["dutMode"]
        data = {"username": username, "password": passwordMD5 }
        res = s.post("http://%s/"%(ip), data)
        cls.s = s

    # 被子类调用，登出
    @classmethod
    def tearDownClass(cls):
        cls.s.get("http://%s/logout.html"%(ip))
        # 第一次请求json，以得服务器设置的cookies
        cls.s.get("http://%s/"%(ip))
        cls.s.get("http://%s/data/login.json"%(ip))

    # 重启设备
    # 视机型和规则数量而定，最短60秒，EAP220超过90秒，需要额外加时间
    def reboot(self):
        res = self.s.get("http://%s/data/configReboot.json"%(ip), headers=header_eap220)
        self.assertEqual(res.json()["success"], True)
        self.assertEqual(res.json()["process"], "reboot")
        print "\n  system rebooting ..."
        time.sleep(120)
        print "  reboot success ..."
        # 重启后登录，返回session
        s = requests.session()
        res = s.get("http://%s/"%(ip))
        res = s.get("http://%s/data/login.json"%(ip))
        data = {"username":username, "password":passwordMD5 }
        res = s.post("http://%s/"%(ip), data)
        print "  login success ..."
        return s

    # 恢复出厂设置
    # 慎用，否则IP会变成动态，自动登录不成功
    def reset(self):
        res = self.s.get("http://%s/data/configReset.joson"%(ip), headers=header_eap220)
        self.assertEqual(res.json()["success"], True)
        self.assertEqual(res.json()["process"], "reset")
