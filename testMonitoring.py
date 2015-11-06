#!/usr/bin/env python
# -*-coding:utf8-*-
#############################################################################################################
#
# File      ：   testMonitoring.py
# Author    ：   luliying
# Brief     ：   test monitor functions
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


# 状态监控
class monitorBasic(utils.EAPLoginSession):

	# 登录
    @classmethod
    def setUpClass(cls):
        super(monitorBasic, cls).setUpClass()  # 单继承情况下，似乎不用管

    # 检查响应是否正确
    def checkBasicResponse(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["success"], True)

    # 获取AP列表
    def getAplist(self):
        data = {"operation": "load"}
        res = self.s.get("http://%s/data/monitor.ap.aplist.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        if self.dutMode in {"EAP120", "EAP220"}:
        	self.assertEqual(res.json()["error"], 0)
        return res.json()

    # 获取AP设备状态
    def getApDevinfo(self, apMac=""):
        data = {"operation": "read", "apMac": apMac}
        res = self.s.get("http://%s/data/monitor.ap.devinfo.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        if self.dutMode in {"EAP120", "EAP220"}:
        	self.assertEqual(res.json()["error"], 0)
        return res.json()

    # 获取AP无线设置
    def getApWirelessSetting(self, apMac="", radioId=0):
        data = {"operation": "read", "apMac": apMac, "radioId": radioId}
        res = self.s.get("http://%s/data/monitor.ap.wsetting.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        if self.dutMode in {"EAP120", "EAP220"}:
        	self.assertEqual(res.json()["error"], 0)
        return res.json()

    # 获取AP LAN状态
    def getApLANinfo(self, apMac=""):
        data = {"operation": "read", "apMac": apMac}
        res = self.s.get("http://%s/data/monitor.ap.laninfo.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        if self.dutMode in {"EAP120", "EAP220"}:
        	self.assertEqual(res.json()["error"], 0)
        return res.json()

    # 获取AP用户状态
    def getApClient(self, apMac=""):
        data = {"operation": "load", "apMac": apMac}
        res = self.s.get("http://%s/data/monitor.ap.client.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        if self.dutMode in {"EAP120", "EAP220"}:
        	self.assertEqual(res.json()["error"], 0)
        return res.json()

    # 获取AP网路状态(interface: AP/WIFI0/WIFI1)
    def getApTraffic(self, interface="LAN", apMac=""):
        data = {"operation": "read", "interface": interface, "apMac": apMac}
        res = self.s.get("http://%s/data/monitor.ap.interface.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        if self.dutMode in {"EAP120", "EAP220"}:
        	self.assertEqual(res.json()["error"], 0)
        return res.json()

    # 获取SSID列表
    def getSSIDlist(self):
        data = {"operation": "load"}
        res = self.s.post("http://%s/data/monitor.ssid.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取用户列表
    def getClientlist(self):
        data = {"operation": "load"}
        res = self.s.get("http://%s/data/monitor.client.client.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        if self.dutMode in {"EAP120", "EAP220"}:
        	self.assertEqual(res.json()["error"], 0)
        return res.json()

    # 获取portal用户列表
    def getPortaluserList(self):
        data = {"operation": "load"}
        res = self.s.get("http://%s/data/monitor.client.portaluser.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        if self.dutMode in {"EAP120", "EAP220"}:
        	self.assertEqual(res.json()["error"], 0)
        return res.json()


# 状态监控测试
class monitor(monitorBasic):

	# case1: 获取AP列表
	def testGetApList(self):
		self.getAplist()

	# case2: 获取AP设备状态
	def testGetApDevinfo(self):
		apMac = self.getAplist()["data"][0]["MAC"]
		self.getApDevinfo(apMac)

	# case3: 获取AP无线设置
	def testGetApWirelessSetting(self):
		apMac = self.getAplist()["data"][0]["MAC"]
		self.getApWirelessSetting(apMac, 0)
		if self.dutMode not in {"EAP120"}:
			self.getApWirelessSetting(apMac, 1)

	# case4: 获取AP LAN状态
	def testGetApLANinfo(self):
		apMac = self.getAplist()["data"][0]["MAC"]
		self.getApLANinfo(apMac)

	# case5: 获取AP用户状态
	def testGetApClient(self):
		apMac = self.getAplist()["data"][0]["MAC"]
		self.getApClient(apMac)

	# case6: 获取AP网路状态
	def testGetApTraffic(self):
		apMac = self.getAplist()["data"][0]["MAC"]
		self.getApTraffic("LAN", apMac)
		self.getApTraffic("WIFI0", apMac)
		if self.dutMode not in {"EAP120"}:
			self.getApTraffic("WIFI1", apMac)

	# case7: 获取SSID列表
	def testGetSSIDlist(self):
		self.getSSIDlist()

	# case8: 获取用户列表
	def testGetClientlist(self):
		self.getClientlist()

	# case9: 获取portal用户列表
	def testGetPortaluserList(self):
		self.getPortaluserList()


if __name__ == "__main__":
    unittest.main()
