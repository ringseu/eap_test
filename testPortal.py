#!/usr/bin/env python
# -*-coding:utf8-*-
#############################################################################################################
#
# File      ：   testPortal.py
# Author    ：   luliying
# Brief     ：   test portal setting
#
# Version   ：   1.1.0
# Date      ：   22 Oct 2015
# 
# History   ：   
#                1.1.0  luliying   2015.10.26  add reboot testcases, finish all function
#                1.0.1  luliying   2015.10.25  finish free rule test module
#                       luliying   2015.10.23  finish portal test module
#                       luliying   2015.10.22  finish portalAuthType
#                1.0.0  chenqinbo  2015.08.21  create the file
#
#############################################################################################################


longestTerm="1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890\
1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890\
1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890\
1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890\
1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890\
1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890\
1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890\
1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890\
1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890\
1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890\
12345678901234567890123"


from utils import utils
import json


# portal认证基本类
class portalBasic(utils.EAPLoginSession):

    # 登录
    @classmethod
    def setUpClass(cls):
        super(portalBasic, cls).setUpClass()  # 单继承情况下，似乎不用管

    # 检查响应是否正确
    def checkBasicResponse(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["success"], True)
        self.assertEqual(res.json()["errorcode"], 0)

    # 获取portal设置
    def getPortalBasicConfig(self):
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/portal_basic.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()


# 获取portal设置
class portalBasicConfig(portalBasic):

    # case1: 测试获取portal设置
    def testGetPortalBasicConfig(self):
        self.getPortalBasicConfig()


# 设置portal认证类型
class portalAuthType(portalBasic):

    # 设置无密码认证
    def portalSetNoPwd(self):
        jsondata = self.getPortalBasicConfig()
        data = {
                "operation": "write",
                "authType": "0",
                "authTimeout": "1",
                "redir": "false",
                "serverType": "0",
                "portal_title": "welcome",
                "portal_useTerm": "welcome",
                "portal_accept": "true"
                }
        res = self.s.post("http://%s/data/portal_basic.json" %(utils.ip), data, headers=utils.header_eap220)
        self.assertEqual(res.json()["success"], True)
        self.assertEqual(res.json()["errorcode"], 0)
        self.assertEqual(res.json()["data"]["authType"], 0)

    # case2: 无密码认证
    def testPortalNoPwd(self):
        self.portalSetNoPwd()

    # 设置本地密码认证(任意字符，最大长度31)
    def portalSetLocalPwd(self, password=""):
        jsondata = self.getPortalBasicConfig()
        data = {
                "operation": "write",
                "authType": "1",
                "username": "",
                "password": password,
                "authTimeout": "1",
                "redir": "false",
                "serverType": "0",
                "portal_title": "welcome",
                "portal_useTerm": "welcome",
                "portal_accept": "true"
                }
        res = self.s.post("http://%s/data/portal_basic.json" %(utils.ip), data, headers=utils.header_eap220)
        if ""==password:
            # 密码为空，返回空响应，不写入
            self.assertEqual(res.status_code, 200)
            if self.dutMode in {"EAP320", "EAP330"}:
                self.assertEqual(res.content, "")
            else:
                self.assertEqual(res.json()["success"], False)
        elif len(password)>32:
            # 密码超过32位，返回空响应，不写入
            self.assertEqual(res.status_code, 200)
            if self.dutMode in {"EAP320", "EAP330"}:
                self.assertEqual(res.content, "")
            else:
                self.assertEqual(res.json()["success"], False)
        elif 32==len(password):
            # 密码为32位，返回失败信息
            self.assertEqual(res.json()["success"], False)
        else:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["errorcode"], 0)
            self.assertEqual(res.json()["data"]["authType"], 1)
            self.assertEqual(res.json()["data"]["password"], password)

    # case3: 本地密码(1位)
    def testPortalLocalPwdShortest(self):
        self.portalSetLocalPwd("?")

    # case4: 本地密码(31位)
    def testPortalLocalPwdLongest(self):
        self.portalSetLocalPwd("1234567890123456789012345678901")

    # case5: 本地密码(32位)
    def testPortalLocalPwd32Charaters(self):
        self.portalSetLocalPwd("12345678901234567890123456789012")

    # case6: 本地密码(33位)
    def testPortalLocalPwdTooLong(self):
        self.portalSetLocalPwd("123456789012345678901234567890123")

    # case7: 本地密码(空)
    def testPortalLocalPwdEmpty(self):
        self.portalSetLocalPwd()

    # 设置radius密码认证
    def portalSetRadiusPwd(self, radiusServerIp="", radiusPort=80, radiusPwd="", ipLegal=True):
        jsondata = self.getPortalBasicConfig()
        data = {
                "operation": "write",
                "authType": "2",
                "radiusServerIp": radiusServerIp,
                "radiusPort": radiusPort,
                "radiusPwd": radiusPwd,
                "authTimeout": "1",
                "redir": "false",
                "serverType": "0",
                "portal_title": "welcome",
                "portal_useTerm": "welcome",
                "portal_accept": "true"
                }
        res = self.s.post("http://%s/data/portal_basic.json" %(utils.ip), data, headers=utils.header_eap220)
        if radiusPort<1 or radiusPort>65535:
            # 端口号错误，理应不能写入
            self.assertEqual(res.json()["success"], False)
        elif False==ipLegal:
            # IP地址错误，理应不能写入
            self.assertEqual(res.json()["success"], False)
        elif ""==radiusPwd:
            # 密码为空，返回空响应，不写入
            self.assertEqual(res.status_code, 200)
            if self.dutMode in {"EAP320", "EAP330"}:
                self.assertEqual(res.content, "")
            else:
                self.assertEqual(res.json()["success"], False)
        elif len(radiusPwd)>32:
            # 密码超过32位，返回空响应，不写入
            self.assertEqual(res.status_code, 200)
            if self.dutMode in {"EAP320", "EAP330"}:
                self.assertEqual(res.content, "")
            else:
                self.assertEqual(res.json()["success"], False)
        elif 32==len(radiusPwd):
            # 密码为32位，返回失败信息
            self.assertEqual(res.json()["success"], False)
        else:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["errorcode"], 0)
            self.assertEqual(res.json()["data"]["authType"], 2)
            self.assertEqual(res.json()["data"]["radiusServerIp"], radiusServerIp)
            self.assertEqual(res.json()["data"]["radiusPort"], radiusPort)
            self.assertEqual(res.json()["data"]["radiusPwd"], radiusPwd)

    # case8: radius密码(端口错误)
    # EAP120/220/320/330有问题，服务器不拒绝写入(无影响)
    def testPortalRadiusWrongPort(self):
        self.portalSetRadiusPwd("1.1.1.1", 65536, "~!@#$%^&*()_+")

    # case9: radius密码(IP地址错误)
    # EAP120/220/320/330有问题，服务器不拒绝写入(无影响)
    def testPortalRadiusWrongIP(self):
        self.portalSetRadiusPwd("127.1.1.1", 65535, "`-=[]{};\:|,./<>?", False)

    # case10: 本地密码(31位)
    def testPortalRadiusPwdLongest(self):
        self.portalSetRadiusPwd("192.168.1.1", 1, "1234567890123456789012345678901")

    # case11: 本地密码(32位)
    def testPortalRadiusPwd32Charaters(self):
        self.portalSetRadiusPwd("223.255.255.255", 65535, "12345678901234567890123456789012")

    # case12: 本地密码(33位)
    def testPortalRadiusPwdTooLong(self):
        self.portalSetRadiusPwd("223.255.255.255", 1, "123456789012345678901234567890123")

    # case13: 本地密码(空)
    def testPortalRadiusPwdEmpty(self):
        self.portalSetRadiusPwd("223.255.255.254", 1, "")

    # 设置错误的认证类型，服务器自动转换成无密码
    def portalSetWrongAuthType(self):
        jsondata = self.getPortalBasicConfig()
        data = {
                "operation": "write",
                "authType": "3",
                "authTimeout": "1",
                "redir": "false",
                "serverType": "0",
                "portal_title": "welcome",
                "portal_useTerm": "welcome",
                "portal_accept": "true"
                }
        res = self.s.post("http://%s/data/portal_basic.json" %(utils.ip), data, headers=utils.header_eap220)
        if self.dutMode in {"EAP320", "EAP330"}:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["errorcode"], 0)
            self.assertEqual(res.json()["data"]["authType"], 0)
        else:
            self.assertEqual(res.json()["success"], False)

    # case14: 错误的认证类型
    def testPortalWrongAuthType(self):
        self.portalSetWrongAuthType()


# 设置超时时间
class portalAuthTimeout(portalBasic):

    # 预设超时时间，超出范围会被修改为0
    def portalSetAuthTimeoutPreset(self, timeout=0):
        jsondata = self.getPortalBasicConfig()
        data = {
                "operation": "write",
                "authType": "1",
                "username": "",
                "password": "portalSetAuthTimeoutPreset",
                "authTimeout": timeout,
                "redir": "false",
                "serverType": "0",
                "portal_title": "welcome",
                "portal_useTerm": "welcome",
                "portal_accept": "true"
                }
        res = self.s.post("http://%s/data/portal_basic.json" %(utils.ip), data, headers=utils.header_eap220)
        if timeout<0 or timeout>=5:
            if self.dutMode in {"EAP320", "EAP330"}:
                self.assertEqual(res.json()["success"], True)
                self.assertEqual(res.json()["errorcode"], 0)
                self.assertEqual(res.json()["data"]["authTimeout"], 0)
            else:
                self.assertEqual(res.json()["success"], False)
        else:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["errorcode"], 0)
            self.assertEqual(res.json()["data"]["authTimeout"], timeout)

    # case15: 预设超时时间
    def testPortalAuthTimeoutPreset(self):
        self.portalSetAuthTimeoutPreset(0)
        self.portalSetAuthTimeoutPreset(1)
        self.portalSetAuthTimeoutPreset(2)
        self.portalSetAuthTimeoutPreset(3)

    # case16: 错误的预设超时时间
    def testPortalAuthTimeoutPresetWrong(self):
        self.portalSetAuthTimeoutPreset(5)

    # 自定义超时时间
    def portalSetAuthTimeoutCustom(self, portal_day=0, portal_hour=0, portal_min=0):
        jsondata = self.getPortalBasicConfig()
        data = {
                "operation": "write",
                "authType": "1",
                "username": "",
                "password": "portalSetAuthTimeoutCustom",
                "authTimeout": 4,
                "portal_day": portal_day,
                "portal_hour": portal_hour,
                "portal_min": portal_min,
                "redir": "false",
                "serverType": "0",
                "portal_title": "welcome",
                "portal_useTerm": "welcome",
                "portal_accept": "true"
                }
        res = self.s.post("http://%s/data/portal_basic.json" %(utils.ip), data, headers=utils.header_eap220)
        if 0==portal_day and 0==portal_hour and 0==portal_min:
            if self.dutMode in {"EAP320", "EAP330"}:
                self.assertEqual(res.json()["success"], False)
            else:
                self.assertEqual(res.json()["success"], True)
        elif portal_day<0 or portal_day>=30:
            self.assertEqual(res.json()["success"], False)
        elif portal_hour<0 or portal_hour>=24:
            self.assertEqual(res.json()["success"], False)
        elif portal_min<0 or portal_min>=60:
            self.assertEqual(res.json()["success"], False)
        else:
            if self.dutMode in {"EAP320", "EAP330"}:
                # EAP320/330这里返回的超时时间是两位字符串
                portal_day_str = "%d"%(portal_day)
                if 1==len(portal_day_str):
                    portal_day_str = "0" + portal_day_str
                portal_hour_str = "%d"%(portal_hour)
                if 1==len(portal_hour_str):
                    portal_hour_str = "0" + portal_hour_str
                portal_min_str = "%d"%(portal_min)
                if 1==len(portal_min_str):
                    portal_min_str = "0" + portal_min_str
                self.assertEqual(res.json()["success"], True)
                self.assertEqual(res.json()["errorcode"], 0)
                self.assertEqual(res.json()["data"]["portal_day"], portal_day_str)
                self.assertEqual(res.json()["data"]["portal_hour"], portal_hour_str)
                self.assertEqual(res.json()["data"]["portal_min"], portal_min_str)
            else:
                self.assertEqual(res.json()["data"]["portal_day"], portal_day)
                self.assertEqual(res.json()["data"]["portal_hour"], portal_hour)
                self.assertEqual(res.json()["data"]["portal_min"], portal_min)

    # case17: 正确的设置
    def testPortalAuthTimeoutCustom(self):
        self.portalSetAuthTimeoutCustom(0, 0, 1)
        self.portalSetAuthTimeoutCustom(10, 10, 10)
        self.portalSetAuthTimeoutCustom(29, 23, 59)

    # case18: 超时时间全0
    def testPortalAuthTimeoutCustomAllZero(self):
        self.portalSetAuthTimeoutCustom()

    # case19: 天数过大
    # EAP320/330有问题，服务器不拒绝写入(不影响上网)
    def testPortalAuthTimeoutCustomBigDay(self):
        self.portalSetAuthTimeoutCustom(30, 23, 59)

    # case20: 小时数过大
    # EAP320/330有问题，服务器不拒绝写入(不影响上网)
    def testPortalAuthTimeoutCustomBigHour(self):
        self.portalSetAuthTimeoutCustom(29, 24, 59)

    # case21: 分钟数过大
    # EAP320/330有问题，服务器不拒绝写入(不影响上网，按错误值给权限)
    def testPortalAuthTimeoutCustomBigMin(self):
        self.portalSetAuthTimeoutCustom(0, 0, 60)


# 设置重定向(必须是合法URL)
class portalRedirect(portalBasic):
    
    # 关闭重定向
    def portalCloseRedirect(self):
        jsondata = self.getPortalBasicConfig()
        data = {
                "operation": "write",
                "authType": "0",
                "authTimeout": "1",
                "redir": "false",
                "serverType": "0",
                "portal_title": "welcome",
                "portal_useTerm": "welcome",
                "portal_accept": "true"
                }
        res = self.s.post("http://%s/data/portal_basic.json" %(utils.ip), data, headers=utils.header_eap220)
        self.assertEqual(res.json()["success"], True)
        self.assertEqual(res.json()["data"]["redir"], False)

    # case22: 关闭重定向
    def testPortalCloseRedirect(self):
        self.portalCloseRedirect()

    # 设置重定向URL
    def portalSetRedirect(self, redirUrl, legal=True):
        jsondata = self.getPortalBasicConfig()
        data = {
                "operation": "write",
                "authType": "0",
                "authTimeout": "1",
                "redir": "true",
                "redirUrl": redirUrl,
                "serverType": "0",
                "portal_title": "welcome",
                "portal_useTerm": "welcome",
                "portal_accept": "true"
                }
        res = self.s.post("http://%s/data/portal_basic.json" %(utils.ip), data, headers=utils.header_eap220)
        if True==legal:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["data"]["redir"], True)
            self.assertEqual(res.json()["data"]["redirUrl"], redirUrl)
        else:
            self.assertEqual(res.json()["success"], False)

    # case23: 重定向URL合法
    def testPortalRedirectRight(self):
        self.portalSetRedirect("http://192.168.1.1")
        self.portalSetRedirect("https://hehe.net")
        self.portalSetRedirect("https://127.0.0.1")
        self.portalSetRedirect("http://hehe.net/haha/gua")

    # case24: 重定向URL非法
    # EAP120/220/320/330有问题，服务器不拒绝写入(无影响)
    def testPortalRedirectWrongUrl(self):
        self.portalSetRedirect("hehe", False)

    # case25: 重定向URL非法
    # EAP120/220/320/330有问题，服务器检查不出(无影响)(前端可以检查)
    def testPortalRedirectWrongIp(self):
        self.portalSetRedirect("htttp://300.1.1.1", False)

    # case26: 重定向URL非法
    # EAP120/220/320/330有问题，服务器检查不出(无影响)(前端也检查不出！)
    def testPortalRedirectWrongIpAllZero(self):
        self.portalSetRedirect("http://00.0.0.0", False)


# 设置portal使用条款(非空，标题限制31字符内，正文限制1023字符内)
class portalUseTerm(portalBasic):

    # 设置使用条款
    def portalSetUseTerm(self, portal_title="welcome", portal_useTerm="welcome", portal_accept="false"):
        jsondata = self.getPortalBasicConfig()
        data = {
                "operation": "write",
                "authType": "1",
                "username": "",
                "password": "portalSetUseTerm",
                "authTimeout": "1",
                "redir": "false",
                "serverType": "0",
                "portal_title": portal_title,
                "portal_useTerm": portal_useTerm,
                "portal_accept": portal_accept
                }
        res = self.s.post("http://%s/data/portal_basic.json" %(utils.ip), data, headers=utils.header_eap220)
        if len(portal_title)>=32:
            if self.dutMode in {"EAP320", "EAP330"}:
                # 标题过长，返回空响应，不写入
                self.assertEqual(res.content, "")
            else:
                self.assertEqual(res.json()["success"], False)
        elif 1024==len(portal_useTerm):
            # 内容为1024字节，返回失败信息
            self.assertEqual(res.json()["success"], False)
        elif len(portal_useTerm)>=1025:
            if self.dutMode in {"EAP320", "EAP330"}:
                # 内容过长，返回空响应，不写入
                self.assertEqual(res.content, "")
            else:
                self.assertEqual(res.json()["success"], False)
        else:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["errorcode"], 0)
            self.assertEqual(res.json()["data"]["portal_title"], portal_title)
            self.assertEqual(res.json()["data"]["portal_useTerm"], portal_useTerm)
            if "true"==portal_accept:
                self.assertEqual(res.json()["data"]["portal_accept"], True)
            else:
                self.assertEqual(res.json()["data"]["portal_accept"], False)

    # case27: 正确的使用条款
    def testPortalUseTerm(self):
        self.portalSetUseTerm()
        self.portalSetUseTerm(portal_accept="true")
        self.portalSetUseTerm("_the_length_of_this_title_is_31", longestTerm)

    # case28: 标题过长
    def testPortalUseTermLongTitle(self):
        self.portalSetUseTerm(portal_title="欢迎登陆这句话的长度为三十二字节")

    # case29: 内容1024字节
    def testPortalUseTermLongTerm1024(self):
        self.portalSetUseTerm(portal_useTerm=longestTerm+"1")

    # case30: 内容1025字节
    def testPortalUseTermLongTerm1025(self):
        self.portalSetUseTerm(portal_useTerm=longestTerm+"12")

    # case31: 测试重启后保存配置
    def testZPortalReboot(self):
        dataBeforeReboot = self.getPortalBasicConfig()["data"]
        self.s = self.reboot()
        dataAfterReboot = self.getPortalBasicConfig()["data"]
        if 0==dataBeforeReboot["authType"]:
            self.assertEqual(dataBeforeReboot["authType"], dataAfterReboot["authType"])
        elif 1==dataBeforeReboot["authType"]:
            self.assertEqual(dataBeforeReboot["password"], dataAfterReboot["password"])
            self.assertEqual(dataBeforeReboot["authTimeout"], dataAfterReboot["authTimeout"])
        elif 2==dataBeforeReboot["authType"]:
            self.assertEqual(dataBeforeReboot["radiusServerIp"], dataAfterReboot["radiusServerIp"])
            self.assertEqual(dataBeforeReboot["authTimeout"], dataAfterReboot["authTimeout"])
        if True==dataBeforeReboot["redir"]:
            self.assertEqual(dataBeforeReboot["redirUrl"], dataAfterReboot["redirUrl"])
        self.assertEqual(dataBeforeReboot["portal_title"], dataAfterReboot["portal_title"])


# 免认证基本类
class freeRuleBasic(utils.EAPLoginSession):

    # 登录
    @classmethod
    def setUpClass(cls):
        super(freeRuleBasic, cls).setUpClass()  # 单继承情况下，似乎不用管

    # 检查响应是否正确
    def checkBasicResponse(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["success"], True)
        self.assertEqual(res.json()["errorcode"], 0)

    # 读取全部规则
    def getFreeRules(self):
        data = {"operation":"load"}
        res = self.s.post("http://%s/data/portal_accessCtrl.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 按名称查找规则
    def getFreeRuleByName(self, policyName):
        rules = self.getFreeRules()["data"]
        for rule in rules:
            if rule["portal_policyName"]==policyName:
                return rule


# 免认证规则
class portalFreeRules(freeRuleBasic):

    # case32: 读取规则
    def testGetFreeRules(self):
        jsondata = self.getFreeRules()
        self.assertEqual(jsondata["success"], True)

    # 判断是否重名
    def isNameExist(self, policyName):
        rules = self.getFreeRules()
        for rule in rules["data"]:
            if policyName == rule["portal_policyName"]:
                return True
        return False

    # 添加规则(不可重名，policyName长度不大于31字符)
    def addFreeRule(self, policyName, sIp="192.168.1.1", sMask=32, dIp="192.168.1.1", dMask=32, sMac="", \
                port=80, status="false", sIpLegal=True, sMaskLegal=True, sMacLegal=True, portLegal=True):
        oldData = self.getFreeRules()["data"]
        if len(oldData)>=15:
            self.removeFreeRuleByIndex()
        jdata = {
                "portal_policyName": policyName,
                "portal_sIp": sIp,
                "portal_sMask": "%d"%sMask,
                "portal_dIp": dIp,
                "portal_dMask": "%d"%dMask,
                "portal_sMac": sMac,
                "portal_port": "%d"%port,
                "portal_status": status
                }
        data = {
                "operation": "insert",
                "key": "add",
                "index": "0",
                "old": "add",
                "new": json.dumps(jdata)
                }
        if True==self.isNameExist(policyName):
            # 已存在同名规则，拒绝添加
            # EAP220有问题，重名规则可以添加
            res = self.s.post("http://%s/data/portal_accessCtrl.json" %(utils.ip), data, headers=utils.header_eap220)
            self.assertEqual(res.json()["success"], False)
        else:
            res = self.s.post("http://%s/data/portal_accessCtrl.json" %(utils.ip), data, headers=utils.header_eap220)
            #print res.content
            if False==sIpLegal:
                # IP地址非法，转换为空地址(只做sIp即可，dIp与此类似)
                self.assertEqual(res.json()["success"], True)
                rule = self.getFreeRuleByName(policyName)
                self.assertEqual(rule["portal_sIp"], "")
            if False==sMaskLegal:
                # 掩码非法，只做sMask
                if self.dutMode in {"EAP320"}:
                    self.assertEqual(res.json()["success"], False)
                else:
                    self.assertEqual(res.json()["success"], True)
                    rule = self.getFreeRuleByName(policyName)
                    self.assertEqual(rule["portal_sMask"], "")
            if False==sMacLegal:
                # Mac地址非法，转换为空地址
                self.assertEqual(res.json()["success"], True)
                rule = self.getFreeRuleByName(policyName)
                self.assertEqual(rule["portal_sMac"], "")
            if False==portLegal:
                # 端口号非法，转换为空端口号
                self.assertEqual(res.json()["success"], True)
                rule = self.getFreeRuleByName(policyName)
                self.assertEqual(rule["portal_port"], "")
            if True==sIpLegal and True==sMaskLegal and True==sMacLegal and True==portLegal:
                # 全部合法，添加成功
                # 服务器会将IP地址改为与掩码计算后的网络号，暂时不依此判断
                self.assertEqual(res.json()["success"], True)
                rule = self.getFreeRuleByName(policyName)
                #self.assertEqual(rule["portal_sIp"], sIp)
                self.assertEqual(rule["portal_sMask"], sMask)
                #self.assertEqual(rule["portal_dIp"], dIp)
                self.assertEqual(rule["portal_dMask"], dMask)
                if self.dutMode in {"EAP320"}:
                    self.assertEqual(rule["portal_sMac"], sMac)
                else:
                    # EAP220会将Mac地址转为小写
                    self.assertEqual(rule["portal_sMac"], sMac.lower())
                self.assertEqual(rule["portal_port"], port)
                if "false"==status:
                    self.assertEqual(rule["portal_status"], False)
                else:
                    self.assertEqual(rule["portal_status"], True)

    # case33: 添加合法条目
    def testPortalAddFreeRule(self):
        self.addFreeRule(policyName="free_rule_1", status="true")
        self.addFreeRule("free_rule_2", "1.1.1.1", 32, "2.2.2.2", 1, "04-05-06-07-08-09", 65535)
        self.addFreeRule("free_rule_3", "223.255.255.255", 32, "1.0.0.0", 1, "04-05-06-07-08-09", 1)

    # case34: 判断是否重名
    def testNameExist(self):
        self.removeAllRules()
        self.addFreeRule(policyName="name_exist")
        self.isNameExist("name_exist")

    # case35: 添加重名条目
    # EAP120/220有问题，可以写入重明条目
    def testPortalAddFreeRuleNameExist(self):
        self.addFreeRule(policyName="name1")
        self.addFreeRule(policyName="name1")

    # case36: 添加非法条目(IP错误)
    # EAP120/220/320返回true，条目已添加，但错误的IP没有被写入
    def testPortalAddFreeRuleWrongIp(self):
        self.addFreeRule(policyName="wrongsIp", sIp="300.1.1.1", sIpLegal=False)

    # case37: 添加非法条目(掩码错误)
    # 返回true，条目已添加，但错误的IP没有被写入
    def testPortalAddFreeRuleWrongMask(self):
        self.addFreeRule(policyName="wrongsMask", sMask=33, sMaskLegal=False)

    # case38: 添加非法条目(Mac地址错误)
    # EAP120/220/320/330有问题，非法的Mac地址(多播地址)被写入(无影响)
    def testPortalAddFreeRuleWrongMac(self):
        self.addFreeRule(policyName="wrongsMac", sMac="11-22-22-22-22-22", sMacLegal=False)

    # case39: 添加非法条目(端口号错误)
    # EAP120/220/320/330有问题，非法的端口号被写入(无影响)
    def testPortalAddFreeRuleWrongPort(self):
        self.addFreeRule(policyName="wrongPort", port=65536, portLegal=False)

    # 修改规则(只测合法输入，非法的参考添加规则)
    def updateFreeRule(self, index, policyName, sIp="", sMask=32, dIp="", dMask=32, sMac="", port=80, status="false"):
        oldData = self.getFreeRules()["data"][index]
        jdata = {
                "portal_policyName": policyName,
                "portal_sIp": sIp,
                "portal_sMask": "%d"%sMask,
                "portal_dIp": dIp,
                "portal_dMask": "%d"%dMask,
                "portal_sMac": sMac,
                "portal_port": "%d"%port,
                "portal_status": status
                }
        data = {
                "operation": "update",
                "index": index,
                "key": oldData["key"],
                "old": oldData,
                "new": json.dumps(jdata)
                }
        res = self.s.post("http://%s/data/portal_accessCtrl.json" %(utils.ip), data, headers=utils.header_eap220)
        # 服务器会将IP地址改为与掩码计算后的网络号，不能用于判断
        self.assertEqual(res.json()["success"], True)
        self.assertEqual(res.json()["data"][index]["portal_policyName"], policyName)
        #self.assertEqual(res.json()["data"][index]["portal_sIp"], sIp)
        self.assertEqual(res.json()["data"][index]["portal_sMask"], sMask)
        #self.assertEqual(res.json()["data"][index]["portal_dIp"], dIp)
        self.assertEqual(res.json()["data"][index]["portal_dMask"], dMask)
        if self.dutMode in {"EAP320", "EAP330"}:
            self.assertEqual(res.json()["data"][index]["portal_sMac"], sMac)
        else:
            # EAP120/220会将Mac地址转为小写
            self.assertEqual(res.json()["data"][index]["portal_sMac"], sMac.lower())
        self.assertEqual(res.json()["data"][index]["portal_port"], port)
        if "false"==status:
            self.assertEqual(res.json()["data"][index]["portal_status"], False)
        else:
            self.assertEqual(res.json()["data"][index]["portal_status"], True)

    # case40: 修改规则
    def testUpdateFreeRule(self):
        self.updateFreeRule(0, "changed", "222.222.222.222", 24, "22.22.22.22", 24, "AA-AA-AA-AA-AA-AA", 999, "true")

    # 删除规则
    def removeFreeRuleByIndex(self, index=0):
        oldData = self.getFreeRules()["data"]
        # 只能删除存在的规则
        if index<len(oldData):
            target = oldData[index]
            data = {"operation": "remove", "key": target["key"], "index": index}
            res = self.s.post("http://%s/data/portal_accessCtrl.json" %(utils.ip), data, headers=utils.header_eap220)
            self.assertEqual(res.json()["success"], True)
            self.assertFalse(self.isNameExist(target["portal_policyName"]))
        elif self.dutMode in {"EAP320"}:
                data = {"operation": "remove", "key": -1, "index": index}
                res = self.s.post("http://%s/data/portal_accessCtrl.json" %(utils.ip), data, headers=utils.header_eap220)
                self.assertEqual(res.json()["success"], False)
        else:
            # EAP220不会响应
            pass

    # case41: 删除规则
    def testRemoveFreeRule(self):
        self.removeFreeRuleByIndex(3)

    # case42: 删除不存在的规则
    def testRemoveFreeRuleNotExist(self):
        self.removeFreeRuleByIndex(18)

    # 清空所有规则
    def removeAllRules(self):
        rules = self.getFreeRules()["data"]
        for rule in rules:
            data = {"operation": "remove", "key": rule["key"], "index": "0"}
            res = self.s.post("http://%s/data/portal_accessCtrl.json" %(utils.ip), data, headers=utils.header_eap220)
            self.checkBasicResponse(res)
        # 检查是否已清空
        data = {"operation":"load"}
        res = self.s.post("http://%s/data/portal_accessCtrl.json" %(utils.ip), data, headers=utils.header_eap220)
        self.assertEqual(len(res.json()["data"]), 0)

    # case43: 测试重启后保存配置
    def testZFreeRuleReboot(self):
        dataBeforeReboot = self.getFreeRules()
        self.s = self.reboot()
        dataAfterReboot = self.getFreeRules()
        self.assertEqual(len(dataBeforeReboot["data"]), len(dataAfterReboot["data"]))


if __name__ == "__main__":
    unittest.main()
