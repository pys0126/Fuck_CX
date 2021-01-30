from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image
import requests 
import time
import os

class fuck_cx():

    def __init__(self,cookie,headers,drive):
        self.drive = drive
        self.cookies = cookie
        self.headers = headers
        try:
            drive.get("http://mooc1-1.chaoxing.com/visit/interaction")
            user = drive.find_element_by_xpath('//input[@id="phone"]')
            user.send_keys(input("输入手机号或用户名："))
            # user.send_keys("17783880328")
            password = drive.find_element_by_xpath('//input[@id="pwd"]')
            password.send_keys(input("输入密码："))
            # password.send_keys("Darkabyss86734")
            drive.find_element_by_xpath('//button[@id="loginBtn"]').click()
        except:
            pass

    #获取课程的名称和各任务的url
    def re_cx(self):
        cx_url = "http://mooc1-1.chaoxing.com/visit/interaction"
        cx_re = requests.Session()
        cx_res = cx_re.get(cx_url,cookies=self.cookies,headers=self.headers)
        cx_bs = BeautifulSoup(cx_res.text,"lxml")
        if cx_bs.find(class_="lg-title"):
            print("登录失败！")
            quit()
        else:
            print("登录成功！")
            print("---------课程列表----------")
            kc_li = cx_bs.find_all(class_="courseItem curFile")
            k = 0
            for title in kc_li:
                k += 1
                kc_titile = title.find(class_="courseName")["title"]
                print(str(k)+": "+kc_titile)
            print("--------------------------")
            x = input("请输入课程序号(Ctrl+C退出程序)：")
            kc_page_url = "https://mooc1-1.chaoxing.com" + cx_bs.find_all(class_="courseItem curFile")[int(x)-1].find(class_="courseName")["href"]
            print(kc_page_url)
            list_page_re = requests.Session()
            list_page_res = list_page_re.get(kc_page_url,cookies=self.cookies,headers=self.headers)
            list_page_bs4 = BeautifulSoup(list_page_res.text,"lxml")
            all_zj_html = list_page_bs4.find_all(class_="units")
            for all_zj in all_zj_html:
                zj_title = all_zj.find("h2").find("a")["title"]
                all_xj = all_zj.find_all(class_="leveltwo")
                print("***********"+zj_title+"***********\n")
                #各任务的url
                for xj in all_xj:
                    xj_url = "https://mooc1-2.chaoxing.com" + xj.find(class_="articlename").find("a")["href"]
                    xj_title = xj.find(class_="articlename").find("a")["title"]
                    print("开始任务："+xj_title)
                    #检测异常页面
                    self.error()
                    #进入任务页
                    self.drive.get(xj_url)
                    #刷任务
                    self.get_pv()
                    
            print("已完成："+str(int(x))+"号课程\n")
 

    #获取有多少个ppt和视频，并刷任务
    def get_pv(self):
        drive.switch_to.frame("iframe")
        ppt = drive.find_elements_by_xpath('//iframe[@class="ans-attach-online insertdoc-online-ppt"]') 
        video = drive.find_elements_by_xpath('//iframe[@class="ans-attach-online ans-insertvideo-online"]')
        pp = []
        vv = []
        
        for v in video:
            vv.append(v)
            time.sleep(5)
            try:
                drive.switch_to.frame(v)
                self.falsh_video()
            except:
                drive.switch_to.parent_frame()
                if video:
                    drive.switch_to.frame(v)
                    self.falsh_video()
                else:
                    drive.switch_to.frame("frame_content")
                    drive.switch_to.frame("time")
                    drive.find_element_by_xpath('//button[@class="vjs-big-play-button"]').click()
        print("\n完成了"+str(len(vv))+"个视频")

        for p in ppt:
            pp.append(p)
            try:
                drive.switch_to.frame(p) #进入第二层嵌套网页
                self.falsh_ppt()
            except:
                drive.switch_to.parent_frame() #返回上一级frame
                if ppt:
                    drive.switch_to.frame(p)
                    self.falsh_ppt()

        print("完成了"+str(len(pp))+"个PPT\n")
            

    #刷PPt
    def falsh_ppt(self):
        time.sleep(0.5)
        ppt_size = int(drive.find_element_by_xpath('//span[@class="all"]').text) #获取ppt页数
        try:
            for ps in range(ppt_size):
                drive.find_element_by_xpath('//a[@id="ext-gen1043"]').click()
        except:
            pass
        return print(ps+1)


    #刷视频
    def falsh_video(self):
        drive.find_element_by_xpath('//button[@title="播放视频"]').click()
        # time.sleep(0)
        # drive.switch_to_alert().send_keys("yes")
        # drive.switch_to_alert().accept()
        

    #显示出验证码并消除验证界面
    def error(self):
        try:
            time.sleep(1)
            if drive.find_element_by_xpath('//i[@class="warn"]'):
                drive.save_screenshot('pictures.png')  # 全屏截图
                page_snap_obj = Image.open('pictures.png')
                img = drive.find_element_by_xpath('//img[@id="ccc"]')  # 验证码元素位置
                time.sleep(1)
                location = img.location
                size = img.size  # 获取验证码的大小参数
                left = location['x']
                top = location['y']
                right = left + size['width']
                bottom = top + size['height']
                image_obj = page_snap_obj.crop((left, top, right, bottom))  # 按照验证码的长宽，切割验证码
                image_obj.show()
                drive.find_element_by_xpath('//input[@class="yzmInp"]').send_keys(input("输入验证码："))
                drive.find_element_by_xpath('//input[@class="submit"]').click()
                time.sleep(1)
        except:
            pass

if __name__ == "__main__":
    try:
        c = input("输入cookie：") 
        # c = 'lv=0; fid=9835; _uid=158574154; uf=14b6b1b3f40d8f90115aff9a480c2946b4cb11962702d83e6ab662843a689ab9f05660a41ce3e512c075c2db39694388913b662843f1f4ad6d92e371d7fdf64432ff693cabccda6bce915f659a7402a85558ebfe920d455c987c077384b9cd114a837b5069d5f848; _d=1611930475086; UID=158574154; vc=F94F84B07C4EEB1C0A35AE8E68B11954; vc2=180E7C0D27DD393A92B8E3292E348785; vc3=SdCRay59rds3sPjzE8OaaUPd8NJklP%2BidmNU7scG0T4%2F4X8CjJK6DIY3r5w9jV9ycO12jb2WXf%2BDddkQTPO2FHuJh%2F4jqdAik%2BxNRyGW%2FH%2BSP4og71HZXHGsBCpAZg5t2BzqEXzzCR%2BkZhyyIk%2Bxde7RGs856D21IkEy6K3qDSk%3Dfb7c5762e799b9ea1c1b4b891c239a2f; xxtenc=35b1b542b12a3e45ef347fd8165cab82; DSSTASH_LOG=C_38-UN_9255-US_158574154-T_1611930475087; source=""; spaceFid=9835; spaceRoleId=""; k8s=51775cddee2e06c0058c81fe70b0c7be0024790b; jrose=B3450BD3B659C7D84D262ED94FD78578.mooc-2133235240-jpzw3; tl=1; route=ac9a7739314fa6817cbac7e56032374b; thirdRegist=0; rt=-2'
        cookie = r"{}".format(c)
        cookies = {}
        for line in cookie.split(';'):
            key, value = line.split('=', 1)
            cookies[key] = value
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
        chrome_opt = webdriver.ChromeOptions()
        chrome_opt.add_argument("--headless")
        chrome_opt.add_argument("--disable-gpu")
        chrome_opt.add_argument('disable-infobars')
        个人资料路径 = r"/home/uodrad/.config/google-chrome/Default"  #在Chrome访问chrome://version/找到个人资料路径
        webdriver_path = r"/usr/local/bin/chromedriver" #填入你下载的Webdriver路径
        chrome_opt.add_argument("--user-data-dir="+个人资料路径)
        drive = webdriver.Chrome(webdriver_path,options=chrome_opt)
        run = fuck_cx(cookies,headers,drive)
        run.re_cx()
    except KeyboardInterrupt:
        quit()
        drive.close()




        
        
