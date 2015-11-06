#!/usr/bin/env python
# -*-coding:utf8-*-
#############################################################################################################
#
# File      ：   testTimeSetting.py
# Author    ：   luliying
# Brief     ：   test time setting
# 
# Version   ：   1.1.0
# Date      ：   22 Oct 2015
# 
# History   ：   
#                1.1.0  luliying   2015.10.26  add reboot testcases (2 cases)
#                                  2015.10.22  finish all testcases for time setting function, find 5 bugs
#                1.0.1  luliying   2015.10.22  reorganize class timeDate and timeTime (add parameter "legal")
#                                              add timeDayLightSaving testcases
#                                              add timeNTPServer testcases (3 failed)
#                                  2015.10.21  add 6 timetime testcases
#                                              add 3 timezone testcases (1800 and -1200 and 1800000 minutes)
#                1.0.0  chenqinbo  2015.08.21  create the file
#
#############################################################################################################


from utils import utils


class timeBasic(utils.EAPLoginSession):

    # 登录
    @classmethod
    def setUpClass(cls):
        super(timeBasic, cls).setUpClass()  # 单继承情况下，似乎不用管

    # 检查响应是否正确
    def checkBasicResponse(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["success"], True)

    # 获取时间
    def getTimeBasicSetting(self):
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/time.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()

    # 获取夏令时
    def getDSTBasicSetting(self):
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/daylightTime.json" %(utils.ip), data, headers=utils.header_eap220)
        self.checkBasicResponse(res)
        return res.json()


# 测试时间获取
class timeBasicConfig(timeBasic):

    # case1: 获取时间
    def testGetTimeBasicSetting(self):
        self.getTimeBasicSetting()
        self.getDSTBasicSetting()


# 测试时区
class timeTimeZone(timeBasic):

    # 设置时差(以-12时区为基准，单位分钟，合法值为0~1500范围内60的倍数)
    # 此处有小问题，服务器不拒绝非法值，写入后找不到列表项(虽然全都能计算出正确时间)，见case4 ~ case7
    def setTimeZone(self, timezone):
        if timezone>=0 and timezone<=1500:
            legal = True
        else:
            legal = False
        jsondata = self.getTimeBasicSetting()
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/time.json" %(utils.ip), data, headers=utils.header_eap220)
        data = {
                "operation": "write",
                "isTimeChanged": 0,
                "ntp1": jsondata["data"]["ntp1"],
                "ntp2": jsondata["data"]["ntp2"],
                "date": jsondata["data"]["date"],
                "time": jsondata["data"]["time"],
                "timezone": timezone
                }
        res = self.s.post("http://%s/data/time.json" %(utils.ip), data, headers=utils.header_eap220)
        if True==legal:
            self.checkBasicResponse(res)
            self.assertEqual(res.json()["data"]["timezone"], timezone)
        else:
            self.assertEqual(res.json()["success"], False)

    # case2: 时差0分钟
    def testSetTimeZoneMin(self):
        self.setTimeZone(0)

    # case3: 时差1500分钟
    def testSetTimeZoneMax(self):
        self.setTimeZone(1500)

    # case4: 时差720分钟
    def testSetTimeZone720(self):
        self.setTimeZone(720)

    # case5: 时差1800分钟(越界)
    # EAP120/220/330有问题，可以写入(不影响时间走动)
    def testSetTimeZoneBig(self):
        self.setTimeZone(1800)

    # case6: 时差-1200分钟(负数)
    # EAP120/220/330有问题，可以写入(不影响时间走动)
    def testSetTimeZoneMinus(self):
        self.setTimeZone(-1200)

    # case7: 时差1800000分钟(超大数字)
    # EAP120/220/330有问题，可以写入(不影响时间走动)
    def testSetTimeZoneVeryVeryBig(self):
        self.setTimeZone(1800000)


# 测试日期
class timeDate(timeBasic):

    # 设置合法日期，其中参数legal为True表示合法值，为False表示非法值
    def setDate(self, date, legal=True):
        jsondata = self.getTimeBasicSetting()
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/time.json" %(utils.ip), data, headers=utils.header_eap220)
        data = {
                "operation": "write",
                "isTimeChanged": 1,
                "ntp1": jsondata["data"]["ntp1"],
                "ntp2": jsondata["data"]["ntp2"],
                "date": date,
                "time": jsondata["data"]["time"],
                "timezone": jsondata["data"]["timezone"]
                }
        res = self.s.post("http://%s/data/time.json" %(utils.ip), data, headers=utils.header_eap220)
        if True==legal:
            self.checkBasicResponse(res)
            self.assertEqual(res.json()["data"]["date"], date)
        else:
            self.assertEqual(res.json()["success"], False)

    # case8: 最小合法日期
    def testSetDateMin(self):
        if self.dutMode in {"EAP320", "EAP330"}:
            self.setDate("01/01/2000")
        else:
            self.setDate("01/01/1980")

    # case9: 最大合法日期
    def testSetDateMax(self):
        if self.dutMode in {"EAP320"}:
            self.setDate("12/31/2037")
        else:
            self.setDate("12/31/2030")

    # case10: 正常日期
    def testSetDateNormal(self):
        self.setDate("10/31/2015")

    # case11: 日期过小
    # EAP120/220有问题
    def testSetDateTooSamll(self):
        if self.dutMode in {"EAP320", "EAP330"}:
            self.setDate("12/31/1999", False)
        else:
            self.setDate("12/31/1979", False)

    # case12: 日期过大
    # EAP120/220/330有问题，可以写入
    def testSetDateTooBig(self):
        if self.dutMode in {"EAP320"}:
            self.setDate("01/01/2038", False)
        else:
            self.setDate("01/01/2031", False)


# 测试时间
class timeTime(timeBasic):

    # 设置时间，其中参数legal为True表示合法值，为False表示非法值
    def setTime(self, settime, legal=True):
        jsondata = self.getTimeBasicSetting()
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/time.json" %(utils.ip), data, headers=utils.header_eap220)
        data = {
                "operation": "write",
                "isTimeChanged": 1,
                "ntp1": jsondata["data"]["ntp1"],
                "ntp2": jsondata["data"]["ntp2"],
                "date": jsondata["data"]["date"],
                "time": settime,
                "timezone": jsondata["data"]["timezone"]
                }
        res = self.s.post("http://%s/data/time.json" %(utils.ip), data, headers=utils.header_eap220)
        if True==legal:
            self.checkBasicResponse(res)
            self.assertEqual(res.json()["data"]["time"], settime)
        else:
            self.assertEqual(res.json()["success"], False)

    # case13: 普通时间
    def testSetTimeNormal(self):
        self.setTime("10:11:12")

    # case14: 最小时间
    def testSetTimeMin(self):
        self.setTime("00:00:00")

    # case15: 最大时间
    def testSetTimeMax(self):
        self.setTime("23:59:59")

    # case16: 小时数错误
    # EAP120/220有问题
    def testSetTimeWrongHour(self):
        self.setTime("24:00:00", False)

    # case17: 分钟数错误
    # EAP120/220有问题
    def testSetTimeWrongMinute(self):
        self.setTime("23:60:00", False)

    # case18: 秒数错误
    # EAP120/220有问题
    def testSetTimeWrongSecond(self):
        self.setTime("23:00:60", False)


# 测试时间服务器
class timeNTPServer(timeBasic):

    # 设置NTP服务器(不能以0或127开头，不能是D、E类地址)
    # 此处有小问题，服务器不拒绝非法输入(前端会检查)，见case22 ~ case24
    def setNTPServer(self, ntp1 = "", ntp2 = "", legal = True):
        jsondata = self.getTimeBasicSetting()
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/time.json" %(utils.ip), data, headers=utils.header_eap220)
        data = {
                "operation": "write",
                "isTimeChanged": 0,
                "ntp1": ntp1,
                "ntp2": ntp2,
                "date": jsondata["data"]["date"],
                "time": jsondata["data"]["time"],
                "timezone": jsondata["data"]["timezone"]
                }
        res = self.s.post("http://%s/data/time.json" %(utils.ip), data, headers=utils.header_eap220)
        if True==legal:
            self.checkBasicResponse(res)
            self.assertEqual(res.json()["data"]["ntp1"], ntp1)
            self.assertEqual(res.json()["data"]["ntp2"], ntp2)
        else:
            self.assertEqual(res.json()["success"], False)

    # case19: 
    def testNTP1(self):
        self.setNTPServer(ntp1="1.0.0.0")

    # case20: 
    def testNTP2(self):
        self.setNTPServer(ntp2="239.255.255.255")

    # case21: 
    def testNTP1and2(self):
        self.setNTPServer("10.1.1.1", "192.168.1.1")

    # case22: 
    # EAP120/220/330有问题，可以写入
    def testNTPWrong1(self):
        self.setNTPServer(ntp1="0.0.0.1", legal=False)

    # case23: 
    # EAP120/220/330有问题，可以写入
    def testNTPWrong2(self):
        self.setNTPServer(ntp2="127.1.1.1", legal=False)

    # case24: 
    # EAP120/220/330有问题，可以写入
    def testNTPWrong1And2(self):
        self.setNTPServer("240.0.0.1", "254.254.254.254", False)

    # 获取NTP时间(因为无法连上真实的NTP服务器，只检查errCode)
    def getNTPTime(self):
        jsondata = self.getTimeBasicSetting()
        data = {
                "operation": "gmt",
                "isTimeChanged": 0,
                "ntp1": jsondata["data"]["ntp1"],
                "ntp2": jsondata["data"]["ntp2"],
                "date": jsondata["data"]["date"],
                "time": jsondata["data"]["time"],
                "timezone": jsondata["data"]["timezone"]
                }
        res = self.s.post("http://%s/data/time.json" %(utils.ip), data, headers=utils.header_eap220)
        self.assertEqual(res.status_code, 200)
        if self.dutMode in {"EAP320"}:
            self.assertEqual(res.json()["data"]["errCode"], 0)

    # case25: 获取NTP时间
    def testGetNTPTime(self):
        self.getNTPTime()

    # case26: 重启后保存时区和NTP配置
    def testZTimeAndNTPReboot(self):
        timeBeforeReboot = self.getTimeBasicSetting()
        #print "time setting before reboot:\n",timeBeforeReboot
        self.s = self.reboot()
        timeAfterReboot = self.getTimeBasicSetting()
        #print "time setting after reboot:\n",timeAfterReboot
        self.assertEqual(timeBeforeReboot["data"]["timezone"], timeAfterReboot["data"]["timezone"])
        self.assertEqual(timeBeforeReboot["data"]["ntp1"], timeAfterReboot["data"]["ntp1"])
        self.assertEqual(timeBeforeReboot["data"]["ntp2"], timeAfterReboot["data"]["ntp2"])


# 测试夏令时
class timeDST(timeBasic):

    # 关闭夏令时
    def closeDSTMode(self):
        jsondata = self.getDSTBasicSetting()
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/daylightTime.json" %(utils.ip), data, headers=utils.header_eap220)
        data = {
                "operation": "write",
                "dstStatus": "false",
                }
        res = self.s.post("http://%s/data/daylightTime.json" %(utils.ip), data, headers=utils.header_eap220)
        self.assertEqual(res.json()["success"], True)
        self.assertEqual(res.json()["data"]["dstStatus"], False)

    # case27: 关闭夏令时
    def testCloseDSTMode(self):
        self.closeDSTMode()

    # 夏令时预置国家模式(只能为0~3)
    def setDSTPredefined(self, modeCountry):
        jsondata = self.getDSTBasicSetting()
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/daylightTime.json" %(utils.ip), data, headers=utils.header_eap220)
        data = {
                "operation": "write",
                "dstStatus": "true",
                "dstMode": "0",
                "modeCountry": modeCountry
                }
        res = self.s.post("http://%s/data/daylightTime.json" %(utils.ip), data, headers=utils.header_eap220)
        if modeCountry>=0 and modeCountry<=3:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["data"]["dstStatus"], True)
            self.assertEqual(res.json()["data"]["dstMode"], 0)
            self.assertEqual(res.json()["data"]["modeCountry"], modeCountry)
        else:
            self.assertEqual(res.json()["success"], False)

    # case28: 正常值
    def testSetDSTPre(self):
        self.setDSTPredefined(0)
        self.setDSTPredefined(3)

    # case29: 非法值
    # EAP120/220有问题
    def testSetDSTPreWrongCountry(self):
        self.setDSTPredefined(4)

    # 夏令时星期模式
    def setDSTRecurring(self, recurringTimeOffset=60, startCount=5, startWeekday=0, startMonth=3, \
        startHour=1, startMin=0, endCount=2, endWeekday=0, endMonth=10, endHour=1, endMin=0, legal=True):
        jsondata = self.getDSTBasicSetting()
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/daylightTime.json" %(utils.ip), data, headers=utils.header_eap220)
        data = {
                "operation": "write",
                "dstStatus": "true",
                "dstMode": "1",
                "recurringTimeOffset": recurringTimeOffset,
                "startCount": startCount,
                "startWeekday": startWeekday,
                "startMonth": startMonth,
                "startHour": startHour,
                "startMin": startMin,
                "endCount": endCount,
                "endWeekday": endWeekday,
                "endMonth": endMonth,
                "endHour": endHour,
                "endMin": endMin
                }
        res = self.s.post("http://%s/data/daylightTime.json" %(utils.ip), data, headers=utils.header_eap220)
        if True==legal:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["data"]["recurringTimeOffset"], recurringTimeOffset)
            self.assertEqual(res.json()["data"]["startCount"], startCount)
            self.assertEqual(res.json()["data"]["startWeekday"], startWeekday)
            self.assertEqual(res.json()["data"]["startMonth"], startMonth)
            self.assertEqual(res.json()["data"]["startHour"], startHour)
            self.assertEqual(res.json()["data"]["startMin"], startMin)
            self.assertEqual(res.json()["data"]["endCount"], endCount)
            self.assertEqual(res.json()["data"]["endWeekday"], endWeekday)
            self.assertEqual(res.json()["data"]["endMonth"], endMonth)
            self.assertEqual(res.json()["data"]["endHour"], endHour)
            self.assertEqual(res.json()["data"]["endMin"], endMin)
        else:
            self.assertEqual(res.json()["success"], False)

    # case30: 正确设置，边界值
    def testDSTRecurringRight(self):
        self.setDSTRecurring(1, 1, 0, 1, 0, 0, 5, 6, 12, 23, 59)
        self.setDSTRecurring(180, 1, 0, 1, 0, 0, 5, 6, 12, 23, 59)

    # case31: 错误设置，数值越界
    # EAP120/220/320/330此处有小问题，可以写入
    def testDSTRecurringOverflow(self):
        self.setDSTRecurring(181, 1, 0, 1, 0, 0, 5, 6, 12, 23, 59, False)

    # case32: 错误设置，开始日期在结束日期之后
    # EAP120/220/320/330此处有小问题，可以写入
    def testDSTRecurringOverlap(self):
        self.setDSTRecurring(60, 5, 6, 12, 23, 59, 1, 0, 1, 0, 0, False)

    # 夏令时日期模式
    def setDSTDate(self, dateTimeOffset=60, startDateYear=2015, startDateMonth=3, startDateDay=1, \
        startDateHour=1, startDateMin=0, endDateYear=2015, endDateMonth=10, endDateDay=1, \
        endDateHour=1, endDateMin=0, legal=True):
        jsondata = self.getDSTBasicSetting()
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/daylightTime.json" %(utils.ip), data, headers=utils.header_eap220)
        data = {
                "operation": "write",
                "dstStatus": "true",
                "dstMode": "2",
                "dateTimeOffset": dateTimeOffset,
                "startDateYear": startDateYear,
                "startDateMonth": startDateMonth,
                "startDateDay": startDateDay,
                "startDateHour": startDateHour,
                "startDateMin": startDateMin,
                "endDateYear": endDateYear,
                "endDateMonth": endDateMonth,
                "endDateDay": endDateDay,
                "endDateHour": endDateHour,
                "endDateMin": endDateMin
                }
        res = self.s.post("http://%s/data/daylightTime.json" %(utils.ip), data, headers=utils.header_eap220)
        if True==legal:
            self.assertEqual(res.json()["success"], True)
            self.assertEqual(res.json()["data"]["dateTimeOffset"], dateTimeOffset)
            self.assertEqual(res.json()["data"]["startDateYear"], startDateYear)
            self.assertEqual(res.json()["data"]["startDateMonth"], startDateMonth)
            self.assertEqual(res.json()["data"]["startDateDay"], startDateDay)
            self.assertEqual(res.json()["data"]["startDateHour"], startDateHour)
            self.assertEqual(res.json()["data"]["startDateMin"], startDateMin)
            self.assertEqual(res.json()["data"]["endDateYear"], endDateYear)
            self.assertEqual(res.json()["data"]["endDateMonth"], endDateMonth)
            self.assertEqual(res.json()["data"]["endDateDay"], endDateDay)
            self.assertEqual(res.json()["data"]["endDateHour"], endDateHour)
            self.assertEqual(res.json()["data"]["endDateMin"], endDateMin)
        else:
            self.assertEqual(res.json()["success"], False)

    # case33: 正确设置，边界值
    def testDSTDateRight(self):
        self.setDSTDate(1, 2014, 1, 1, 0, 0, 2037, 12, 31, 23, 59)
        self.setDSTDate(180, 2014, 1, 1, 0, 0, 2037, 12, 31, 23, 59)

    # case34: 错误设置，数值越界
    # EAP120/220/320/330此处有问题，可以写入
    def testDSTDateOverflow(self):
        self.setDSTDate(1, 2013, 1, 1, 0, 0, 2037, 12, 31, 23, 59, False)

    # case35: 错误设置，日期错误(2月29日)
    # EAP120/220有问题
    def testDSTDateWrongDay(self):
        self.setDSTDate(1, 2015, 2, 29, 0, 0, 2037, 12, 31, 23, 59, False)

    # case36: 错误设置，开始日期在结束日期之后
    # EAP120/220有问题
    def testDSTDateOverlap(self):
        self.setDSTDate(60, 2037, 12, 31, 23, 59, 2014, 1, 1, 0, 0, False)

    # 设置错误模式
    def setDSTWrongMode(self, wrongMode):
        jsondata = self.getDSTBasicSetting()
        data = {"operation": "read"}
        res = self.s.post("http://%s/data/daylightTime.json" %(utils.ip), data, headers=utils.header_eap220)
        data = {
                "operation": "write",
                "dstStatus": "true",
                "dstMode": wrongMode
                }
        res = self.s.post("http://%s/data/daylightTime.json" %(utils.ip), data, headers=utils.header_eap220)
        self.assertEqual(res.json()["success"], True)
        self.assertEqual(res.json()["data"]["dstStatus"], False)

    # case37: 设置错误模式，EAP320服务器会关闭夏令时功能
    # EAP120/220有问题
    def testDSTWrongMode(self):
        self.setDSTWrongMode(3)

    # case38: 重启后保存配置(抽样检查)
    def testZDSTReboot(self):
        DSTBeforeReboot = self.getDSTBasicSetting()["data"]
        self.s = self.reboot()
        DSTAfterReboot = self.getDSTBasicSetting()["data"]
        if True==DSTBeforeReboot["dstStatus"]:
            self.assertEqual(DSTBeforeReboot["dstStatus"], DSTAfterReboot["dstStatus"])
            self.assertEqual(DSTBeforeReboot["dstMode"], DSTAfterReboot["dstMode"])
            if 0==DSTBeforeReboot["dstMode"]:
                self.assertEqual(DSTBeforeReboot["modeCountry"], DSTAfterReboot["modeCountry"])
            elif 1==DSTBeforeReboot["dstMode"]:
                self.assertEqual(DSTBeforeReboot["recurringTimeOffset"], DSTAfterReboot["recurringTimeOffset"])
                self.assertEqual(DSTBeforeReboot["endWeekday"], DSTAfterReboot["endWeekday"])
            else:
                self.assertEqual(DSTBeforeReboot["dateTimeOffset"], DSTAfterReboot["dateTimeOffset"])
                self.assertEqual(DSTBeforeReboot["endDateHour"], DSTAfterReboot["endDateHour"])
        else:
            self.assertEqual(DSTBeforeReboot["dstStatus"], DSTAfterReboot["dstStatus"])


if __name__ == "__main__":
    unittest.main()
