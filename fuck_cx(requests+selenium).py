from msedge.selenium_tools import Edge, EdgeOptions
from bs4 import BeautifulSoup
from PIL import Image
import requests 
import base64
import random
import json
import time
import getpass

######################需要设置的信息##############################
webdriver_path = r"" #引号内填入你下载的Webdriver路径
phone = ""           #引号内填入你的手机号
password = ""        #引号内填入你的密码
################################################################

user_name = getpass.getuser() #获取当前系统用户名
user_data = f"C:\\Users\\{user_name}\\AppData\\Local\\Microsoft\\Edge\\User Data"

class fuck_cx():
    def __init__(self,drive,headers,phone,password):
        self.drive = drive
        self.headers = headers
        self.phone = phone
        self.password = password
        try:
            drive.get("http://mooc1-1.chaoxing.com/visit/interaction")
            user = drive.find_element_by_xpath('//input[@id="phone"]')
            user.send_keys(self.phone)
            
            password = drive.find_element_by_xpath('//input[@id="pwd"]')
            password.send_keys(self.password)
            
            drive.find_element_by_xpath('//button[@id="loginBtn"]').click()
        except:
            pass

    #获取课程的名称和各任务的url
    def re_cx(self):
        session = requests.Session()
        url = 'http://mooc2-ans.chaoxing.com/visit/interaction'
        re = session.get(url)
        bs = BeautifulSoup(re.text,"lxml")

        fid = bs.find(id="fid")["value"]
        phone = self.phone
        password = self.password
        bytes_pwd = password.encode("utf-8")
        pwd = base64.b64encode(bytes_pwd)
        refer = "http%3A%2F%2Fi.chaoxing.com"
        t = bs.find(id="t")["value"]
        forbidotherlogin = 0
        data = {                  #获取登录需要的数据
            'fid':fid,
            'uname':phone,
            'password':pwd,
            'refer':refer,
            't':t,
            'forbidotherlogin':forbidotherlogin
            }
        url = "http://passport2.chaoxing.com/fanyalogin"
        re = session.post(url=url,data=data)
        re_json = re.text
        re_dict = json.loads(re_json)
        if re_dict["status"]:
            print("登录成功！\n--------------------------------")
            url = 'http://mooc2-ans.chaoxing.com/visit/courses/list?rss=1&start=0&size=500&catalogId=0&searchname='
            re = session.get(url)
            bs = BeautifulSoup(re.text,"lxml")
            kc_bs = bs.find_all(class_="inlineBlock")
            x = 0
            kc_url = []
            for kb in kc_bs:
                x += 1
                kc_url.append("http://mooc2-ans.chaoxing.com" + kb.find("a")["href"])
                kc_title = kb.find("a").find("span")["title"]
                print(f"课程序号{x}："+kc_title)
            size = input("--------------------------------\n请输入要完成的课程序号：")
            kc_page_url = kc_url[int(size)-1]
            kc_page_re = session.get(kc_page_url)
            kc_page_bs = BeautifulSoup(kc_page_re.text,"lxml")
            #kc_page_url_one参数获取
            courseid = kc_page_bs.find(id="courseid")["value"]
            clazzid = kc_page_bs.find(id="clazzid")["value"]
            cpi = kc_page_bs.find(id="cpi")["value"]
            ut = kc_page_bs.find(id="heardUt")["value"]
            enc = kc_page_bs.find(id="oldenc")["value"]
            openc = kc_page_bs.find(id="openc")["value"]
            #传入kc_page_url_one参数
            kc_page_url_one = f"http://mooc2-ans.chaoxing.com/mycourse/studentcourse?courseid={courseid}&clazzid={clazzid}&cpi={cpi}&ut={ut}"
            kc_page_one_re = session.get(kc_page_url_one)
            kc_page_one_bs = BeautifulSoup(kc_page_one_re.text,"lxml")
            xj_catalog_title = kc_page_one_bs.find_all(class_="catalog_title")
            zj_catalog_name = kc_page_one_bs.find_all(class_="catalog_name")
            zj_title = []
            for zcn in zj_catalog_name:
                try:
                    zj_title.append(zcn.find("span")["title"])
                except:
                    continue
            x = 0
            for xct in xj_catalog_title:
                chapterid = xct.find(type="checkbox")["value"]
                if chapterid:
                    rw_url = f"http://mooc1.chaoxing.com/mycourse/studentstudy?chapterId={chapterid}&courseId={courseid}&clazzid={clazzid}&enc={enc}&mooc2=1&cpi={cpi}&openc={openc}"
                    #检测异常页面
                    self.error()
                    #进入任务页
                    self.drive.get(rw_url)
                    #刷任务
                    self.get_pv()             
                else:
                    print("\n"+zj_title[x])
                    x += 1
            print("已完成："+str(int(x))+"号课程\n")
 

    #获取有多少个ppt和视频，并刷任务
    def get_pv(self):
        self.drive.switch_to.frame("iframe")
        ppt = self.drive.find_elements_by_xpath('//iframe[@class="ans-attach-online insertdoc-online-ppt"]') 
        video = self.drive.find_elements_by_xpath('//iframe[@class="ans-attach-online ans-insertvideo-online"]')
        pp = []
        vv = []

        for v in video:
            vv.append(v)
            time.sleep(1)
            try:
                self.drive.switch_to.frame(v)
                self.falsh_video()
            except:
                self.drive.switch_to.parent_frame()
                if video:
                    self.drive.switch_to.frame(v)
                    self.falsh_video()
                else:
                    self.drive.switch_to.frame("frame_content")
                    self.drive.switch_to.frame("time")
                    self.drive.find_element_by_xpath('//button[@class="vjs-big-play-button"]').click()
        print("完成了"+str(len(vv))+"个视频")

        for p in ppt:
            pp.append(p)
            try:
                self.drive.switch_to.frame(p) #进入第二层嵌套网页
                self.falsh_ppt()    
            except:
                self.drive.switch_to.parent_frame() #返回上一级frame
                if ppt:
                    self.drive.switch_to.frame(p)
                    self.falsh_ppt()

        print("完成了"+str(len(pp))+"个PPT\n")
            

    #刷PPt
    def falsh_ppt(self):
        time.sleep(0.5)
        drive = self.drive
        try:
            ppt_size = int(drive.find_element_by_xpath('//span[@class="all"]').text) #获取ppt页数
            for ps in range(ppt_size):
                drive.find_element_by_xpath('//a[@id="ext-gen1043"]').click()
        except:
            print(str(ps)+"页PPT")


    #刷视频
    def falsh_video(self):
        drive = self.drive
        drive.find_element_by_xpath('//button[@title="播放视频"]').click()
        if drive.find_element_by_xpath('//span[@class="vjs-duration-display"]'):
            print("\nstart")
            time.sleep(0.5)
            min = drive.find_element_by_xpath('//span[@class="vjs-duration-display"]').text.split(":")[0]
            sec = drive.find_element_by_xpath('//span[@class="vjs-duration-display"]').text.split(":")[1]
            data_time = (int(min)*60+int(sec))/16
            print("请等待"+str(data_time+1)+"秒")
            time.sleep(data_time)
            # time.sleep(0.2)
            # self.drive.switch_to.alert().send_keys("yes")
            # time.sleep(0.2)
            # self.drive.switch_to.alert().accept()
        else:
            print("NO")

    #显示出验证码并消除验证界面
    def error(self):
        try:
            time.sleep(1)
            if self.drive.find_element_by_xpath('//i[@class="warn"]'):
                self.drive.save_screenshot('pictures.png')  # 全屏截图
                page_snap_obj = Image.open('pictures.png')
                img = self.drive.find_element_by_xpath('//img[@id="ccc"]')  # 验证码元素位置
                time.sleep(1)
                location = img.location
                size = img.size  # 获取验证码的大小参数
                left = location['x']
                top = location['y']
                right = left + size['width']
                bottom = top + size['height']
                image_obj = page_snap_obj.crop((left, top, right, bottom))  # 按照验证码的长宽，切割验证码
                image_obj.show()
                self.drive.find_element_by_xpath('//input[@class="yzmInp"]').send_keys(input("输入验证码："))
                self.drive.find_element_by_xpath('//input[@class="submit"]').click()
                time.sleep(1)
        except:
            pass

if __name__ == "__main__":
    try:
        #edge设置
        edge_opt = EdgeOptions()
        edge_opt.use_chromium = True
        edge_opt.add_argument('lang=zh_CN.UTF-8')
        # edge_opt.add_argument("--headless")
        # edge_opt.add_argument("--disable-gpu")
        edge_opt.add_argument("--mute-audio")
        edge_opt.add_argument('disable-infobars')
        edge_opt.add_argument("--user-data-dir="+user_data)
        edge_opt.add_experimental_option('excludeSwitches', ['enable-automation'])
        drive = Edge(webdriver_path,options=edge_opt)
        #随机请求头信息
        headers = {
        'Accept':'text/html, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Host':'mooc1.chaoxing.com',
        'Pragma':'no-cache',
        'User-Agent':'',
        'X-Requested-With':'XMLHttpRequest'
        }
        user_agent_list = [ 
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
        ]
        headers['User-Agent'] = random.choice(user_agent_list)
        #运行。。。
        run = fuck_cx(drive,headers,phone,password)
        run.re_cx()
    except KeyboardInterrupt:
        quit()
        drive.close()
