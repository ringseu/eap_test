#!/usr/bin/env python
# -*-coding:utf8-*-
#############################################################################################################
#
# File      ：   testCssStyle.py
# Author    ：   luliying
# Brief     ：   test if css files loaded or not
# 
# Version   ：   1.0.1
# Date      ：   10 Nov 2015
# 
# History   ：  
#                1.0.1  luliying  2015.11.10  finish
#                1.0.0  luliying  2015.11.10  create the file
#
#############################################################################################################


from utils import utils
import unittest
import requests


# 检查css文件是否已加载
class cssStyle(unittest.TestCase):

    # case1: 检查css文件是否已加载
    def testGetCss(self):
    	self.s = requests.session()
    	res = self.s.get("http://%s/css/widget.css"%(utils.ip))
    	self.assertEqual(res.status_code, 200)
    	res = self.s.get("http://%s/themes/dark/css/widget.css"%(utils.ip))
    	self.assertEqual(res.status_code, 200)
    	res = self.s.get("http://%s/themes/dark/css/style.css"%(utils.ip))
    	self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
