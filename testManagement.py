#!/usr/bin/env python
# -*-coding:utf8-*-
#############################################################################################################
#
# File      ：   testManagement.py
# Author    ：   luliying
# Brief     ：   test management functions
# 
# Version   ：   1.0.1
# Date      ：   4 Nov 2015
# 
# History   ：   
#                1.0.1  luliying  2015.11.04  finish
#                1.0.0  luliying  2015.11.04  create the file
#
#############################################################################################################


from utils import utils


# 系统管理
class managementBasic(utils.EAPLoginSession):

	# 登录
    @classmethod
    def setUpClass(cls):
        super(managementBasic, cls).setUpClass()  # 单继承情况下，似乎不用管

    # 检查响应是否正确
    def checkBasicResponse(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["success"], True)

    # 获取日志
    def getSystemLog(self):
    	data = {"operation": "load"}
        res = self.s.post("http://%s/data/syslogShow.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 设置发送日志邮件
    def setLogMail(self, data={}):
        res = self.s.post("http://%s/data/log.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)

    # 设置日志服务器和nvram
    def setLogServer(self, ip="", port=514, nvram="false"):
        data = {
                "operation": "write",
                "mailEnable": "true",
                "mailFrom": "everyday@mail.com",
                "mailTo": "everyday@mail.com",
                "smtpSvr": "12.12.12.12",
                "mailAuth": "true",
                "mailUsername": "everyday",
                "mailPassword": "everyday",
                "mailPassConf": "everyday",
                "mailTime": "1",
                "every_day_time": "11:11",
                "serverEnable": "true",
                "serverIp": ip,
                "serverPort": "%d"%port,
                "nvramEnable": nvram
                }
        res = self.s.post("http://%s/data/log.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)

    # 获取web server
    def getWebServer(self):
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/webserver.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        self.assertEqual(res.json()["errCode"], 0)
        return res.json()

    # 设置web server
    def setWebServer(self, secureConnEnable="true", secureServerPort=443, serverPort=80, sessionTimeout=15):
        data = {
                "operation": "write",
                "secureConnEnable": secureConnEnable,
                "secureServerPort": "%d"%secureServerPort,
                "serverPort": "%d"%serverPort,
                "sessionTimeout": "%d"%sessionTimeout
                }
        res = self.s.post("http://%s/data/webserver.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        self.assertEqual(res.json()["errCode"], 0)
        self.assertEqual(res.json()["data"]["sessionTimeout"], sessionTimeout)
        return res.json()

    # 获取本机Mac
    def getHostMac(self):
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/mac.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        self.assertEqual(res.json()["error"], 0)
        return res.json()["data"]["hostMac"]

    # 设置管理权限
    def setManagementAccess(self, macAuthEnable="false", mac2="", mac3="", mac4=""):
        hostMac = self.getHostMac()
        data = {
                "operation": "write",
                "macAuthEnable": macAuthEnable,
                "hostMac": hostMac
                }
        if "true"==macAuthEnable:
                data["mac1"] = hostMac
                data["mac2"] = mac2
                data["mac3"] = mac3
                data["mac4"] = mac4
        res = self.s.post("http://%s/data/mac.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        self.assertEqual(res.json()["error"], 0)
        if "true"==macAuthEnable:
            self.assertEqual(res.json()["data"]["mac1"], hostMac)
            self.assertEqual(res.json()["data"]["mac2"], mac2)

    # 开启或关闭LED
    def ledCtrl(self, enable="on"):
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/ledctrl.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        data = {"operation": "write", "enable": enable}
        res = self.s.post("http://%s/data/ledctrl.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        self.assertEqual(res.json()["error"], 0)
        self.assertEqual(res.json()["data"]["enable"], enable)

    # 设置SSH服务器
    def setSSHServer(self, port=22, sshServerEnable="false"):
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/sshServer.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        data = {
                "operation": "write",
                "remoteEnable": "0",
                "serverPort": "%d"%port,
                "sshServerEnable": sshServerEnable
                }
        res = self.s.post("http://%s/data/sshServer.json" %(utils.ip), data, headers=utils.header_eap220)
        if 22==port or (port>=1025 and port<=65535):
            self.checkBasicResponse(res)
            self.assertEqual(res.json()["errCode"], 0)
            self.assertEqual(res.json()["data"]["serverPort"], port)
        else:
            data = {"operation": "read"}
            res = self.s.post("http://%s/data/sshServer.json" %(utils.ip), data, headers=utils.header_eap220)
            self.assertNotEqual(res.json()["data"]["serverPort"], port)

    # 设置SNMP代理
    def setSNMPAgent(self, snmpEnable="false", sysContact="contact", sysName="Agent", sysLocation="Shenzhen", \
                getCommunity="public", getSource="192.168.1.1", setCommunity="private", setSource="192.168.1.1"):
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/snmp.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        data = {
                "operation": "write",
                "snmpEnable": snmpEnable,
                "sysContact": sysContact,
                "sysName": sysName,
                "sysLocation": sysLocation,
                "getCommunity": getCommunity,
                "getSource": getSource,
                "setCommunity": setCommunity,
                "setSource": setSource,
                "remoteEnable": "false"
                }
        res = self.s.post("http://%s/data/snmp.json" %(utils.ip), data, headers=utils.header_eap220)
        if "true"==snmpEnable:
            self.checkBasicResponse(res)
            self.assertEqual(res.json()["errCode"], 0)
            self.assertEqual(res.json()["data"]["sysName"], sysName)
            self.assertEqual(res.json()["data"]["getSource"], getSource)
            self.assertEqual(res.json()["data"]["setCommunity"], setCommunity)
        else:
            self.checkBasicResponse(res)
            self.assertEqual(res.json()["errCode"], 0)
            self.assertEqual(res.json()["data"]["snmpEnable"], False)


# 系统管理测试
class management(managementBasic):

    # case1: 获取日志
    def testGetSystemLog(self):
        self.getSystemLog()

    # case2: 设置发送日志邮件
    def testSetLogMail(self):
        data_everyday = {
                        "operation": "write",
                        "mailEnable": "true",
                        "mailFrom": "everyday@mail.com",
                        "mailTo": "everyday@mail.com",
                        "smtpSvr": "12.12.12.12",
                        "mailAuth": "true",
                        "mailUsername": "everyday",
                        "mailPassword": "everyday",
                        "mailPassConf": "everyday",
                        "mailTime": "1",
                        "every_day_time": "11:11",
                        "serverEnable": "false",
                        "nvramEnable": "false"
                        }
        data_hourhour = {
                        "operation": "write",
                        "mailEnable": "true",
                        "mailFrom": "hourhour@mail.com",
                        "mailTo": "hourhour@mail.com",
                        "smtpSvr": "12.12.12.12",
                        "mailAuth": "true",
                        "mailUsername": "hourhour",
                        "mailPassword": "hourhour",
                        "mailPassConf": "hourhour",
                        "mailTime": "2",
                        "mailHourHour": "12",
                        "serverEnable": "false",
                        "nvramEnable": "false"
                        }
        self.setLogMail(data_everyday)
        self.setLogMail(data_hourhour)

    # case3: 设置日志服务器和nvram
    def testSetLogServer(self):
        self.setLogServer("12.12.12.12", 1, "false")
        self.setLogServer("223.12.12.12", 65535, "true")

    # case4: 设置并获取web server
    def testSetWebServer(self):
        self.setWebServer(sessionTimeout=66)
        newData = self.getWebServer()
        self.assertEqual(newData["data"]["sessionTimeout"], 66)

    # case5: 设置管理权限
    def testSetManagementAccess(self):
        self.setManagementAccess()
        self.setManagementAccess("true", "10-10-10-10-10-10", "", "AA-AA-AA-AA-AA-AA")

    # case6: 设置LED状态
    def testLedCtrl(self):
        self.ledCtrl("off")
        self.ledCtrl()

    # case7: 设置SSH服务器
    def testSetSSHServer(self):
        self.setSSHServer()
        self.setSSHServer(1025, "true")
        self.setSSHServer(65535, "false")

    # case8: 设置SSH服务器(端口号错误)
    # EAP120/220有问题，可以写入
    def testSetSSHServerWrong(self):
        self.setSSHServer(1024, "false")

    # case9: 设置SNMP代理
    def testSetSNMPAgent(self):
        self.setSNMPAgent(snmpEnable="true", sysLocation="enableSNMPAgent")
        self.setSNMPAgent(snmpEnable="false", sysLocation="unableSNMPAgent")


if __name__ == "__main__":
    unittest.main()
