#!/usr/bin/env python
# -*-coding:utf8-*-
#############################################################################################################
#
# File      ：   testWireless.py
# Author    ：   luliying
# Brief     ：   test wireless setting
# 
# Version   ：   1.1.0
# Date      ：   28 Oct 2015
# 
# History   ：   
#                1.1.0  luliying  2015.10.28  finish 5G wireless testcases
#                1.0.1  luliying  2015.10.27  finish 2.4G wireless testcases
#                1.0.0  luliying  2015.10.26  create the file
#
#############################################################################################################


longestpwd = "1234567890123456789012345678901234567890123456789012345678901234"


from utils import utils
import json


class wirelessBasic(utils.EAPLoginSession):

	# 登录
    @classmethod
    def setUpClass(cls):
        super(wirelessBasic, cls).setUpClass()  # 单继承情况下，似乎不用管

    # 检查响应是否正确
    def checkBasicResponse(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["success"], True)

    # 获取2.4G基本设置
    def getWireless2GBasic(self):
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/wireless.basic.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取2.4G SSID设置
    def getWireless2GSSID(self):
        data = {"operation": "load"}
        res = self.s.post("http://%s/data/wireless.ssids.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取2.4G扩展设置
    def getWireless2GAdv(self):
    	data = {"operation": "read"}
        res = self.s.post("http://%s/data/wireless.adv.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取2.4G负载平衡设置
    def getWireless2GLb(self):
        data = {"operation": "read"}
        if self.dutMode in {"EAP320", "EAP330"}:
            res = self.s.post("http://%s/data/wireless.lb.json" %(utils.ip), data, headers=utils.header_eap220)
        else:
            res = self.s.post("http://%s/data/clusterLoadBalance.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取5G基本设置
    def getWireless5GBasic(self):
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/wireless.basic.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取5G SSID设置
    def getWireless5GSSID(self):
        data = {"operation": "load"}
        res = self.s.post("http://%s/data/wireless.ssids.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取5G扩展设置
    def getWireless5GAdv(self):
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/wireless.adv.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取5G负载平衡设置
    def getWireless5GLb(self):
        data = {"operation": "read"}
        if self.dutMode in {"EAP320", "EAP330"}:
            res = self.s.post("http://%s/data/wireless.lb.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
        else:
            res = self.s.post("http://%s/data/clusterLoadBalance.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()


# 测试获取无线设置
class getWirelessBasic(wirelessBasic):

    # case1: 获取无线设置
    def testGetWirelessBasic(self):
        self.getWireless2GBasic()
        self.getWireless2GSSID()
        self.getWireless2GAdv()
        self.getWireless2GLb()
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.getWireless5GBasic()
            self.getWireless5GSSID()
            self.getWireless5GAdv()
            self.getWireless5GLb()


# 2.4G无线基本设置
class wireless2GBasic(wirelessBasic):

    # 基本设置
    # wirelessmode: 4: 11b/g/n;   3: 11b/g;     2: 11n;
    # chwidth:      4: 20/40MHz;  3: 40MHz;     2: 20MHz;
    # channel:      0: Auto;      1~11: 各个信道
    # txpower:      1~26: 发射功率
    # isapmode:     未知
    def set2GBasic(self, status="on", wirelessmode=4, chwidth=4, channel=0, txpower=20, legal=True):
        data = {
                "operation": "write",
                "wireless-bset-status": status,
                "wireless_mode_2g": "%d"%wirelessmode,
                "chan_width_2g": "%d"%chwidth,
                "channel_2g": "%d"%channel,
                "txpower_2g": "%d"%txpower,
                "is_apmode": "1"
               }
        res = self.s.post("http://%s/data/wireless.basic.json" %(utils.ip), data, headers=utils.header_eap220)
        if True==legal:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["data"]["status"], status)
            self.assertEqual(res.json()["data"]["wirelessmode"], wirelessmode)
            self.assertEqual(res.json()["data"]["chwidth"], chwidth)
            # 信道过大会变为自动
            if channel>=0 and channel<=11:
                self.assertEqual(res.json()["data"]["channel"], channel)
            else:
                self.assertEqual(res.json()["data"]["channel"], 0)
            self.assertEqual(res.json()["data"]["txpower"], txpower)
        else:
            self.assertEqual(res.json()["success"], False)

    # case2: 2.4G基本设置
    def testSet2GBasic(self):
        self.set2GBasic()
        self.set2GBasic("off", 4, 2, 11, 1)

    # case3: 2.4G基本设置(模式错误)
    # EAP120/220有小问题
    def testSet2GBasicWrongMode(self):
        self.set2GBasic(wirelessmode=5, legal=False)

    # case4: 2.4G基本设置(信道错误)
    def testSet2GBasicWrongChannel(self):
        self.set2GBasic(channel=100)

    # case5: 2.4G基本设置(带宽错误)
    # EAP120/220返回true，但带宽被后台改正确了
    def testSet2GBasicWrongWidth(self):
        self.set2GBasic(chwidth=5, legal=False)

    # case6: 2.4G基本设置(功率过大)
    # EAP120/220/320/330有小问题，可以写入(不影响上网)
    def testSet2GBasicWrongPower(self):
        self.set2GBasic(txpower=30, legal=False)

    # case7: 重启后是否保留
    def testZ2GBasicReboot(self):
        dataBeforeReboot = self.getWireless2GBasic()["data"]
        self.s = self.reboot()
        dataAfterReboot = self.getWireless2GBasic()["data"]
        self.assertEqual(dataBeforeReboot, dataAfterReboot)


class wireless2GSSID(wirelessBasic):

    # 判断是否重名
    def isNameExist(self, ssidName):
        SSIDS = self.getWireless2GSSID()["data"]
        for ssid in SSIDS:
            if ssid["ssidname"]==ssidName:
                return True
        return False

    # 判断WEP加密SSID是否存在
    def isWEPExist(self):
        SSIDS = self.getWireless2GSSID()["data"]
        for ssid in SSIDS:
            if 1==ssid["securityMode"]:
                return True
        return False

    # 按名称查找SSID
    def getSSIDByName(self, ssidName=""):
        SSIDS = self.getWireless2GSSID()["data"]
        for ssid in SSIDS:
            if ssid["ssidname"]==ssidName:
                return ssid

    # 2.4G添加无加密SSID
    # vlanid:   1~4094
    # ssidbcast、portal、isolation:  0或1
    def add2GSSIDNoPwd(self, ssidName="TP-LINK_2.4G", vlanid=1, ssidbcast=1, portal=0, isolation=0):
        oldData = self.getWireless2GSSID()
        if len(oldData["data"])>=7:
            # SSID过多就删掉前面的
            self.remove2GSSID()
        jdata = {
                "ssidname": ssidName,
                "vlanid": "%d"%vlanid,
                "ssidbcast": "%d"%ssidbcast,
                "securityMode": "0",
                "portal": "%d"%portal,
                "isolation": "%d"%isolation
                }
        data = {
                "operation": "insert",
                "key": "add",
                "index": "0",
                "old": "add",
                "new": json.dumps(jdata)
                }
        if self.isNameExist(ssidName):
            res = self.s.post("http://%s/data/wireless.ssids.json" %(utils.ip), data, headers=utils.header_eap220)
            self.assertEqual(res.json()["success"], False)
        else:
            res = self.s.post("http://%s/data/wireless.ssids.json" %(utils.ip), data, headers=utils.header_eap220)
            if vlanid>=1 and vlanid<=4094:
                newSSID = self.getSSIDByName(ssidName)
                self.assertEqual(newSSID["vlanid"], vlanid)
                self.assertEqual(newSSID["ssidbcast"], ssidbcast)
                self.assertEqual(newSSID["securityMode"], 0)
                self.assertEqual(newSSID["portal"], portal)
                self.assertEqual(newSSID["isolation"], isolation)
            else:
                self.assertEqual(res.json()["success"], False)

    # case8: 添加无加密SSID
    def testAdd2GSSIDNoPwd(self):
        self.add2GSSIDNoPwd()
        self.add2GSSIDNoPwd("no_pwd_min", 1, 0, 0, 0)
        self.add2GSSIDNoPwd("no_pwd_max", 4094, 1, 1, 1)

    # case9: 添加无加密SSID(重名)
    def testAdd2GSSIDNoPwdNameExist(self):
        self.add2GSSIDNoPwd("name1")
        self.add2GSSIDNoPwd("name1")

    # case10: 添加无加密SSID(vlanid错误)
    def testAdd2GSSIDNoPwdWrongVlanid(self):
        self.add2GSSIDNoPwd(ssidName="wrong_vlanid", vlanid=4095)

    # 2.4GG添加WEP加密SSID(只能设置一个)
    # wep_mode:     1: Open_System;    2: Shared_Key;    3: Auto
    # wep_select:   1~4: Key1~Key4
    # wep_format:   1: 数字;      2: ASCII字符
    # wep_type:     5: 64位;      13: 128位
    # wep_key:      format=1、type=5:    10位
    #               format=1、type=13:   26位
    #               format=2、type=5:    5位
    #               format=2、type=13:   13位
    def add2GSSIDWep(self, ssidName="TP-LINK_2.4G", vlanid=1, ssidbcast=1, wep_mode=3, wep_select=1, \
            wep_format=2, wep_type=5, wep_key="weppw", portal=0, isolation=0):
        oldData = self.getWireless2GSSID()
        if len(oldData["data"])>=7:
            # SSID过多就删掉前面的
            self.remove2GSSID()
        json_wep_format = "wep_format"+"%d"%wep_select
        json_wep_type = "wep_type"+"%d"%wep_select
        json_wep_key = "wep_key"+"%d"%wep_select
        jdata = {
                "ssidname": ssidName,
                "vlanid": "%d"%vlanid,
                "ssidbcast": "%d"%ssidbcast,
                "securityMode": "1",
                "wep_mode": "%d"%wep_mode,
                "wep_select": "%d"%wep_select,
                json_wep_format: "%d"%wep_format,
                json_wep_type: "%d"%wep_type,
                json_wep_key: wep_key,
                "portal": "%d"%portal,
                "isolation": "%d"%isolation
                }
        data = {
                "operation": "insert",
                "key": "add",
                "index": "0",
                "old": "add",
                "new": json.dumps(jdata)
                }
        if self.isWEPExist() or self.isNameExist(ssidName):
            # 存在WEP加密SSID或存在同名SSID，返回false
            res = self.s.post("http://%s/data/wireless.ssids.json" %(utils.ip), data, headers=utils.header_eap220)
            self.assertEqual(res.json()["success"], False)
        else:
            res = self.s.post("http://%s/data/wireless.ssids.json" %(utils.ip), data, headers=utils.header_eap220)
            if (1==wep_format and 5==wep_type and 10!=len(wep_key)) or (1==wep_format and 13==wep_type and 26!=len(wep_key)) \
                or (2==wep_format and 5==wep_type and 5!=len(wep_key)) or (2==wep_format and 13==wep_type and 13!=len(wep_key)):
                # 密钥位数不对，返回错误信息
                self.assertEqual(res.json()["success"], False)
            else:
                self.assertEqual(res.json()["success"], True)
                newSSID = self.getSSIDByName(ssidName)
                self.assertEqual(newSSID["vlanid"], vlanid)
                self.assertEqual(newSSID["ssidbcast"], ssidbcast)
                self.assertEqual(newSSID["securityMode"], 1)
                self.assertEqual(newSSID["wep_mode"], wep_mode)
                self.assertEqual(newSSID["wep_select"], wep_select)
                self.assertEqual(newSSID[json_wep_format], wep_format)
                self.assertEqual(newSSID[json_wep_type], wep_type)
                self.assertEqual(newSSID[json_wep_key], wep_key)
                self.assertEqual(newSSID["portal"], portal)
                self.assertEqual(newSSID["isolation"], isolation)                

    # case11: 添加WEP加密SSID
    def testAdd2GSSIDWep(self):
        self.add2GSSIDWep(ssidName="2G_WEP", wep_select=4)

    # case12: 添加WEP加密SSID(密钥位数不对)
    def testAdd2GSSIDWepWrongKey(self):
        self.add2GSSIDWep(ssidName="2G_WEP_WRONG_KEY", wep_key="hehe")

    # 2.4G添加WPA-ENTERPRISE加密SSID
    # wpa_version:      1: WPA-PSK;     2: WPA2-PSK;    3: Auto
    # wpa_chpher:       1: Auto;        2: TKIP;        3: AES
    # wpa_key_update_2g:    30~8640000: 密钥更新周期;   0: 不更新
    def add2GSSIDEnterprise(self, ssidName="TP-LINK_2.4G", vlanid=1, ssidbcast=1, wpa_version=3, wpa_cipher=1, \
                    server="192.168.1.1", port=0, wpa_key="11111111", wpa_key_update_2g=0, portal=0, isolation=0):
        oldData = self.getWireless2GSSID()
        if len(oldData["data"])>=7:
            # SSID过多就删掉前面的
            self.remove2GSSID()
        jdata = {
                "ssidname": ssidName,
                "vlanid": "%d"%vlanid,
                "ssidbcast": "%d"%ssidbcast,
                "securityMode": "2",
                "wpa_version": "%d"%wpa_version,
                "wpa_cipher": "%d"%wpa_cipher,
                "server": server,
                "port": "%d"%port,
                "wpa_key": wpa_key,
                "wpa_key_update_2g": "%d"%wpa_key_update_2g,
                "portal": "%d"%portal,
                "isolation": "%d"%isolation
                }
        data = {
                "operation": "insert",
                "key": "add",
                "index": "0",
                "old": "add",
                "new": json.dumps(jdata)
                }
        if self.isNameExist(ssidName):
            res = self.s.post("http://%s/data/wireless.ssids.json" %(utils.ip), data, headers=utils.header_eap220)
            if len(wpa_key)>=65:
                # 密钥超长，不返回信息
                self.assertEqual(res.content, "")
            else:
                self.assertEqual(res.json()["success"], False)
        else:
            res = self.s.post("http://%s/data/wireless.ssids.json" %(utils.ip), data, headers=utils.header_eap220)
            if vlanid>=1 and vlanid<=4094 and len(wpa_key)>=8 and len(wpa_key)<=64:
                newSSID = self.getSSIDByName(ssidName)
                self.assertEqual(newSSID["vlanid"], vlanid)
                self.assertEqual(newSSID["ssidbcast"], ssidbcast)
                self.assertEqual(newSSID["securityMode"], 2)
                self.assertEqual(newSSID["wpa_version"], wpa_version)
                self.assertEqual(newSSID["wpa_cipher"], wpa_cipher)
                self.assertEqual(newSSID["server"], server)
                self.assertEqual(newSSID["port"], port)
                self.assertEqual(newSSID["wpa_key"], wpa_key)
                self.assertEqual(newSSID["wpa_key_update_2g"], wpa_key_update_2g)
                self.assertEqual(newSSID["portal"], portal)
                self.assertEqual(newSSID["isolation"], isolation)
            elif len(wpa_key)<=7:
                # 密钥太短，EAP320返回false
                self.assertEqual(res.json()["success"], False)
            elif len(wpa_key)>=65:
                if self.dutMode in {"EAP320", "EAP330"}:
                    # 密钥超长，EAP320不返回信息
                    self.assertEqual(res.content, "")
                else:
                    self.assertEqual(res.json()["success"], False)
            else:
                self.assertEqual(res.json()["success"], False)

    # case13: 添加Enterprise加密SSID
    def testAdd2GSSIDEnterprise(self):
        self.remove2GAllSSIDS()
        self.add2GSSIDEnterprise("2G_ENTERPRISE_SHORTEST", 1, 0, 1, 1, "1.0.0.1", 0, "12345678", 0, 0, 0)
        self.add2GSSIDEnterprise("2G_ENTERPRISE_LONGEST", 4094, 1, 3, 3, "223.255.255.254", 65535, longestpwd, 8640000, 1, 1)

    # case14: 添加Enterprise加密SSID(密钥太短)
    # EAP120/220有问题，可以写入
    def testAdd2GSSIDEnterprisePwdTooShort(self):
        self.add2GSSIDEnterprise(ssidName="2G_ENTERPRISE_PWD_TOO_SHORT", wpa_key="1234567")

    # case15: 添加Enterprise加密SSID(密钥太长)
    # EAP120/220有问题，可以写入
    def testAdd2GSSIDEnterprisePwdTooLong(self):
        self.add2GSSIDEnterprise(ssidName="2G_ENTERPRISE_PWD_TOO_LONG", wpa_key=longestpwd+"a")

    # case16: 添加Enterprise加密SSID(重名)
    def testAdd2GSSIDEnterpriseExist(self):
        self.add2GSSIDEnterprise(ssidName="ENTERPRISE_EXIST")
        self.add2GSSIDEnterprise(ssidName="ENTERPRISE_EXIST")

    # 2.4G添加WPA-PSK加密SSID
    # psk_version:      1: WPA-PSK;     2: WPA2-PSK;    3: Auto
    # psk_cipher:       1: Auto;        2: TKIP;        3: AES
    def add2GSSIDPsk(self, ssidName="TP-LINK_2.4G", vlanid=1, ssidbcast=1, psk_version=3, \
                psk_cipher=1, psk_key="11111111", psk_key_update_2g=0, portal=0, isolation=0):
        oldData = self.getWireless2GSSID()
        if len(oldData["data"])>=7:
            # SSID过多就删掉前面的
            self.remove2GSSID()
        jdata = {
                "ssidname": ssidName,
                "vlanid": "%d"%vlanid,
                "ssidbcast": "%d"%ssidbcast,
                "securityMode": "3",
                "psk_version": "%d"%psk_version,
                "psk_cipher": "%d"%psk_cipher,
                "psk_key": psk_key,
                "psk_key_update_2g": "%d"%psk_key_update_2g,
                "portal": "%d"%portal,
                "isolation": "%d"%isolation
                }
        data = {
                "operation": "insert",
                "key": "add",
                "index": "0",
                "old": "add",
                "new": json.dumps(jdata)
                }
        if self.isNameExist(ssidName):
            res = self.s.post("http://%s/data/wireless.ssids.json" %(utils.ip), data, headers=utils.header_eap220)
            if len(psk_key)>=65:
                # 密钥超长，不返回信息
                self.assertEqual(res.content, "")
            else:
                self.assertEqual(res.json()["success"], False)
        else:
            res = self.s.post("http://%s/data/wireless.ssids.json" %(utils.ip), data, headers=utils.header_eap220)
            if vlanid>=1 and vlanid<=4094 and len(psk_key)>=8 and len(psk_key)<=64:
                newSSID = self.getSSIDByName(ssidName)
                self.assertEqual(newSSID["vlanid"], vlanid)
                self.assertEqual(newSSID["ssidbcast"], ssidbcast)
                self.assertEqual(newSSID["securityMode"], 3)
                self.assertEqual(newSSID["psk_version"], psk_version)
                self.assertEqual(newSSID["psk_cipher"], psk_cipher)
                self.assertEqual(newSSID["psk_key"], psk_key)
                self.assertEqual(newSSID["psk_key_update_2g"], psk_key_update_2g)
                self.assertEqual(newSSID["portal"], portal)
                self.assertEqual(newSSID["isolation"], isolation)
            elif len(psk_key)<=7:
                # 密钥太短，返回false
                self.assertEqual(res.json()["success"], False)
            elif len(psk_key)>=65:
                if self.dutMode in {"EAP320", "EAP330"}:
                    # 密钥超长，EAP320不返回信息
                    self.assertEqual(res.content, "")
                else:
                    self.assertEqual(res.json()["success"], False)
            else:
                self.assertEqual(res.json()["success"], False)

    # case17: 添加WPA-PSK加密SSID
    def testAdd2GSSIDPsk(self):
        self.add2GSSIDPsk("2G_PSK_SHORTEST", 1, 0, 1, 1, "12345678", 30, 0, 0)
        self.add2GSSIDPsk("2G_PSK_LONGEST", 4094, 1, 3, 3, longestpwd, 8640000, 1, 1)

    # case18: 添加WPA-PSK加密SSID(密钥太短)
    # EAP120/220有问题，可以写入
    def testAdd2GSSIDPskPwdTooShort(self):
        self.add2GSSIDPsk(ssidName="2G_PSK_PWD_TOO_SHORT", psk_key="1234567")

    # case19: 添加WPA-PSK加密SSID(密钥太长)
    # EAP120/220有问题，可以写入
    def testAdd2GSSIDPskPwdTooLong(self):        
        self.add2GSSIDPsk(ssidName="2G_PSK_PWD_TOO_LONG", psk_key=longestpwd + "a")

    # case20: 添加WPA-PSK加密SSID(重名)
    def testAdd2GSSIDPskExist(self):
        self.add2GSSIDPsk(ssidName="PSK_EXIST")
        self.add2GSSIDPsk(ssidName="PSK_EXIST")


    # 修改SSID(改什么就POST什么)
    def update2GSSIDByIndex(self, index=0, newData=""):
        oldData = self.getWireless2GSSID()["data"]
        if index<len(oldData):
            oldData = oldData[index]
            data = {
                    "operation": "update",
                    "index": index,
                    "key": oldData["key"],
                    "old": oldData,
                    "new": json.dumps(newData)
                    }
            res = self.s.post("http://%s/data/wireless.ssids.json" %(utils.ip), data, headers=utils.header_eap220)
            # 简单判断一下
            self.assertEqual(res.json()["success"], True)
            SSIDS = self.getWireless2GSSID()
            self.assertTrue(self.isNameExist(newData["ssidname"]))
        else:
            pass

    # case21: 修改SSID
    def testUpdate2GSSID(self):
        newData1 = {
                    "ssidname":"update_1",
                    "vlanid":"4094",
                    "ssidbcast":"1",
                    "securityMode":"0",
                    "portal":"0",
                    "isolation":"0"
                    }
        newData2 = {
                    "ssidname":"update_2",
                    "vlanid":"4094",
                    "ssidbcast":"1",
                    "securityMode":"3",
                    "psk_version":"3",
                    "psk_cipher":"1",
                    "psk_key":"1234567890",
                    "psk_key_update_2g":"0",
                    "wep_format1":"2",
                    "portal":"0",
                    "isolation":"0"
                    }
        self.update2GSSIDByIndex(newData=newData1)
        self.update2GSSIDByIndex(1, newData2)
        self.update2GSSIDByIndex(10, newData1)

    # 2.4G删除SSID
    def remove2GSSID(self, index=0):
        SSIDS = self.getWireless2GSSID()["data"]
        if index<len(SSIDS):
            target = SSIDS[index]
            data = {"operation": "remove", "index": "%d"%index, "key": target["key"]}
            res = self.s.post("http://%s/data/wireless.ssids.json" %(utils.ip), data, headers=utils.header_eap220)
            self.assertEqual(res.json()["success"], True)
            self.assertFalse(self.isNameExist(target["ssidname"]))
        else:
            data = {"operation": "remove", "index": "%d"%index, "key": -1}
            res = self.s.post("http://%s/data/wireless.ssids.json" %(utils.ip), data, headers=utils.header_eap220)
            if self.dutMode in {"EAP320", "EAP330"}:
                self.assertEqual(res.json()["success"], False)
            else:
                # EAP220返回true，但什么也没删掉
                self.assertEqual(res.json()["success"], True)

    # case22: 删除SSID
    def testRemove2GSSID(self):
        self.add2GSSIDNoPwd(ssidName="remove")
        self.remove2GSSID(0)

    # case23: 删除不存在的SSID
    def testRemove2GSSIDNotExist(self):
        self.remove2GSSID(100)

    # 2.4G清空所有SSID
    def remove2GAllSSIDS(self):
        SSIDS = self.getWireless2GSSID()["data"]
        for ssid in SSIDS:
            data = {"operation": "remove", "index": "0", "key": ssid["key"]}
            res = self.s.post("http://%s/data/wireless.ssids.json" %(utils.ip), data, headers=utils.header_eap220)
        SSIDS = self.getWireless2GSSID()["data"]
        self.assertEqual(len(SSIDS), 0)


# 2.4G无线扩展设置
class wireless2GAdv(wirelessBasic):

    # 扩展设置
    # beacon_interval:  40~100
    # dtim_period:      1~255
    # rts_threshold:    1~2347
    # frag_threshold:   256~2346，仅用于11b/g模式
    def set2GAdv(self, beacon_interval=100, dtim_period=1, rts_threshold=2347, frag_threshold=2346, atf="on", legal=True):
        data = {
                "operation": "write",
                "wireless_beacon_interval": beacon_interval,
                "wireless_dtim_period": dtim_period,
                "wireless_rts_threshold": rts_threshold,
                "wireless_frag_threshold": frag_threshold,
               }
        if self.dutMode in {"EAP320", "EAP330"}:
            data["wireless_atf"] = atf
        res = self.s.post("http://%s/data/wireless.adv.json" %(utils.ip), data, headers=utils.header_eap220)
        if True==legal:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["data"]["beaconinter"], beacon_interval)
            self.assertEqual(res.json()["data"]["dtimperiod"], dtim_period)
            self.assertEqual(res.json()["data"]["rtsshreshold"], rts_threshold)
            self.assertEqual(res.json()["data"]["fragshreshold"], frag_threshold)
            if self.dutMode in {"EAP320", "EAP330"}:
                self.assertEqual(res.json()["data"]["atf"], atf)
        else:
            self.assertEqual(res.json()["success"], False)

    # case24: 2.4G扩展设置
    def testSet2GAdv(self):
        self.set2GAdv(40, 1, 1, 256, "off")
        self.set2GAdv(100, 255, 2347, 2346, "on")

    # case25: 2.4G扩展设置(beacon错误)
    # EAP120/220/320/330有问题，可以写入(不影响上网，按错误值发送Beacon)
    def testSet2GAdvWrongBeacon(self):
        self.set2GAdv(beacon_interval=200, legal=False)

    # case26: 2.4G扩展设置(dtim错误)
    # EAP120/220有问题，可以写入
    def testSet2GAdvWrongDtim(self):
        self.set2GAdv(dtim_period=256, legal=False)

    # case27: 2.4G扩展设置(rts错误)
    # EAP120/220有问题，可以写入
    def testSet2GAdvWrongRts(self):
        self.set2GAdv(rts_threshold=2348, legal=False)

    # case28: 2.4G扩展设置(frag错误)
    # EAP120/220有问题，可以写入
    def testSet2GAdvWrongFrag(self):
        self.set2GAdv(frag_threshold=2347, legal=False)


# 2.4G无线负载平衡设置
class wireless2GBalance(wirelessBasic):

    # 负载平衡设置
    def set2GBalance(self, lb_enable="off", max_client=10):
        if self.dutMode in {"EAP320", "EAP330"}:
            data = {
                    "operation": "write",
                    "lb_enable": lb_enable,
                    "max_client": max_client
                   }
            res = self.s.post("http://%s/data/wireless.lb.json" %(utils.ip), data, headers=utils.header_eap220)
            if max_client>=1 and max_client<=99:
                self.assertEqual(res.json()["success"], True)
                self.assertEqual(res.json()["data"]["lb_enable"], lb_enable)
                self.assertEqual(res.json()["data"]["max_client"], max_client)
            else:
                self.assertEqual(res.json()["success"], False)
        else:
            data = {
                    "operation": "write",
                    "lb_2G": lb_enable,
                    "max_client2G": max_client
                    }
            res = self.s.post("http://%s/data/clusterLoadBalance.json" %(utils.ip), data, headers=utils.header_eap220)
            if max_client>=1 and max_client<=99:
                self.assertEqual(res.json()["success"], True)
                self.assertEqual(res.json()["data"]["lb_2G"], lb_enable)
                self.assertEqual(res.json()["data"]["max_client2G"], max_client)
            else:
                self.assertEqual(res.json()["success"], False)

    # case29: 负载平衡设置
    def testSet2GBalance(self):
        self.set2GBalance("off", 1)
        self.set2GBalance("on", 99)
        self.set2GBalance("on", 1)

    # case30: 负载平衡设置(超过上限)
    # EAP120/220/320/330有问题，可以写入(设备不够，无法实测)
    def testSet2GBalanceTooBig(self):
        self.set2GBalance("on", 100)


# 5G无线基本设置
class wireless5GBasic(wirelessBasic):

    # EAP320基本设置
    # wirelessmode: 8: 11ac;    9: 11n/ac;  10: 11a/n/ac
    # chwidth:      2: 20MHz;   3: 40MHz;   5:80MHz;    6: 20/40/80MHz
    # channel:      0: Auto;    36、40、44、48、149、153、157、161: 各个信道
    # txpower:      发射功率:   若channel为36~48: 1~23;   若channel为0或149~161: 1~30
    # isapmode:     未知
    def set5GBasicEAP320(self, status="on", wirelessmode=10, chwidth=6, channel=0, txpower=20, legal=True):
        data = {
                "operation": "write",
                "wireless-bset-status-5ghz": status,
                "wireless_mode_5g": "%d"%wirelessmode,
                "chan_width_5g": "%d"%chwidth,
                "channel_5g": "%d"%channel,
                "txpower_5g": "%d"%txpower,
                "is_apmode": "1"
               }
        res = self.s.post("http://%s/data/wireless.basic.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
        if True==legal:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["data"]["status"], status)
            self.assertEqual(res.json()["data"]["wirelessmode"], wirelessmode)
            self.assertEqual(res.json()["data"]["chwidth"], chwidth)
            self.assertEqual(res.json()["data"]["channel"], channel)
            self.assertEqual(res.json()["data"]["txpower"], txpower)
        else:
            self.assertEqual(res.json()["success"], False)

    # EAP220基本设置
    # wirelessmode: 5: 11a;     6: 11n;     7: 11a/n
    # chwidth:      2: 20MHz;   3: 40MHz;   4: 20/40MHz
    # channel:      0: Auto;    1~4: 36、40、44、48信道;     17~21: 149、153、157、161、165信道
    # txpower:      发射功率:   若channel为36~48: 1~23;   若channel为0或149~161: 1~26
    # isapmode:     未知
    def set5GBasicEAP220(self, status="on", wirelessmode=7, chwidth=4, channel=0, txpower=20, legal=True):
        data = {
                "operation": "write",
                "wireless-bset-status-5ghz": status,
                "wireless_mode_5g": "%d"%wirelessmode,
                "chan_width_5g": "%d"%chwidth,
                "channel_5g": "%d"%channel,
                "txpower_5g": "%d"%txpower,
                "is_apmode": "1"
               }
        res = self.s.post("http://%s/data/wireless.basic.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
        if True==legal:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["data"]["status"], status)
            self.assertEqual(res.json()["data"]["wirelessmode"], wirelessmode)
            self.assertEqual(res.json()["data"]["chwidth"], chwidth)
            if self.dutMode in {"EAP320", "EAP330"}:
                # EAP320响应中返回错误值，但被后台改成0
                self.assertEqual(res.json()["data"]["channel"], channel)
            else:
                if not channel in {1,2,3,4,17,18,19,20,21}:
                    # EAP220响应中直接被改成0
                    self.assertEqual(res.json()["data"]["channel"], 0)
                else:
                    self.assertEqual(res.json()["data"]["channel"], channel)
            self.assertEqual(res.json()["data"]["txpower"], txpower)
        else:
            self.assertEqual(res.json()["success"], False)

    # case31: 5G基本设置
    def testSet5GBasic(self):
        if self.dutMode in {"EAP320", "EAP330"}:
            self.set5GBasicEAP320()
            self.set5GBasicEAP320("off", 10, 2, 161, 30)
        elif self.dutMode in {"EAP220"}:
            self.set5GBasicEAP220()
            self.set5GBasicEAP220("off", 5, 2, 21, 26)
        else:
            pass

    # case32: 5G基本设置(模式错误)
    # EAP220严重问题，输入错误的wirelessmode导致机子崩溃
    def testSet5GBasicWrongMode(self):
        if self.dutMode in {"EAP320", "EAP330"}:
            self.set5GBasicEAP320(wirelessmode=7, legal=False)
        elif self.dutMode in {"EAP220"}:
            # 自动测试时需注释掉，否则AP挂掉，后面的测试全崩
            #self.set5GBasicEAP220(wirelessmode=10, legal=False)
            raise Exception("EAP220 has a serious error here, input a wrong wirelessmode will cause a system crash !")
        else:
            pass

    # case33: 5G基本设置(信道错误)
    def testSet5GBasicWrongChannel(self):
        if self.dutMode in {"EAP320", "EAP330"}:
            self.set5GBasicEAP320(channel=100)
        elif self.dutMode in {"EAP220"}:
            self.set5GBasicEAP220(channel=100)
        else:
            pass

    # case34: 5G基本设置(带宽错误)
    def testSet5GBasicWrongWidth(self):
        if self.dutMode in {"EAP320", "EAP330"}:
            self.set5GBasicEAP320(chwidth=4, legal=False)
        elif self.dutMode in {"EAP220"}:
            # EAP220返回true，但被后台改成正确值
            self.set5GBasicEAP220(chwidth=5, legal=False)

    # case35: 5G基本设置(功率过大)
    # EAP120/220/320有问题，可以写入(不影响上网)
    def testSet5GBasicWrongPower(self):
        if self.dutMode in {"EAP320", "EAP330"}:
            self.set5GBasicEAP320(txpower=31, legal=False)
        elif self.dutMode in {"EAP220"}:
            self.set5GBasicEAP220(txpower=27, legal=False)
        else:
            pass


# 5G SSID设置
class wireless5GSSID(wirelessBasic):

    # 判断是否重名
    def isNameExist(self, ssidName):
        SSIDS = self.getWireless5GSSID()["data"]
        for ssid in SSIDS:
            if ssid["ssidname_5g"]==ssidName:
                return True
        return False

    # 判断WEP加密SSID是否存在
    def isWEPExist(self):
        SSIDS = self.getWireless5GSSID()["data"]
        for ssid in SSIDS:
            if 1==ssid["securityMode_5g"]:
                return True
        return False

    # 按名称查找SSID
    def getSSIDByName(self, ssidName=""):
        SSIDS = self.getWireless5GSSID()["data"]
        for ssid in SSIDS:
            if ssid["ssidname_5g"]==ssidName:
                return ssid

    # 5G添加无加密SSID
    # vlanid:   1~4094
    # ssidbcast、portal、isolation:  0或1
    def add5GSSIDNoPwd(self, ssidName="TP-LINK_5G", vlanid=1, ssidbcast=1, portal=0, isolation=0):
        oldData = self.getWireless5GSSID()
        if len(oldData["data"])>=7:
            # SSID过多就删掉前面的
            self.remove5GSSID()
        jdata = {
                "ssidname_5g": ssidName,
                "vlanid_5g": "%d"%vlanid,
                "ssidbcast_5g": "%d"%ssidbcast,
                "securityMode_5g": "0",
                "portal_5g": "%d"%portal,
                "isolation_5g": "%d"%isolation
                }
        data = {
                "operation": "insert",
                "key": "add",
                "index": "0",
                "old": "add",
                "new": json.dumps(jdata)
                }
        if self.isNameExist(ssidName):
            res = self.s.post("http://%s/data/wireless.ssids.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
            self.assertEqual(res.json()["success"], False)
        else:
            res = self.s.post("http://%s/data/wireless.ssids.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
            if vlanid>=1 and vlanid<=4094:
                newSSID = self.getSSIDByName(ssidName)
                self.assertEqual(newSSID["vlanid_5g"], vlanid)
                self.assertEqual(newSSID["ssidbcast_5g"], ssidbcast)
                self.assertEqual(newSSID["securityMode_5g"], 0)
                self.assertEqual(newSSID["portal_5g"], portal)
                self.assertEqual(newSSID["isolation_5g"], isolation)
            else:
                self.assertEqual(res.json()["success"], False)

    # case36: 添加无加密SSID
    def testAdd5GSSIDNoPwd(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDNoPwd()
            self.add5GSSIDNoPwd("5G_no_pwd_min", 1, 0, 0, 0)
            self.add5GSSIDNoPwd("5G_no_pwd_max", 4094, 1, 1, 1)

    # case37: 添加无加密SSID(重名)
    def testAdd5GSSIDNoPwdNameExist(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDNoPwd("5G_name1")
            self.add5GSSIDNoPwd("5G_name1")

    # case38: 添加无加密SSID(vlanid错误)
    def testAdd5GSSIDNoPwdWrongVlanid(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDNoPwd(ssidName="5G_wrong_vlanid", vlanid=4095)

    # 5G添加WEP加密SSID(只能设置一个)
    # wep_mode:     1: Open_System;    2: Shared_Key;    3: Auto
    # wep_select:   1~4: Key1~Key4
    # wep_format:   1: 数字;      2: ASCII字符
    # wep_type:     5: 64位;      13: 128位
    # wep_key:      format=1、type=5:    10位
    #               format=1、type=13:   26位
    #               format=2、type=5:    5位
    #               format=2、type=13:   13位
    def add5GSSIDWep(self, ssidName="TP-LINK_5G", vlanid=1, ssidbcast=1, wep_mode=3, wep_select=1, \
            wep_format=2, wep_type=5, wep_key="weppw", portal=0, isolation=0):
        oldData = self.getWireless5GSSID()
        if len(oldData["data"])>=7:
            # SSID过多就删掉前面的
            self.remove5GSSID()
        json_wep_format = "wep_format"+"%d"%wep_select+"_5g"
        json_wep_type = "wep_type"+"%d"%wep_select+"_5g"
        json_wep_key = "wep_key"+"%d"%wep_select+"_5g"
        jdata = {
                "ssidname_5g": ssidName,
                "vlanid_5g": "%d"%vlanid,
                "ssidbcast_5g": "%d"%ssidbcast,
                "securityMode_5g": "1",
                "wep_mode_5g": "%d"%wep_mode,
                "wep_select_5g": "%d"%wep_select,
                json_wep_format: "%d"%wep_format,
                json_wep_type: "%d"%wep_type,
                json_wep_key: wep_key,
                "portal_5g": "%d"%portal,
                "isolation_5g": "%d"%isolation
                }
        data = {
                "operation": "insert",
                "key": "add",
                "index": "0",
                "old": "add",
                "new": json.dumps(jdata)
                }
        if self.isWEPExist() or self.isNameExist(ssidName):
            # 存在WEP加密SSID或存在同名SSID，返回false
            res = self.s.post("http://%s/data/wireless.ssids.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
            self.assertEqual(res.json()["success"], False)
        else:
            res = self.s.post("http://%s/data/wireless.ssids.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
            if (1==wep_format and 5==wep_type and 10!=len(wep_key)) or (1==wep_format and 13==wep_type and 26!=len(wep_key)) \
                or (2==wep_format and 5==wep_type and 5!=len(wep_key)) or (2==wep_format and 13==wep_type and 13!=len(wep_key)):
                # 密钥位数不对，返回错误信息
                self.assertEqual(res.json()["success"], False)
            else:
                self.assertEqual(res.json()["success"], True)
                newSSID = self.getSSIDByName(ssidName)
                self.assertEqual(newSSID["vlanid_5g"], vlanid)
                self.assertEqual(newSSID["ssidbcast_5g"], ssidbcast)
                self.assertEqual(newSSID["securityMode_5g"], 1)
                self.assertEqual(newSSID["wep_mode_5g"], wep_mode)
                self.assertEqual(newSSID["wep_select_5g"], wep_select)
                self.assertEqual(newSSID[json_wep_format], wep_format)
                self.assertEqual(newSSID[json_wep_type], wep_type)
                self.assertEqual(newSSID[json_wep_key], wep_key)
                self.assertEqual(newSSID["portal_5g"], portal)
                self.assertEqual(newSSID["isolation_5g"], isolation)

    # case39: 添加WEP加密SSID
    def testAdd5GSSIDWep(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDWep(ssidName="5G_WEP", wep_select=4)

    # case40: 添加WEP加密SSID(密钥位数不对)
    def testAdd5GSSIDWepWrongKey(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDWep(ssidName="5G_WEP_WRONG_KEY", wep_key="hehehehehe123")

    # 5G添加WPA-ENTERPRISE加密SSID
    # wpa_version:      1: WPA-PSK;     2: WPA2-PSK;    3: Auto
    # wpa_chpher:       1: Auto;        2: TKIP;        3: AES
    # wpa_key_update_5g:    30~8640000: 密钥更新周期;   0: 不更新
    def add5GSSIDEnterprise(self, ssidName="TP-LINK_5G", vlanid=1, ssidbcast=1, wpa_version=3, wpa_cipher=1, \
                    server="192.168.1.1", port=0, wpa_key="11111111", wpa_key_update_5g=0, portal=0, isolation=0):
        oldData = self.getWireless5GSSID()
        if len(oldData["data"])>=7:
            # SSID过多就删掉前面的
            self.remove5GSSID()
        jdata = {
                "ssidname_5g": ssidName,
                "vlanid_5g": "%d"%vlanid,
                "ssidbcast_5g": "%d"%ssidbcast,
                "securityMode_5g": "2",
                "wpa_version_5g": "%d"%wpa_version,
                "wpa_cipher_5g": "%d"%wpa_cipher,
                "server_5g": server,
                "port_5g": "%d"%port,
                "wpa_key_5g": wpa_key,
                "wpa_key_update_5g": "%d"%wpa_key_update_5g,
                "portal_5g": "%d"%portal,
                "isolation_5g": "%d"%isolation
                }
        data = {
                "operation": "insert",
                "key": "add",
                "index": "0",
                "old": "add",
                "new": json.dumps(jdata)
                }
        if self.isNameExist(ssidName):
            res = self.s.post("http://%s/data/wireless.ssids.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
            if len(wpa_key)>=65:
                # 密钥超长，不返回信息
                self.assertEqual(res.content, "")
            else:
                self.assertEqual(res.json()["success"], False)
        else:
            res = self.s.post("http://%s/data/wireless.ssids.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
            if vlanid>=1 and vlanid<=4094 and len(wpa_key)>=8 and len(wpa_key)<=64:
                newSSID = self.getSSIDByName(ssidName)
                self.assertEqual(newSSID["vlanid_5g"], vlanid)
                self.assertEqual(newSSID["ssidbcast_5g"], ssidbcast)
                self.assertEqual(newSSID["securityMode_5g"], 2)
                self.assertEqual(newSSID["wpa_version_5g"], wpa_version)
                self.assertEqual(newSSID["wpa_cipher_5g"], wpa_cipher)
                self.assertEqual(newSSID["server_5g"], server)
                self.assertEqual(newSSID["port_5g"], port)
                self.assertEqual(newSSID["wpa_key_5g"], wpa_key)
                self.assertEqual(newSSID["wpa_key_update_5g"], wpa_key_update_5g)
                self.assertEqual(newSSID["portal_5g"], portal)
                self.assertEqual(newSSID["isolation_5g"], isolation)
            elif len(wpa_key)<=7:
                # 密钥太短，返回false
                self.assertEqual(res.json()["success"], False)
            elif len(wpa_key)>=65:
                if self.dutMode in {"EAP320", "EAP330"}:
                    # 密钥超长，EAP320不返回信息
                    self.assertEqual(res.content, "")
                else:
                    self.assertEqual(res.json()["success"], False)
            else:
                self.assertEqual(res.json()["success"], False)

    # case41: 添加Enterprise加密SSID
    def testAdd5GSSIDEnterprise(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.remove5GAllSSIDS()
            self.add5GSSIDEnterprise("5G_ENTERPRISE_SHORTEST", 1, 0, 1, 1, "1.0.0.1", 0, "12345678", 0, 0, 0)
            self.add5GSSIDEnterprise("5G_ENTERPRISE_LONGEST", 4094, 1, 3, 3, "223.255.255.254", 65535, longestpwd, 8640000, 1, 1)

    # case42: 添加Enterprise加密SSID(密钥太短)
    def testAdd5GSSIDEnterprisePwdTooShort(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDEnterprise(ssidName="5G_ENTERPRISE_PWD_TOO_SHORT", wpa_key="1234567")

    # case43: 添加Enterprise加密SSID(密钥太长)
    def testAdd5GSSIDEnterprisePwdTooLong(self):    
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDEnterprise(ssidName="5G_ENTERPRISE_PWD_TOO_LONG", wpa_key=longestpwd+"a")

    # case44: 添加Enterprise加密SSID(重名)
    def testAdd5GSSIDEnterpriseExist(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDEnterprise(ssidName="ENTERPRISE_EXIST")
            self.add5GSSIDEnterprise(ssidName="ENTERPRISE_EXIST")

    # 5G添加WPA-PSK加密SSID
    # psk_version:      1: WPA-PSK;     2: WPA2-PSK;    3: Auto
    # psk_cipher:       1: Auto;        2: TKIP;        3: AES
    def add5GSSIDPsk(self, ssidName="TP-LINK_5G", vlanid=1, ssidbcast=1, psk_version=3, \
                psk_cipher=1, psk_key="11111111", psk_key_update_5g=0, portal=0, isolation=0):
        oldData = self.getWireless5GSSID()
        if len(oldData["data"])>=7:
            # SSID过多就删掉前面的
            self.remove5GSSID()
        jdata = {
                "ssidname_5g": ssidName,
                "vlanid_5g": "%d"%vlanid,
                "ssidbcast_5g": "%d"%ssidbcast,
                "securityMode_5g": "3",
                "psk_version_5g": "%d"%psk_version,
                "psk_cipher_5g": "%d"%psk_cipher,
                "psk_key_5g": psk_key,
                "psk_key_update_5g": "%d"%psk_key_update_5g,
                "portal_5g": "%d"%portal,
                "isolation_5g": "%d"%isolation
                }
        data = {
                "operation": "insert",
                "key": "add",
                "index": "0",
                "old": "add",
                "new": json.dumps(jdata)
                }
        if self.isNameExist(ssidName):
            res = self.s.post("http://%s/data/wireless.ssids.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
            if len(psk_key)>=65:
                # 密钥超长，不返回信息
                self.assertEqual(res.content, "")
            else:
                self.assertEqual(res.json()["success"], False)
        else:
            res = self.s.post("http://%s/data/wireless.ssids.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
            if vlanid>=1 and vlanid<=4094 and len(psk_key)>=8 and len(psk_key)<=64:
                newSSID = self.getSSIDByName(ssidName)
                self.assertEqual(newSSID["vlanid_5g"], vlanid)
                self.assertEqual(newSSID["ssidbcast_5g"], ssidbcast)
                self.assertEqual(newSSID["securityMode_5g"], 3)
                self.assertEqual(newSSID["psk_version_5g"], psk_version)
                self.assertEqual(newSSID["psk_cipher_5g"], psk_cipher)
                self.assertEqual(newSSID["psk_key_5g"], psk_key)
                self.assertEqual(newSSID["psk_key_update_5g"], psk_key_update_5g)
                self.assertEqual(newSSID["portal_5g"], portal)
                self.assertEqual(newSSID["isolation_5g"], isolation)
            elif len(psk_key)<=7:
                # 密钥太短，返回false
                self.assertEqual(res.json()["success"], False)
            elif len(psk_key)>=65:
                if self.dutMode in {"EAP320", "EAP330"}:
                    # 密钥超长，EAP320不返回信息
                    self.assertEqual(res.content, "")
                else:
                    self.assertEqual(res.json()["success"], False)
            else:
                self.assertEqual(res.json()["success"], False)

    # case45: 添加WPA-PSK加密SSID
    def testAdd5GSSIDPsk(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDPsk("5G_PSK_SHORTEST", 1, 0, 1, 1, "12345678", 30, 0, 0)
            self.add5GSSIDPsk("5G_PSK_LONGEST", 4094, 1, 3, 3, longestpwd, 8640000, 1, 1)

    # case46: 添加WPA-PSK加密SSID(密钥太短)
    def testAdd5GSSIDPskPwdTooShort(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDPsk(ssidName="5G_PSK_PWD_TOO_SHORT", psk_key="1234567")

    # case47: 添加WPA-PSK加密SSID(密钥太长)
    def testAdd5GSSIDPskPwdTooLong(self):    
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDPsk(ssidName="5G_PSK_PWD_TOO_LONG", psk_key=longestpwd + "a")

    # case48: 添加WPA-PSK加密SSID(重名)
    def testAdd5GSSIDPskExist(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDPsk(ssidName="PSK_EXIST")
            self.add5GSSIDPsk(ssidName="PSK_EXIST")

    # 修改SSID(改什么就POST什么)
    def update5GSSIDByIndex(self, index=0, newData=""):
        oldData = self.getWireless5GSSID()["data"]
        if index<len(oldData):
            oldData = oldData[index]
            data = {
                    "operation": "update",
                    "index": index,
                    "key": oldData["key"],
                    "old": oldData,
                    "new": json.dumps(newData)
                    }
            res = self.s.post("http://%s/data/wireless.ssids.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
            # 简单判断一下
            self.assertEqual(res.json()["success"], True)
            SSIDS = self.getWireless5GSSID()
            self.assertTrue(self.isNameExist(newData["ssidname_5g"]))
        else:
            pass

    # case49: 修改SSID
    def testUpdate5GSSID(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            newData1 = {
                        "ssidname_5g":"5G_update_1",
                        "vlanid_5g":"1",
                        "ssidbcast_5g":"1",
                        "securityMode_5g":"3",
                        "psk_version_5g":"3",
                        "psk_cipher_5g":"1",
                        "psk_key_5g":"11111111",
                        "psk_key_update_5g":"0",
                        "wep_format1_5g":"2",
                        "portal_5g":"0",
                        "isolation_5g":"0"
                        }
            newData2 = {
                        "ssidname_5g":"5G_update_2",
                        "vlanid_5g":"4094",
                        "ssidbcast_5g":"1",
                        "securityMode_5g":"0",
                        "portal_5g":"0",
                        "isolation_5g":"0"
                        }
            self.update5GSSIDByIndex(newData=newData1)
            self.update5GSSIDByIndex(1, newData2)
            self.update5GSSIDByIndex(10, newData1)

    # 5G删除SSID
    def remove5GSSID(self, index=0):
        SSIDS = self.getWireless5GSSID()["data"]
        if index<len(SSIDS):
            target = SSIDS[index]
            data = {"operation": "remove", "index": "%d"%index, "key": target["key"]}
            res = self.s.post("http://%s/data/wireless.ssids.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
            self.assertEqual(res.json()["success"], True)
            self.assertFalse(self.isNameExist(target["ssidname_5g"]))
        else:
            data = {"operation": "remove", "index": "%d"%index, "key": -1}
            res = self.s.post("http://%s/data/wireless.ssids.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
            if self.dutMode in {"EAP320", "EAP330"}:
                self.assertEqual(res.json()["success"], False)
            else:
                # EAP220返回true，但什么也没删掉
                self.assertEqual(res.json()["success"], True)

    # case50: 删除SSID
    def testRemove5GSSID(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDNoPwd(ssidName="5G_remove")
            self.remove5GSSID(0)

    # case51: 删除不存在的SSID
    def testRemove5GSSIDNotExist(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.remove5GSSID(100)

    # 5G清空所有SSID
    def remove5GAllSSIDS(self):
        SSIDS = self.getWireless5GSSID()["data"]
        for ssid in SSIDS:
            data = {"operation": "remove", "index": "0", "key": ssid["key"]}
            res = self.s.post("http://%s/data/wireless.ssids.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
        SSIDS = self.getWireless5GSSID()["data"]
        self.assertEqual(len(SSIDS), 0)

    # case52: 重启后是否保留
    def testZ5GSSIDReboot(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.add5GSSIDNoPwd(ssidName="5G_reboot")
            ssidsBeforeReboot = self.getWireless5GSSID()["data"]
            self.s = self.reboot()
            ssidsAfterReboot = self.getWireless5GSSID()["data"]
            self.assertEqual(len(ssidsBeforeReboot), len(ssidsAfterReboot))
            self.assertTrue(self.isNameExist("5G_reboot"))


# 5G无线扩展设置
class wireless5GAdv(wirelessBasic):

    # 扩展设置
    # beacon_interval:  40~100
    # dtim_period:      1~255
    # rts_threshold:    1~2347
    # frag_threshold:   256~2346，仅用于11a模式
    def set5GAdv(self, beacon_interval=100, dtim_period=1, rts_threshold=2347, frag_threshold=2346, atf="on", legal=True):
        data = {
                "operation": "write",
                "wireless_beacon_interval_5g": beacon_interval,
                "wireless_dtim_period_5g": dtim_period,
                "wireless_rts_threshold_5g": rts_threshold,
                "wireless_frag_threshold_5g": frag_threshold,
               }
        if self.dutMode in {"EAP320", "EAP330"}:
            data["wireless_atf_5g"] = atf
        res = self.s.post("http://%s/data/wireless.adv.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
        if True==legal:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["data"]["beaconinter"], beacon_interval)
            self.assertEqual(res.json()["data"]["dtimperiod"], dtim_period)
            self.assertEqual(res.json()["data"]["rtsshreshold"], rts_threshold)
            self.assertEqual(res.json()["data"]["fragshreshold"], frag_threshold)
            if self.dutMode in {"EAP320", "EAP330"}:
                self.assertEqual(res.json()["data"]["atf"], atf)
        else:
            self.assertEqual(res.json()["success"], False)

    # case53: 5G扩展设置
    def testSet5GAdv(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.set5GAdv(40, 1, 1, 256, "off")
            self.set5GAdv(100, 255, 2347, 2346, "on")

    # case54: 5G扩展设置(beacon错误)
    # EAP120/220/320有问题，可以写入(不影响上网，按错误值发送Beacon)
    def testSet5GAdvWrongBeacon(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.set5GAdv(beacon_interval=101, legal=False)

    # case55: 5G扩展设置(dtim错误)
    # EAP220有问题，可以写入
    def testSet5GAdvWrongDtim(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.set5GAdv(dtim_period=256, legal=False)

    # case56: 5G扩展设置(rts错误)
    # EAP220有问题，可以写入
    def testSet5GAdvWrongRts(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.set5GAdv(rts_threshold=2348, legal=False)

    # case57: 5G扩展设置(frag错误)
    # EAP220有问题，可以写入
    def testSet5GAdvWrongFrag(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.set5GAdv(frag_threshold=2347, legal=False)


# 5G无线负载平衡设置
class wireless5GBalance(wirelessBasic):

    # 负载平衡设置
    def set5GBalance(self, lb_enable="off", max_client=10):
        if self.dutMode in {"EAP320", "EAP330"}:
            data = {
                    "operation": "write",
                    "lb_enable_5g": lb_enable,
                    "max_client_5g": max_client
                   }
            res = self.s.post("http://%s/data/wireless.lb.5ghz.json" %(utils.ip), data, headers=utils.header_eap220)
            if max_client>=1 and max_client<=99:
                self.assertEqual(res.json()["success"], True)
                self.assertEqual(res.json()["data"]["lb_enable"], lb_enable)
                self.assertEqual(res.json()["data"]["max_client"], max_client)
            else:
                self.assertEqual(res.json()["success"], False)
        else:
            data = {
                    "operation": "write",
                    "lb_5G": lb_enable,
                    "max_client5G": max_client
                    }
            res = self.s.post("http://%s/data/clusterLoadBalance.json" %(utils.ip), data, headers=utils.header_eap220)
            if max_client>=1 and max_client<=99:
                self.assertEqual(res.json()["success"], True)
                self.assertEqual(res.json()["data"]["lb_5G"], lb_enable)
                self.assertEqual(res.json()["data"]["max_client5G"], max_client)
            else:
                self.assertEqual(res.json()["success"], False)

    # case58: 负载平衡设置
    def testSet5GBalance(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.set5GBalance("off", 1)
            self.set5GBalance("on", 99)
            self.set5GBalance("on", 1)

    # case59: 负载平衡设置(超过上限)
    # EAP120/220/320有问题，可以写入(设备不够，无法实测)
    def testSet5GBalanceTooBig(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            self.set5GBalance("on", 100)

    # case60: 重启后是否保留
    def testZ5GBalanceReboot(self):
        if self.dutMode in {"EAP330", "EAP320", "EAP220"}:
            dataBeforeReboot = self.getWireless5GLb()["data"]
            self.s = self.reboot()
            dataAfterReboot = self.getWireless5GLb()["data"]
            self.assertEqual(dataBeforeReboot, dataAfterReboot)


if __name__ == "__main__":
    unittest.main()
