#!/usr/bin/env python
# -*-coding:utf8-*-
#############################################################################################################
#
# File      ：   testLogin.py
# Author    ：   luliying
# Brief     ：   test login function
# 
# Version   ：   1.0.2
# Date      ：   4 Nov 2015
# 
# History   ：  
#                1.0.2  luliying   2015.11.04  add user account class
#                1.0.1  luliying   2015.10.28  modify post->login.json to get->login.json
#                1.0.0  chenqinbo  2015.08.21  create the file, add login class
#
#############################################################################################################


import requests
import hashlib
import unittest
import json
from utils import utils


# unittest按字母顺序依次执行测试用例
class login(utils.EAPLoginSession):

    # 初始化工作(每个用例)
    def setUp(self):
        self.s = requests.session()

    # 收尾工作(每个用例)
    def tearDown(self):
        self.s.get("http://%s/logout.html"%(utils.ip))
        res = self.s.post("http://%s/data/login.json"%(utils.ip))

    # case1: 获取被测机型
    def testLoginDutMode(self):
        res = self.s.get("http://%s/data/login.json"%(utils.ip))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["error"], 0)
        print "DutMode: " + res.json()["dutMode"]

    # case2: 正确用户名和密码登录
    def testLoginRight(self):
        res = self.s.get("http://%s/data/login.json"%(utils.ip))
        data = {"username":utils.username, "password":utils.passwordMD5 }
        res = self.s.post("http://%s/"%(utils.ip), data)
        res = self.s.get("http://%s/data/login.json"%(utils.ip))
        self.assertEqual(res.json()["error"], 0)

    # case3: 用户名错误
    def testLoginWrongName(self):
        res = self.s.get("http://%s/data/login.json"%(utils.ip))
        data = {"username":utils.username + "x", "password":utils.passwordMD5 }
        res = self.s.post("http://%s/"%(utils.ip), data)
        res = self.s.get("http://%s/data/login.json"%(utils.ip))
        self.assertEqual(res.json()["error"], 1)

    # case4: 密码错误
    def testLoginWrongPassword(self):
        res = self.s.get("http://%s/data/login.json"%(utils.ip))
        data = {"username":utils.username, "password":hashlib.md5((utils.password + "x").encode("utf8")).hexdigest().upper() }
        res = self.s.post("http://%s/"%(utils.ip), data)
        res = self.s.get("http://%s/data/login.json"%(utils.ip))
        self.assertEqual(res.json()["error"], 1)

    # case5: 用户名和密码错误
    def testLoginWrongNameAndPassword(self):
        res = self.s.get("http://%s/data/login.json"%(utils.ip))
        data = {"username":utils.username + "x", "password":hashlib.md5((utils.password + "x").encode("utf8")).hexdigest().upper() }
        res = self.s.post("http://%s/"%(utils.ip), data)
        res = self.s.get("http://%s/data/login.json"%(utils.ip))
        self.assertEqual(res.json()["error"], 1)


# 设置用户名和密码
class userAccount(utils.EAPLoginSession):

    # 登录
    @classmethod
    def setUpClass(cls):
        super(userAccount, cls).setUpClass()  # 单继承情况下，似乎不用管

    # 更改帐户密码
    def changeAccount(self, newUserName="new", newPassword="new"):
        newPasswordMD5 = hashlib.md5(newPassword.encode("utf8")).hexdigest().upper()
        data = {
                "operation": "write",
                "curUserName": "admin",
                "newUserName": newUserName,
                "curPassword": utils.passwordMD5,
                "newPwd": newPasswordMD5
                }
        res = self.s.post("http://%s/data/userAccount.json" %(utils.ip), data, headers=utils.header_eap220)
        self.assertEqual(res.json()["success"], True)
        self.assertEqual(res.json()["data"]["curUserName"], newUserName)

    # case6: 更改账户密码并重新登录
    def testChangeAccount(self):
        newPasswordMD5 = "22AF645D1859CB5CA6DA0C484F1F37EA"
        self.changeAccount()
        # 重新登录
        self.s = requests.session()
        res = self.s.get("http://%s/"%(utils.ip))
        res = self.s.get("http://%s/data/login.json"%(utils.ip))
        data = {"username": "new", "password": newPasswordMD5 }
        res = self.s.post("http://%s/"%(utils.ip), data)
        res = self.s.get("http://%s/data/login.json"%(utils.ip))
        self.assertEqual(res.json()["error"], 0)
        # 改回原来的账户密码
        data = {
                "operation": "write",
                "curUserName": "new",
                "newUserName": "admin",
                "curPassword": newPasswordMD5,
                "newPwd": utils.passwordMD5
                }
        res = self.s.post("http://%s/data/userAccount.json" %(utils.ip), data, headers=utils.header_eap220)
        self.assertEqual(res.json()["success"], True)


if __name__ == "__main__":
    unittest.main()
