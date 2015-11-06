#!/usr/bin/env python
# -*-coding:utf8-*-
#############################################################################################################
#
# File      ：   testMacFilter.py
# Author    ：   luliying
# Brief     ：   test wireless Mac filter
# 
# Version   ：   1.0.1
# Date      ：   2 Nov 2015
# 
# History   ：   
#                1.0.1  luliying  2015.11.02  finish
#                1.0.0  luliying  2015.11.02  create the file
#
#############################################################################################################


from utils import utils
import json


class MacFilterBasic(utils.EAPLoginSession):

	# 登录
    @classmethod
    def setUpClass(cls):
        super(MacFilterBasic, cls).setUpClass()  # 单继承情况下，似乎不用管

    # 检查响应是否正确
    def checkBasicResponse(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["success"], True)

    # 获取Mac过滤状态
    def getMacFilterStatus(self):
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/macFiltering.set.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取Mac过滤组
    def getMacGroups(self):
        data = {"operation": "load"}
        res = self.s.post("http://%s/data/macFiltering.maclist.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取Mac过滤规则
    def getMacRules(self):
        data = {"operation": "load"}
        res = self.s.post("http://%s/data/macFiltering.rule.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取某个Mac组的过滤规则
    def getMacRulesByName(self, listName):
        data = {"operation": "load", "listName": listName}
        res = self.s.post("http://%s/data/macFiltering.rule.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取Mac过滤配置
    def getMacFilterAssociation(self):
        data = {"operation": "load"}
        res = self.s.post("http://%s/data/macFiltering.association.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 设置Mac过滤状态
    def setMacFilterStatus(self, status="off"):
        data = {"operation": "write", "status": status}
        res = self.s.post("http://%s/data/macFiltering.set.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        self.assertEqual(res.json()["data"]["status"], status)

    # 判断组是否存在
    def isGroupExist(self, groupName):
        groups = self.getMacGroups()["data"]
        for group in groups:
            if groupName==group["listName"]:
                return True
        return False

    # 按名字查找Mac组
    def getMacGroupByName(self, groupName):
        groups = self.getMacGroups()["data"]
        for group in groups:
            if groupName==group["listName"]:
                return group


# 测试Mac过滤基本设置
class getMacFilterBasic(MacFilterBasic):

    # case1: 获取Mac过滤设置
    def testGetMacFilterConfig(self):
        self.getMacFilterStatus()
        self.getMacGroups()
        self.getMacRules()
        self.getMacFilterAssociation()

    # case2: 开启关闭Mac过滤
    def testSetMacFilterStatus(self):
        self.setMacFilterStatus()
        self.setMacFilterStatus("on")


# Mac组
class MacFilterGroupsBasic(MacFilterBasic):

    # 添加Mac组
    def addMacGroup(self, groupName):
        groups = self.getMacGroups()["data"]
        if len(groups)>=7:
            # Mac组太多就先删掉
            self.removeMacGroup(0)
        jdata = {"maclistName": groupName}
        data = {
                "operation": "insert",
                "key": "add",
                "index": "0",
                "old": "add",
                "new": json.dumps(jdata)
                }
        if True==self.isGroupExist(groupName):
            res = self.s.post("http://%s/data/macFiltering.maclist.json" %(utils.ip), data, headers=utils.header_eap220)
            self.checkBasicResponse(res)
            if self.dutMode in {"EAP120", "EAP220"}:
                self.assertEqual(res.json()["error"], -1)
            else:
                # EAP320不返回错误，但不添加重名组
                pass
        else:
            res = self.s.post("http://%s/data/macFiltering.maclist.json" %(utils.ip), data, headers=utils.header_eap220)
            self.checkBasicResponse(res)
            self.assertTrue(self.isGroupExist(groupName))

    # 修改Mac组
    def updateMacGroup(self, index=0, groupName=""):
        oldData = self.getMacGroups()["data"][index]
        jdata = {"listName": oldData["listName"], "key": oldData["key"]}
        newJdata = {"maclistName": groupName}
        data = {
                "operation": "update",
                "index": index,
                "key": oldData["key"],
                "old": json.dumps(jdata),
                "new": json.dumps(newJdata)
                }
        if True==self.isGroupExist(groupName):
            res = self.s.post("http://%s/data/macFiltering.maclist.json" %(utils.ip), data, headers=utils.header_eap220)
            self.checkBasicResponse(res)
            if self.dutMode in {"EAP120", "EAP220"}:
                self.assertEqual(res.json()["error"], -1)
            else:
                # EAP320不返回错误，但不添加重名组
                pass
        else:
            res = self.s.post("http://%s/data/macFiltering.maclist.json" %(utils.ip), data, headers=utils.header_eap220)
            self.checkBasicResponse(res)
            self.assertTrue(self.isGroupExist(groupName))

    # 删除Mac组
    def removeMacGroup(self, index=0):
        oldData = self.getMacGroups()["data"]
        if index>=0 and index<len(oldData):
            data = {"operation": "remove", "key": oldData[index]["key"], "index": index}
            res = self.s.post("http://%s/data/macFiltering.maclist.json" %(utils.ip), data, headers=utils.header_eap220)
            self.assertEqual(res.json()["success"], True)
        else:
            data = {"operation": "remove", "key": -1, "index": index}
            res = self.s.post("http://%s/data/macFiltering.maclist.json" %(utils.ip), data, headers=utils.header_eap220)
            if self.dutMode in {"EAP120", "EAP220"}:
                self.assertEqual(res.json()["error"], -1)
            else:
                # EAP320不返回错误，但删除任何组
                pass

    # 清空Mac组
    def removeAllMacGroups(self):
        groups = self.getMacGroups()["data"]
        for group in groups:
            data = {"operation": "remove", "key": group["key"], "index": 0}
            res = self.s.post("http://%s/data/macFiltering.maclist.json" %(utils.ip), data, headers=utils.header_eap220)
        groups = self.getMacGroups()["data"]
        self.assertEqual(len(groups), 0)


# 测试Mac组
class MacFilterGroups(MacFilterGroupsBasic):

    # case3: 添加Mac组
    def testAddMacGroup(self):
        self.removeAllMacGroups()
        self.addMacGroup("Add_Group_1")

    # case4: 添加重名Mac组
    def testAddMacGroupExist(self):
        self.addMacGroup("Group_Exist_1")
        self.addMacGroup("Group_Exist_1")

    # case5: 修改Mac组
    def testUpdateMacGroup(self):
        self.addMacGroup("Group_Before_Change")
        self.updateMacGroup(0, "Group_After_Change")

    # case6: 修改重名Mac组
    # EAP120/220有问题，可以修改
    def testUpdateMacGroupExist(self):
        self.addMacGroup("Group_Hold_Position")
        self.addMacGroup("Group_Change_Exist")
        self.updateMacGroup(0, "Group_Change_Exist")

    # case7: 删除Mac组
    def testRemoveMacGroup(self):
        self.addMacGroup("Group_Remove")
        self.removeMacGroup(0)

    # case8: 删除不存在的Mac组
    def testRemoveMacGroupNotExist(self):
        self.removeMacGroup(8)


# Mac组规则
class MacFilterRules(MacFilterGroupsBasic):

    # 判断Mac规则是否存在
    def isMacRuleExist(self, listName, mac_addr):
        rules = self.getMacRulesByName(listName)["data"]
        for rule in rules:
            if mac_addr==rule["mac"]:
                return True
        return False

    # 添加Mac规则(只能往已经存在的Mac组里添加)
    def addMacRule(self, listName="", mac_addr="", legal=True):
        jdata = {"listName": listName, "mac_addr": mac_addr}
        data = {
                "operation": "insert",
                "key": "add",
                "index": "0",
                "old": "add",
                "new": json.dumps(jdata)
                }
        ruleExist = self.isMacRuleExist(listName, mac_addr)
        res = self.s.post("http://%s/data/macFiltering.rule.json" %(utils.ip), data, headers=utils.header_eap220)
        if False==self.isGroupExist(listName):
            # Mac组不存在
            if self.dutMode in {"EAP120", "EAP220"}:
                self.assertEqual(res.json()["error"], -1)
            else:
                self.assertEqual(res.content, "")
        else:
            if True==legal:
                if True==ruleExist:
                    # Mac规则已存在
                    if self.dutMode in {"EAP120", "EAP220"}:
                        self.assertEqual(res.json()["error"], -1)
                    else:
                        pass
                else:
                    self.assertEqual(res.json()["error"], 0)
                    rules = self.getMacRulesByName(listName)
                    self.assertTrue(self.isMacRuleExist(listName, mac_addr))
            else:
                # Mac地址非法
                rules = self.getMacRulesByName(listName)
                self.assertFalse(self.isMacRuleExist(listName, mac_addr))

    # case10: 添加Mac规则
    def testAddMacRule(self):
        self.removeAllMacGroups()
        self.addMacGroup("Add_Rule")
        self.addMacRule("Add_Rule", "AA-AA-AA-AA-AA-AA")

    # case11: 添加非法的Mac规则(多播地址)
    # EAP120/220/330有问题，可以添加
    def testAddMacRuleWrong(self):
        self.addMacRule("Add_Rule", "99-99-99-99-99-99", False)

    # case12: 添加重复的Mac规则
    def testAddMacRuleExist(self):
        self.addMacGroup("Rule_Exist")
        self.addMacRule("Rule_Exist", "AA-AA-AA-AA-AA-AA")
        self.addMacRule("Rule_Exist", "AA-AA-AA-AA-AA-AA")

    # case13: 在不存在的Mac组添加Mac规则
    def testAddMacRuleInUnexistGroup(self):
        self.addMacRule("Group_Not_Exist", "AA-AA-AA-AA-AA-AA")

    # 修改Mac规则
    def updateMacRule(self, index=0, listName="", mac_addr="", legal=True):
        oldData = self.getMacRulesByName(listName)["data"]
        if index>=0 and index<len(oldData):
            jdata = {"mac": oldData[index]["mac"], "key": oldData[index]["key"]}
            ruleKey = oldData[index]["key"]
        else:
            jdata = {"mac": "22-22-22-22-22-22", "key": -1}
            ruleKey = -1
        newJdata = {"listName": listName, "mac_addr": mac_addr}
        data = {
                "operation": "update",
                "index": index,
                "key": ruleKey,
                "old": json.dumps(jdata),
                "new": json.dumps(newJdata)
                }
        res = self.s.post("http://%s/data/macFiltering.rule.json" %(utils.ip), data, headers=utils.header_eap220)
        if False==self.isGroupExist(listName):
            if self.dutMode in {"EAP120", "EAP220"}:
                self.assertEqual(res.json()["error"], -1)
            else:
                self.assertEqual(res.content, "")
        elif index>len(oldData):
            if self.dutMode in {"EAP120", "EAP220"}:
                self.assertEqual(res.json()["error"], -1)
            else:
                pass
        else:
            if True==legal:
                self.assertEqual(res.json()["error"], 0)
                self.assertTrue(self.isMacRuleExist(listName, mac_addr))
            else:
                # Mac地址非法
                self.assertFalse(self.isMacRuleExist(listName, mac_addr))

    # case14: 修改Mac规则
    def testUpdateMacRule(self):
        self.addMacGroup("Update_Rule")
        self.addMacRule("Update_Rule", "22-22-22-22-22-22")
        self.updateMacRule(0, "Update_Rule", "66-66-66-66-66-66")

    # case15: 修改成非法的Mac规则
    # EAP120/220/320有问题，可以修改
    def testUpdateMacRuleWrong(self):
        self.addMacRule("Update_Rule", "22-22-22-22-22-22")
        self.updateMacRule(1, "Update_Rule", "99-99-99-99-99-99", False)

    # case16: 修改不存在的Mac规则
    def testUpdateMacRuleNotExist(self):
        self.updateMacRule(0, "Update_Rule_Not_Exist", "88-88-88-88-88-88")
        self.updateMacRule(8, "Update_Rule", "88-88-88-88-88-88")

    # 删除Mac规则
    def removeMacRule(self, index=0, listName=""):
        oldData = self.getMacRulesByName(listName)["data"]
        if index>=0 and index<len(oldData):
            data = {"operation": "remove", "key": oldData[index]["key"], "index": index}
            res = self.s.post("http://%s/data/macFiltering.rule.json" %(utils.ip), data, headers=utils.header_eap220)
            self.assertEqual(res.json()["error"], 0)
        else:
            data = {"operation": "remove", "key": -1, "index": index}
            res = self.s.post("http://%s/data/macFiltering.rule.json" %(utils.ip), data, headers=utils.header_eap220)
            if self.dutMode in {"EAP120", "EAP220"}:
                self.assertEqual(res.json()["error"], -1)
            else:
                pass

    # case17: 删除Mac规则
    def testRemoveMacRule(self):
        self.addMacGroup("Remove_Rule")
        self.addMacRule("Remove_Rule", "22-22-22-22-22-22")
        self.removeMacRule(0, "Remove_Rule")

    # case18: 删除不存在的规则
    def testRemoveMacRuleNotExist(self):
        self.removeMacRule(8, "Remove_Rule")

    # case19: 重启是否保存
    def testZMacFilterReboot(self):
        self.addMacGroup("Reboot")
        self.addMacRule("Reboot", "66-66-66-66-66-66")
        self.s = self.reboot()
        self.assertTrue(self.isGroupExist("Reboot"))
        self.assertTrue(self.isMacRuleExist("Reboot", "66-66-66-66-66-66"))


# Mac过滤规则配置
class MacFilterAssociation(MacFilterGroupsBasic):

    # 保存配置
    def saveMacFilterAssociation(self, allow=0):
        oldData = self.getMacFilterAssociation()["data"]
        ssidName = ""
        band = ""
        listName = ""
        action = ""
        for association in oldData:
            ssidName += (association["ssid"] + "\n")
            band += (association["band"] + "\n")
            listName += (association["maclist"] + "\n")
            action += ("%d"%allow + "\n")
        data = {
                "operation": "save",
                "ssidName": ssidName,
                "band": band,
                "listName": listName,
                "action": action
                }
        res = self.s.post("http://%s/data/macFiltering.association.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)

    # case20: 保存配置
    def testSaveMacFilterAssociation(self):
        self.saveMacFilterAssociation(1)
        self.saveMacFilterAssociation()


if __name__ == "__main__":
    unittest.main()
