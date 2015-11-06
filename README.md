一、概述
	本测试工程是以python unittest框架为基础，模拟浏览器和DUT之间的json交互过程的一套网页配置自动化测试工程
	由于json交互中包含重启的json，所以这一套也可以自动测试系统保存配置功能

二、运行
1. 	工具安装要求
	python, python requests模块

2. 	先手动修改DUT的IP地址(静态)，再修改utils/utils.py文件里边的用户名、密码和IP

3. 	由于登录是所有测试的基础，因此先测试登录过程是否正确
	$ python -m unittest login.testLogin
	若希望显示详细信息：
	$ python -m unittest -v login.testLogin

4. 	如果登录测试通过，那么可以测试其他所有的测试项
	$ python eap320Test.py

5. 	测试中会产生很多Fail信息，一般在浏览器中操作并不会暴露这些错误

6	少量出现的Error信息属于严重隐患

7	如果重启后马上出现Error，就在utils.py的reboot函数中将time.sleep()的时间改长一些
