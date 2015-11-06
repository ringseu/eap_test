#!/usr/bin/env python
# -*-coding:utf8-*-
#############################################################################################################
#
# File      ：   testScheduler.py
# Author    ：   luliying
# Brief     ：   test wireless scheduler
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


class schedulerBasic(utils.EAPLoginSession):

	# 登录
    @classmethod
    def setUpClass(cls):
        super(schedulerBasic, cls).setUpClass()  # 单继承情况下，似乎不用管

    # 检查响应是否正确
    def checkBasicResponse(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["success"], True)

    # 获取定时状态
    def getSchedulerStatus(self):
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/scheduler.set.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取定时组
    def getSchedulerProfiles(self):
        data = {"operation": "load"}
        res = self.s.post("http://%s/data/scheduler.profile.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取定时规则
    def getSchedulerRules(self):
        data = {"operation": "load"}
        res = self.s.post("http://%s/data/scheduler.rule.json" %(utils.ip), data, headers=utils.header_eap220)
        if self.dutMode in {"EAP120", "EAP220"}:
            self.checkBasicResponse(res)
            return res.json()

    # 获取某个定时组的规则
    def getSchedulerRulesByName(self, profileName):
        data = {"operation": "load", "profileName": profileName}
        res = self.s.post("http://%s/data/scheduler.rule.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取定时配置(SSID模式)
    def getSchedulerAssociation(self):
        data = {"operation": "load"}
        res = self.s.post("http://%s/data/scheduler.association.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取定时配置(AP模式)
    def getSchedulerAssociationAP(self):
        data = {"operation": "load"}
        res = self.s.post("http://%s/data/scheduler.associationAp.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 开启或关闭定时功能
    def setSchedulerStatus(self, status="off", scheduler_type=0):
        data = {"operation": "write", "status": status, "scheduler_type": "%d"%scheduler_type}
        res = self.s.post("http://%s/data/scheduler.set.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        self.assertEqual(res.json()["data"]["status"], status)
        self.assertEqual(res.json()["data"]["scheduler_type"], scheduler_type)

    # 判断组是否存在
    def isProfileExist(self, profileName):
        profiles = self.getSchedulerProfiles()["data"]
        for profile in profiles:
            if profileName==profile["profileName"]:
                return True
        return False

    # 按名字查找组
    def getProfileByName(self, profileName):
        profiles = self.getSchedulerProfiles()["data"]
        for profile in profiles:
            if profileName==profile["profileName"]:
                return profile


# 测试定时基本设置
class getSchedulerBasic(schedulerBasic):

    # case1: 获取Scheduler设置
    def testSchedulerConfig(self):
        self.getSchedulerStatus()
        self.getSchedulerProfiles()
        self.getSchedulerRules()
        self.getSchedulerAssociation()
        self.getSchedulerAssociationAP()

    # case2: 开启关闭Scheduler功能
    def testSetSchedulerStatus(self):
        self.setSchedulerStatus("off", 1)
        self.setSchedulerStatus("on", 0)


# 定时组
class schedulerProfilesBasic(schedulerBasic):

    # 添加定时组
    def addProfile(self, profileName):
        profiles = self.getSchedulerProfiles()["data"]
        if len(profiles)>=7:
            # Scheduler组太多就先删掉
            self.removeSchedulerProfile(0)
        jdata = {"profileName": profileName}
        data = {
                "operation": "insert",
                "key": "add",
                "index": "0",
                "old": "add",
                "new": json.dumps(jdata)
                }
        if True==self.isProfileExist(profileName):
            # 重名
            res = self.s.post("http://%s/data/scheduler.profile.json" %(utils.ip), data, headers=utils.header_eap220)
            if self.dutMode in {"EAP120", "EAP220"}:
                self.checkBasicResponse(res)
                self.assertEqual(res.json()["error"], -1)
            else:
                self.assertEqual(res.json()["success"], False)
                self.assertEqual(res.json()["error"], -1)
        else:
            res = self.s.post("http://%s/data/scheduler.profile.json" %(utils.ip), data, headers=utils.header_eap220)
            self.checkBasicResponse(res)
            self.assertEqual(res.json()["error"], 0)
            self.assertTrue(self.isProfileExist(profileName))

    # 修改定时组
    def updateProfile(self, index=0, profileName=""):
        oldData = self.getSchedulerProfiles()["data"][index]
        jdata = {"profileName": oldData["profileName"], "key": oldData["key"]}
        newJdata = {"profileName": profileName}
        data = {
                "operation": "update",
                "index": index,
                "key": oldData["key"],
                "old": json.dumps(jdata),
                "new": json.dumps(newJdata)
                }
        if True==self.isProfileExist(profileName):
            # 重名
            res = self.s.post("http://%s/data/scheduler.profile.json" %(utils.ip), data, headers=utils.header_eap220)
            if self.dutMode in {"EAP120", "EAP220"}:
                self.checkBasicResponse(res)
                self.assertEqual(res.json()["error"], -1)
            else:
                self.assertEqual(res.json()["success"], False)
                self.assertEqual(res.json()["error"], -1)
        else:
            res = self.s.post("http://%s/data/scheduler.profile.json" %(utils.ip), data, headers=utils.header_eap220)
            self.checkBasicResponse(res)
            self.assertEqual(res.json()["error"], 0)
            self.assertEqual(res.json()["data"][index]["profileName"], profileName)

    # 删除定时组
    def removeProfile(self, index=0):
        oldData = self.getSchedulerProfiles()["data"]
        if index>=0 and index<len(oldData):
            data = {"operation": "remove", "key": oldData[index]["key"], "index": index}
            res = self.s.post("http://%s/data/scheduler.profile.json" %(utils.ip), data, headers=utils.header_eap220)
            self.checkBasicResponse(res)
            self.assertEqual(res.json()["error"], 0)
        else:
            # 参数不正确
            data = {"operation": "remove", "key": -1, "index": index}
            res = self.s.post("http://%s/data/scheduler.profile.json" %(utils.ip), data, headers=utils.header_eap220)
            self.assertEqual(res.json()["error"], -1)

    # 清空定时组
    def removeAllProfiles(self):
        profiles = self.getSchedulerProfiles()["data"]
        for profile in profiles:
            data = {"operation": "remove", "key": profile["key"], "index": 0}
            res = self.s.post("http://%s/data/scheduler.profile.json" %(utils.ip), data, headers=utils.header_eap220)
        profiles = self.getSchedulerProfiles()["data"]
        self.assertEqual(len(profiles), 0)


# 测试定时组
class schedulerProfiles(schedulerProfilesBasic):

    # case3: 添加定时组
    def testAddSchedulerProfile(self):
        self.removeAllProfiles()
        self.addProfile("Add_Profile_1")

    # case4: 添加重名定时组
    def testAddSchedulerProfileExist(self):
        self.addProfile("Profile_Exist_1")
        self.addProfile("Profile_Exist_1")

    # case5: 修改定时组
    def testUpdateSchedulerProfile(self):
        self.addProfile("Profile_Before_Change")
        self.updateProfile(0, "Profile_After_Change")

    # case6: 修改重名定时组
    # EAP120/220有问题，可以修改
    def testUpdateSchedulerProfileExist(self):
        self.addProfile("Profile_Hold_Position")
        self.addProfile("Profile_Change_Exist")
        self.updateProfile(0, "Profile_Change_Exist")

    # case7: 删除定时组
    def testRemoveSchedulerProfile(self):
        self.addProfile("Profile_Remove")
        self.removeProfile(0)

    # case8: 删除不存在的定时组
    def testRemoveSchedulerProfileNotExist(self):
        self.removeProfile(8)


# 定时规则
class schedulerRules(schedulerProfilesBasic):

    # 添加规则
    def addSchedulerRule(self, profileName="", jdata={}, legal=True):
        data = {
                "operation": "insert",
                "key": "add",
                "index": 0,
                "old": "add",
                "new": json.dumps(jdata)
                }
        res = self.s.post("http://%s/data/scheduler.rule.json" %(utils.ip), data, headers=utils.header_eap220)
        if False==self.isProfileExist(profileName):
            # 目标组不存在
            if self.dutMode in {"EAP120", "EAP220"}:
                self.assertEqual(res.json()["error"], -1)
            else:
                self.assertEqual(res.content, "")
        else:
            if True==legal:
                self.assertEqual(res.json()["success"], True)
                self.assertEqual(res.json()["error"], 0)
            else:
                # 非法规则
                self.assertEqual(res.json()["error"], -1)

    # case9: 添加定时规则
    def testAddSchedulerRule(self):
        self.removeAllProfiles()
        jdata_weekends = {
                        "proName":"Add_Rule",
                        "weekDay":"1",
                        "dayVal_sat":"1",
                        "dayVal_sun":"1",
                        "dayTime":"1"
                        }
        self.removeAllProfiles()
        self.addProfile("Add_Rule")
        self.addSchedulerRule("Add_Rule", jdata_weekends)

    # case10: 添加非法的定时规则
    # EAP120/220/320有问题，可以添加
    def testAddSchedulerRuleWrong(self):
        jdata_wrong = {
                    "proName":"Add_Rule",
                    "weekDay": "3",
                    "dayVal_mon": "1",
                    "dayVal_tue": "1",
                    "dayVal_wed": "0",
                    "dayVal_thu": "1",
                    "dayVal_fri": "0",
                    "dayVal_sat": "1",
                    "dayVal_sun": "1",
                    "dayTime": "0",
                    "start_hour": "00",
                    "start_min": "01",
                    "end_hour": "25",
                    "end_min": "01"
                    }
        self.addSchedulerRule("Add_Rule", jdata_wrong, False)

    # case11: 在不存在的组添加定时规则
    def testAddSchedulerRuleInUnexistProfile(self):
        jdata_weekends = {
                        "proName": "Profile_Not_Exist",
                        "weekDay": "1",
                        "dayVal_sat": "1",
                        "dayVal_sun": "1",
                        "dayTime": "1"
                        }
        self.addSchedulerRule("Profile_Not_Exist", jdata_weekends, False)

    # 修改规则
    def updateSchedulerRule(self, index=0, profileName="", jdata={}, legal=True):
        oldData = self.getSchedulerRulesByName(profileName)["data"]
        if index>=0 and index<len(oldData):
            data = {
                    "operation": "update",
                    "key": oldData[index]["key"],
                    "index": index,
                    "old": oldData[index],
                    "new": json.dumps(jdata)
                    }
            res = self.s.post("http://%s/data/scheduler.rule.json" %(utils.ip), data, headers=utils.header_eap220)
            self.checkBasicResponse(res)
            if False==self.isProfileExist(profileName):
                # 目标组不存在
                if self.dutMode in {"EAP120", "EAP220"}:
                    self.assertEqual(res.json()["error"], -1)
                else:
                    self.assertEqual(res.content, "")
            else:
                if True==legal:
                    self.assertEqual(res.json()["success"], True)
                    self.assertEqual(res.json()["error"], 0)
                else:
                    # 非法规则
                    self.assertEqual(res.json()["error"], -1)

    # case12: 修改定时规则
    def testUpdateSchedulerRule(self):
        jdata_weekends = {
                        "proName":"Update_Rule",
                        "weekDay":"1",
                        "dayVal_sat":"1",
                        "dayVal_sun":"1",
                        "dayTime":"1"
                        }
        jdata_everyday = {
                        "proName":"Update_Rule",
                        "weekDay":"2",
                        "dayTime":"1"
                        }
        self.addProfile("Update_Rule")
        self.addSchedulerRule("Update_Rule", jdata_weekends)
        self.updateSchedulerRule(0, "Update_Rule", jdata_everyday)

    # case13: 修改成非法的定时规则
    # EAP120/220/320有问题，可以修改
    def testUpdateSchedulerRuleWrong(self):
        jdata_weekends = {
                        "proName":"Update_Rule",
                        "weekDay":"1",
                        "dayVal_sat":"1",
                        "dayVal_sun":"1",
                        "dayTime":"1"
                        }
        jdata_wrong =   {
                        "proName":"Update_Rule",
                        "weekDay": "3",
                        "dayVal_mon": "1",
                        "dayVal_tue": "1",
                        "dayVal_wed": "0",
                        "dayVal_thu": "1",
                        "dayVal_fri": "0",
                        "dayVal_sat": "1",
                        "dayVal_sun": "1",
                        "dayTime": "0",
                        "start_hour": "00",
                        "start_min": "01",
                        "end_hour": "25",
                        "end_min": "01"
                        }
        self.addSchedulerRule("Update_Rule", jdata_weekends)
        self.updateSchedulerRule(1, "Update_Rule", jdata_wrong, False)

    # case14: 修改不存在的定时规则
    def testUpdateSchedulerRuleNotExist(self):
        jdata_workdays = {
                        "proName":"Update_Rule",
                        "weekDay":"0",
                        "dayVal_mon":"1",
                        "dayVal_tue":"1",
                        "dayVal_wed":"1",
                        "dayVal_thu":"1",
                        "dayVal_fri":"1",
                        "dayVal_sat":"0",
                        "dayVal_sun":"0",
                        "dayTime":"1"
                        }
        self.updateSchedulerRule(8, "Update_Rule", jdata_workdays)

    # 删除定时规则
    def removeSchedulerRule(self, index=0, profileName=""):
        oldData = self.getSchedulerRulesByName(profileName)["data"]
        if index>=0 and index<len(oldData):
            data = {"operation": "remove", "key": oldData[index]["key"], "index": index}
            res = self.s.post("http://%s/data/scheduler.rule.json" %(utils.ip), data, headers=utils.header_eap220)
            self.assertEqual(res.json()["error"], 0)
        else:
            data = {"operation": "remove", "key": -1, "index": index}
            res = self.s.post("http://%s/data/scheduler.rule.json" %(utils.ip), data, headers=utils.header_eap220)
            if self.dutMode in {"EAP120", "EAP220"}:
                self.assertEqual(res.json()["error"], -1)
            else:
                self.assertEqual(res.content, "")

    # case15: 删除Mac规则
    def testRemoveSchedulerRule(self):
        jdata_everyday = {
                        "proName":"Remove_Rule",
                        "weekDay":"2",
                        "dayTime":"1"
                        }
        self.addProfile("Remove_Rule")
        self.addSchedulerRule("Remove_Rule", jdata_everyday)
        self.removeSchedulerRule(0, "Remove_Rule")

    # case16: 删除不存在的规则
    def testRemoveSchedulerRuleNotExist(self):
        self.removeSchedulerRule(8, "Remove_Rule")

    # case17: 重启是否保存
    def testZSchedulerReboot(self):
        jdata_everyday = {
                        "proName":"Reboot",
                        "weekDay":"2",
                        "dayTime":"1"
                        }
        self.addProfile("Reboot")
        self.addSchedulerRule("Reboot", jdata_everyday)
        self.s = self.reboot()
        self.assertTrue(self.isProfileExist("Reboot"))
        newData = self.getSchedulerRulesByName("Reboot")["data"]
        self.assertEqual(newData[0]["dayOpt"], "Daily")


# 定时过滤规则配置
class schedulerAssociation(schedulerProfilesBasic):

    # 保存配置(SSID模式)
    def saveSchedulerAssociation(self, allow=0):
        self.setSchedulerStatus("on", 0)
        oldData = self.getSchedulerAssociation()["data"]
        ssid = ""
        band = ""
        profile = ""
        action = ""
        for index in range(len(oldData)-1):
            ssid += (oldData[index]["ssid"] + "\n")
            band += (oldData[index]["band"] + "\n")
            profile += (oldData[index]["profileName"] + "\n")
            action += ("%d"%allow + "\n")
        ssid += oldData[len(oldData)-1]["ssid"]
        band += oldData[len(oldData)-1]["band"]
        profile += oldData[len(oldData)-1]["profileName"]
        action += "%d"%allow
        data = {
                "operation": "save",
                "ssid": ssid,
                "band": band,
                "profile": profile,
                "action": action
                }
        res = self.s.post("http://%s/data/scheduler.association.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        self.assertEqual(res.json()["error"], 0)

    # 保存配置(AP模式)
    def saveSchedulerAssociationAp(self, profileName):
        self.setSchedulerStatus("on", 1)
        oldData = self.getSchedulerAssociationAP()["data"][0]
        data = {
                "operation": "save",
                "ap": oldData["apName"],
                "mac": oldData["mac"],
                "profile": profileName,
                "action": "1",
                "type": "1"
                }
        res = self.s.post("http://%s/data/scheduler.associationAp.json" %(utils.ip), data, headers=utils.header_eap220)
        self.assertEqual(res.json()["error"], 0)
        self.assertEqual(res.json()["data"][0]["profileName"], profileName)

    # case18: 保存配置(SSID模式)
    def testSaveSchedulerAssociation(self):
        self.saveSchedulerAssociation(1)
        self.saveSchedulerAssociation()

    # case19: 保存配置(AP模式)
    def testSaveSchedulerAssociationAP(self):
        self.addProfile("AssociationAP")
        self.saveSchedulerAssociationAp("AssociationAP")


if __name__ == "__main__":
    unittest.main()
