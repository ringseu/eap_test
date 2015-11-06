#!/usr/bin/env python
# -*-coding:utf8-*-
#############################################################################################################
#
# File      ：   eap320Test.py
# Author    ：   chenqinbo
# Brief     ：   automatically run all testcases under current directory
# 
# Version   ：   1.0.0
# Date      ：   21 Aug 2015
# 
# History   ：  
#                1.0.0  chenqinbo  2015.08.21  create the file
#
#############################################################################################################


import unittest


if __name__ == "__main__":
    testsuite = unittest.TestLoader().discover(".")
    unittest.TextTestRunner(verbosity=1).run(testsuite)
