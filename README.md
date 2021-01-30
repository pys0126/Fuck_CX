# 去TM的学习通
**貌似仅支持CQCIVC学院**，目前的功能：过PPT任务，视频任务（16倍播放），捕获异常界面要求输入的验证码
# 前提需要
## 安装Python3和相关依赖
* 安装Python3
  - Windows和MacOS：https://www.python.org/downloads/release/python-379/
  - Linux自带
* 安装依赖：
  - 在命令行窗口运行`pip3 install -r requirements.txt`
## Chrome浏览器及Webdriver
* Chrome下载地址：https://www.google.cn/chrome/
* Webdriver下载地址：http://npm.taobao.org/mirrors/chromedriver/
## 下载Chrome网课扩展
* 下载地址：https://github.com/CodFrm/cxmooc-tools/releases （如何添加Chrome扩展自行百度）
## 脚本设置
* 在脚本173行设置Chrome个人资料路径（在Chrome访问chrome://version/找到个人资料路径）
* 在脚本174行设置webdriver_path
## Cookie（用于requests）
获取cookie：
* 1.访问：http://mooc1-1.chaoxing.com/visit/interaction
* 2.登陆后按F12点击Network刷新页面
* 3.点击XHR，点击workTestPendingNew
* 4.将Cookie项的值全部复制下来
## 手机号或用户名和密码（用于selenium）
* 按脚本提示输入即可
# 可能会实现的功能
* 1.不需要Cookie（只利用selenium，效率可能会降低）
* 2.答题（再说吧...）
