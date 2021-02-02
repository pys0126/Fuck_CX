# 去TM的学习通
**仅支持CQCIVC学院**，目前的功能：过PPT任务，视频任务（16倍播放需自己设置网课扩展），捕获异常界面要求输入的验证码
下载：[点击这里](https://github.com/pys0126/Fuck_CX/archive/main.zip)
# 前提需要
## 安装Python3和相关依赖
* 安装Python3
  - Windows下载地址：https://www.python.org/downloads/release/python-379/
* 安装依赖：
  - 在命令行窗口运行`pip3 install -r requirements.txt`
## 下载Edge浏览器的webdriver
* 在Edge浏览器输入edge://version/查看版本，然后下载**对应版本的Webdriver**
* Webdriver下载地址：https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
## 下载网课扩展
* 下载地址：https://github.com/CodFrm/cxmooc-tools/releases/download/v2.5.0/cxmooc-tools.zip （如何添加edge扩展自行百度）
## 运行脚本
* 1、在脚本12行-14行设置好Webdriver路径，手机号，密码
* 2、在脚本路径下按住Shift+鼠标右键打开PowerShell，运行`python '.\fuck_cx(requests+selenium).py'`

