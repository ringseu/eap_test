#!/usr/bin/env python
# -*-coding:utf8-*-
#############################################################################################################
#
# File      ：   testRogue.py
# Author    ：   luliying
# Brief     ：   test rogue detection
# 
# Version   ：   1.0.1
# Date      ：   3 Nov 2015
# 
# History   ：   
#                1.0.1  luliying  2015.11.03  finish
#                1.0.0  luliying  2015.11.03  create the file
#
#############################################################################################################


from utils import utils
import json


# Rogue设备检测设置
class rogueDetectBasic(utils.EAPLoginSession):

	# 登录
    @classmethod
    def setUpClass(cls):
        super(rogueDetectBasic, cls).setUpClass()  # 单继承情况下，似乎不用管

    # 检查响应是否正确
    def checkBasicResponse(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["success"], True)

    # 获取Rogue设备
    def getRogueAPs(self):
        data = {"operation": "load"}
        res = self.s.get("http://%s/data/rogueApDetect.raList.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取受信任设备
    def getTrustedAPs(self):
        data = {"operation": "load"}
        res = self.s.get("http://%s/data/rogueApDetect.taList.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 开启或关闭Rogue设备检测
    def setRogueDetectStatus(self, status="off"):
        data = {"operation": "write", "ra_status": status}
        res = self.s.get("http://%s/data/rogueApDetect.status.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        self.assertEqual(res.json()["data"]["ra_status"], status)

    # 扫描Rogue设备
    def scanRogueDevices(self):
        data = {"operation": "scan"}
        res = self.s.get("http://%s/data/rogueApDetect.scan.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        self.assertEqual(res.json()["error"], 0)

    # 获取扫描结果
    def getRogueDetectResults(self):
        self.scanRogueDevices()
        data = {"operation": "getScanState"}
        res = self.s.get("http://%s/data/rogueApDetect.scanState.json" %(utils.ip), params=data, headers=utils.header_eap220)
        while True!=res.json()["data"]["refresh"]:
            res = self.s.get("http://%s/data/rogueApDetect.scanState.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.getRogueAPs()
        self.getTrustedAPs()


# Rogue设备检测测试
class rogueDetect(rogueDetectBasic):

    # case1: 获取Rogue设备
    def testGetRogueAPs(self):
        self.getRogueAPs()

    # case2: 获取受信任设备
    def testGetTrustedAPs(self):
        self.getTrustedAPs()

    # case3: 开启或关闭Rogue设备检测
    def testSetRogueDetectStatus(self):
        self.setRogueDetectStatus()
        self.setRogueDetectStatus("on")

    # case4: 获取扫描结果
    def testGetRogueDetectResults(self):
        self.setRogueDetectStatus("on")
        self.getRogueDetectResults()


if __name__ == "__main__":
    unittest.main()
