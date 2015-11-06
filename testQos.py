#!/usr/bin/env python
# -*-coding:utf8-*-
#############################################################################################################
#
# File      ：   testQos.py
# Author    ：   luliying
# Brief     ：   test Qos setting
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


# 2.4G Qos设置
class Qos2GBasic(utils.EAPLoginSession):

	# 登录
    @classmethod
    def setUpClass(cls):
        super(Qos2GBasic, cls).setUpClass()  # 单继承情况下，似乎不用管

    # 检查响应是否正确
    def checkBasicResponse(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["success"], True)

    # 获取2.4G Qos参数
    def getQos2GSetting(self):
        data = {"operation": "read"}
        res = self.s.get("http://%s/data/qos_setting.2g.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 设置2.4G Qos参数
    def setQos2GSetting(self, data={}, legal=True):
        res = self.s.get("http://%s/data/qos_setting.2g.json" %(utils.ip), params=data, headers=utils.header_eap220)
        if True==legal:
            self.checkBasicResponse(res)
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["error"], 0)
        else:
            if self.dutMode in {"EAP320"}:
                self.assertEqual(res.content, "")
            else:
                self.assertNotEqual(res.json()["error"], 0)


# 2.4G Qos测试
class Qos2GSetting(Qos2GBasic):

    # case1: 获取2.4G Qos参数
    def testGetQos2GSetting(self):
        self.getQos2GSetting()

    # case2: 设置2.4G Qos参数
    def testSetQos2GSetting(self):
        data_min = {
                    "operation":"write", "wmm_enable":"off", "ap_vo_aifs":0, "ap_vo_cwmin":1, "ap_vo_cwmax":1, "ap_vo_maxBurst":0, 
                    "ap_vi_aifs":0, "ap_vi_cwmin":1, "ap_vi_cwmax":1, "ap_vi_maxBurst":0, "ap_be_aifs":0, "ap_be_cwmin":1, 
                    "ap_be_cwmax":1, "ap_be_maxBurst":0, "ap_bk_aifs":0, "ap_bk_cwmin":1, "ap_bk_cwmax":1, "ap_bk_maxBurst":0, 
                    "sta_vo_aifs":0, "sta_vo_cwmin":1, "sta_vo_cwmax":1, "sta_vo_txopLimit":0, "sta_vi_aifs":0, "sta_vi_cwmin":1, 
                    "sta_vi_cwmax":1, "sta_vi_txopLimit":0, "sta_be_aifs":0, "sta_be_cwmin":1, "sta_be_cwmax":1, "sta_be_txopLimit":0, 
                    "sta_bk_aifs":0, "sta_bk_cwmin":1, "sta_bk_cwmax":1, "sta_bk_txopLimit":0, "noAck_enable":"off", "uapsd_enable":"off"
                    }
        data_max = {
                    "operation":"write", "wmm_enable":"on", "ap_vo_aifs":15, "ap_vo_cwmin":1023, "ap_vo_cwmax":1023, "ap_vo_maxBurst":8192, 
                    "ap_vi_aifs":15, "ap_vi_cwmin":1023, "ap_vi_cwmax":1023, "ap_vi_maxBurst":8192, "ap_be_aifs":15, "ap_be_cwmin":1023, 
                    "ap_be_cwmax":1023, "ap_be_maxBurst":8192, "ap_bk_aifs":15, "ap_bk_cwmin":1023, "ap_bk_cwmax":1023, "ap_bk_maxBurst":8192, 
                    "sta_vo_aifs":15, "sta_vo_cwmin":1023, "sta_vo_cwmax":1023, "sta_vo_txopLimit":8192, "sta_vi_aifs":15, "sta_vi_cwmin":1023, 
                    "sta_vi_cwmax":1023, "sta_vi_txopLimit":8192, "sta_be_aifs":15, "sta_be_cwmin":1023, "sta_be_cwmax":1023, "sta_be_txopLimit":8192, 
                    "sta_bk_aifs":15, "sta_bk_cwmin":1023, "sta_bk_cwmax":1023, "sta_bk_txopLimit":8192, "noAck_enable":"on", "uapsd_enable":"on"
                    }
        self.setQos2GSetting(data_min)
        self.setQos2GSetting(data_max)

    # case3: 设置非法2.4G Qos参数
    # EAP120/220响应不对，但没写入
    def testSetQos2GSettingWrong(self):
        data_wrong = {
                    "operation":"write", "wmm_enable":"on", "ap_vo_aifs":16, "ap_vo_cwmin":3, "ap_vo_cwmax":7, "ap_vo_maxBurst":1504, 
                    "ap_vi_aifs":1, "ap_vi_cwmin":7, "ap_vi_cwmax":15, "ap_vi_maxBurst":3008, "ap_be_aifs":3, "ap_be_cwmin":15, 
                    "ap_be_cwmax":63, "ap_be_maxBurst":0, "ap_bk_aifs":7, "ap_bk_cwmin":15, "ap_bk_cwmax":1023, "ap_bk_maxBurst":0, 
                    "sta_vo_aifs":2, "sta_vo_cwmin":3, "sta_vo_cwmax":7, "sta_vo_txopLimit":1504, "sta_vi_aifs":2, "sta_vi_cwmin":7, 
                    "sta_vi_cwmax":15, "sta_vi_txopLimit":3008, "sta_be_aifs":3, "sta_be_cwmin":15, "sta_be_cwmax":1023, "sta_be_txopLimit":0, 
                    "sta_bk_aifs":7, "sta_bk_cwmin":15, "sta_bk_cwmax":1023, "sta_bk_txopLimit":0, "noAck_enable":"on", "uapsd_enable":"on"
                    }
        self.setQos2GSetting(data_wrong, False)


# 5G Qos设置
class Qos5GBasic(utils.EAPLoginSession):

    # 登录
    @classmethod
    def setUpClass(cls):
        super(Qos5GBasic, cls).setUpClass()  # 单继承情况下，似乎不用管

    # 检查响应是否正确
    def checkBasicResponse(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["success"], True)

    # 获取5G Qos参数
    def getQos5GSetting(self):
        data = {"operation": "read"}
        res = self.s.get("http://%s/data/qos_setting.5g.json" %(utils.ip), params=data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 设置5G Qos参数
    def setQos5GSetting(self, data={}, legal=True):
        res = self.s.get("http://%s/data/qos_setting.5g.json" %(utils.ip), params=data, headers=utils.header_eap220)
        if True==legal:
            self.checkBasicResponse(res)
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["error"], 0)
        else:
            if self.dutMode in {"EAP320"}:
                self.assertEqual(res.content, "")
            else:
                self.assertNotEqual(res.json()["error"], 0)


# 5G Qos测试
class Qos5GSetting(Qos5GBasic):

    # case4: 获取5G Qos参数
    def testGetQos5GSetting(self):
        if self.dutMode not in {"EAP120"}:
            self.getQos5GSetting()

    # case5: 设置5G Qos参数
    def testSetQos5GSetting(self):
        data_min = {
                    "operation":"write", "wmm_enable":"off", "ap_vo_aifs":0, "ap_vo_cwmin":1, "ap_vo_cwmax":1, "ap_vo_maxBurst":0, 
                    "ap_vi_aifs":0, "ap_vi_cwmin":1, "ap_vi_cwmax":1, "ap_vi_maxBurst":0, "ap_be_aifs":0, "ap_be_cwmin":1, 
                    "ap_be_cwmax":1, "ap_be_maxBurst":0, "ap_bk_aifs":0, "ap_bk_cwmin":1, "ap_bk_cwmax":1, "ap_bk_maxBurst":0, 
                    "sta_vo_aifs":0, "sta_vo_cwmin":1, "sta_vo_cwmax":1, "sta_vo_txopLimit":0, "sta_vi_aifs":0, "sta_vi_cwmin":1, 
                    "sta_vi_cwmax":1, "sta_vi_txopLimit":0, "sta_be_aifs":0, "sta_be_cwmin":1, "sta_be_cwmax":1, "sta_be_txopLimit":0, 
                    "sta_bk_aifs":0, "sta_bk_cwmin":1, "sta_bk_cwmax":1, "sta_bk_txopLimit":0, "noAck_enable":"off", "uapsd_enable":"off"
                    }
        data_max = {
                    "operation":"write", "wmm_enable":"on", "ap_vo_aifs":15, "ap_vo_cwmin":1023, "ap_vo_cwmax":1023, "ap_vo_maxBurst":8192, 
                    "ap_vi_aifs":15, "ap_vi_cwmin":1023, "ap_vi_cwmax":1023, "ap_vi_maxBurst":8192, "ap_be_aifs":15, "ap_be_cwmin":1023, 
                    "ap_be_cwmax":1023, "ap_be_maxBurst":8192, "ap_bk_aifs":15, "ap_bk_cwmin":1023, "ap_bk_cwmax":1023, "ap_bk_maxBurst":8192, 
                    "sta_vo_aifs":15, "sta_vo_cwmin":1023, "sta_vo_cwmax":1023, "sta_vo_txopLimit":8192, "sta_vi_aifs":15, "sta_vi_cwmin":1023, 
                    "sta_vi_cwmax":1023, "sta_vi_txopLimit":8192, "sta_be_aifs":15, "sta_be_cwmin":1023, "sta_be_cwmax":1023, "sta_be_txopLimit":8192, 
                    "sta_bk_aifs":15, "sta_bk_cwmin":1023, "sta_bk_cwmax":1023, "sta_bk_txopLimit":8192, "noAck_enable":"on", "uapsd_enable":"on"
                    }
        if self.dutMode not in {"EAP120"}:
            self.setQos5GSetting(data_min)
            self.setQos5GSetting(data_max)

    # case6: 设置非法5G Qos参数
    # EAP120/220响应不对，但没写入
    def testSetQos5GSettingWrong(self):
        data_wrong = {
                    "operation":"write", "wmm_enable":"on", "ap_vo_aifs":16, "ap_vo_cwmin":3, "ap_vo_cwmax":7, "ap_vo_maxBurst":1504, 
                    "ap_vi_aifs":1, "ap_vi_cwmin":7, "ap_vi_cwmax":15, "ap_vi_maxBurst":3008, "ap_be_aifs":3, "ap_be_cwmin":15, 
                    "ap_be_cwmax":63, "ap_be_maxBurst":0, "ap_bk_aifs":7, "ap_bk_cwmin":15, "ap_bk_cwmax":1023, "ap_bk_maxBurst":0, 
                    "sta_vo_aifs":2, "sta_vo_cwmin":3, "sta_vo_cwmax":7, "sta_vo_txopLimit":1504, "sta_vi_aifs":2, "sta_vi_cwmin":7, 
                    "sta_vi_cwmax":15, "sta_vi_txopLimit":3008, "sta_be_aifs":3, "sta_be_cwmin":15, "sta_be_cwmax":1023, "sta_be_txopLimit":0, 
                    "sta_bk_aifs":7, "sta_bk_cwmin":15, "sta_bk_cwmax":1023, "sta_bk_txopLimit":0, "noAck_enable":"on", "uapsd_enable":"on"
                    }
        if self.dutMode not in {"EAP120"}:
            self.setQos5GSetting(data_wrong, False)


if __name__ == "__main__":
    unittest.main()
