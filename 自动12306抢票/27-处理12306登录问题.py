import random
import time
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Edge, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.edge.options import Options
from tkinter import *
import argparse

class Application(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master

        self.pack()
        self.createWidget()

    def createWidget(self):
        self.v1 = StringVar() # 账号
        self.v2 = StringVar() # 密码
        self.v3 = StringVar() # 出发点
        self.v4 = StringVar() # 终点
        self.v5 = StringVar() # 时间
        self.v6 = StringVar() # 乘车人
        # 用户名栏
        self.label01 = Label(self, text="12306用户名").grid(row=0,column=0,sticky=W+S+E+N)
        self.entry01 = Entry(self, textvariable=self.v1)
        self.entry01.grid(row=0,column=1,columnspan=2,sticky=W+S+E+N)
        # 用户密码栏
        self.label02 = Label(self, text="12306密码").grid(row=1,column=0,sticky=W+S+E+N)
        self.entry02 = Entry(self, textvariable=self.v2)
        self.entry02.grid(row=1, column=1, columnspan=2, sticky=W + S + E + N)
        # 始发地
        self.label03 = Label(self, text="始发地").grid(row=2, column=0, sticky=W + S + E + N)
        self.entry03 = Entry(self, textvariable=self.v3)
        self.entry03.grid(row=2, column=1, sticky=W + S + E + N)
        # 终点
        self.label04 = Label(self, text="终点").grid(row=3, column=0, sticky=W + S + E + N)
        self.entry04 = Entry(self, textvariable=self.v4)
        self.entry04.grid(row=3, column=1, sticky=W + S + E + N)
        # 出发时间
        self.label05 = Label(self, text="出发时间").grid(row=4, column=0, sticky=W + S + E + N)
        self.entry05 = Entry(self, textvariable=self.v5)
        self.entry05.grid(row=4, column=1, sticky=W + S + E + N)
        # 出发时间
        self.label06 = Label(self, text="乘车人").grid(row=5, column=0, sticky=W + S + E + N)
        self.entry06 = Entry(self, textvariable=self.v6)
        self.entry06.grid(row=5, column=1, columnspan=2, sticky=W + S + E + N)
        # 警告
        self.label06 = Label(self,text="出发时间没售票将会持续等待!!",fg="red").grid(row=6,column=1,columnspan=2,rowspan=2,sticky=W + S + E + N)

        self.btn01 = Button(self,text="确认",command=lambda :kefw_12306(self.entry01.get(),self.entry02.get(),self.entry03.get(),self.entry04.get(),self.entry05.get(),self.entry06.get())
                          ,bg="pink",fg="red").grid(row=8,column=0,sticky=W + S + E + N)
        self.btn02 = Button(self,text="退出",command=root.destroy).grid(row=8,column=1,sticky=W + S + E + N)



def get_move_track(gap):
    track = []  # 移动轨迹
    current = 0  # 当前位移
    # 减速阈值
    mid = gap * 4 / 5  # 前4/5段加速 后1/5段减速
    f = random.random()
    if f>0.7:
        t = f/2
    elif f<0.2:
        t = f+0.1
    else:
        t = f  # 计算间隔
    v = 0  # 初速度
    while current < gap:
        if current < mid:
            num = random.randrange(4)*20
            a = 30  # 加速度为+5
        else:
            a = -10  # 加速度为-5
        v0 = v  # 初速度v0
        v = v0 + a * t  # 当前速度
        move = v0 * t + 1 / 2 * a * t * t  # 移动距离
        current += move  # 当前位移
        track.append(round(move))  # 加入轨迹
    return track


def kefw_12306(number,password,string_point,end,string_time,name):
    option = Options()
    option.add_argument("--enable-automation")
    option.add_argument("--headless")
    option.add_argument("--start-maximized")
    web = webdriver.Edge(options=option)
    web.get('https://kyfw.12306.cn/otn/resources/login.html')
    # 照搬照抄CSDN不然滑块处理会出错
    script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
    web.execute_script(script)
    time.sleep(1)
    # 点击 ‘账号登录’
    web.find_element(by=By.XPATH,value='//*[@id="toolbar_Div"]/div[2]/div[2]/ul/li[1]/a').click()
    time.sleep(1)
    # 输入用户名
    web.find_element(by=By.XPATH,value='//*[@id="J-userName"]').send_keys(number)
    time.sleep(0.5)
    # 输入密码
    web.find_element(by=By.XPATH,value='//*[@id="J-password"]').send_keys(password)
    time.sleep(0.5)
    # 点击登录
    try:
        web.find_element(by=By.XPATH,value='//*[@id="J-login"]').click()
    except Exception as e:
        messagebox.showinfo("高铁12306自动化", "用户名或密码输入错误")
    time.sleep(2)

    # while True:
    try:
        slider = WebDriverWait(web,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="nc_1_n1z"]')))
    except Exception as e:
        messagebox.showinfo("高铁12306自动化", "用户名或密码输入错误")
    distance = 350
    actions = ActionChains(web)
    # 摁住 持续0.5s
    actions.click_and_hold(slider)
    actions.pause(0.5)
    move_track = get_move_track(distance)
    # print(move_track[3:])
    for i in move_track[3:]:
        actions.move_by_offset(i,0).perform()
        time.sleep(0.1)
    actions.pause(0.4)
    # actions.move_by_offset(-10,0)
    # 松开
    actions.release()
    # 结束
    actions.perform()
    time.sleep(4)
    # 进入单程的买票页面
    element = web.find_element(by=By.LINK_TEXT,value='车票')
    # 鼠标移动到 '车票' 元素上的中心点
    actions.move_to_element(element).perform()
    # 点击'单程'
    web.find_element(by=By.XPATH,value='//*[@id="J-chepiao"]/div/div[1]/ul/li[1]/a').click()
    # 消除第二次弹窗
    # web.find_element(by=By.LINK_TEXT,value='确认').click()
    time.sleep(1)
    # web.find_element(by=By.XPATH,value='//*[@id="J-index"]/a').click()
    i = 1
    while True:
        web.find_element(by=By.XPATH,value='//*[@id="fromStationText"]').click()
        web.find_element(by=By.XPATH,value='//*[@id="fromStationText"]').send_keys(string_point,Keys.ENTER)
        web.find_element(by=By.XPATH,value='//*[@id="toStationText"]').click()
        web.find_element(by=By.XPATH,value='//*[@id="toStationText"]').send_keys(end,Keys.ENTER)
        web.find_element(by=By.XPATH,value='//*[@id="train_date"]').click()
        web.find_element(by=By.XPATH,value='//*[@id="train_date"]').clear()
        web.find_element(by=By.XPATH,value='//*[@id="train_date"]').click()
        web.find_element(by=By.XPATH,value='//*[@id="train_date"]').send_keys(string_time,Keys.ENTER)
        web.find_element(by=By.XPATH,value='//*[@id="query_ticket"]').click()
        time.sleep(1)
        while True:
            try:
                WebDriverWait(web, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="ticket_18000K739205_03_09"]/td[13]/a'))).click()
            except Exception as e:
                time.sleep(5)
                web.refresh()
                continue
            break
        # web.find_element(by=By.XPATH,value='//*[@id="ticket_18000K739205_03_09"]/td[13]/a').click()
        time.sleep(1)
        name.split(" ")
        # print(type(name))
        # 选好乘客
        if type(name) == str:
            try:
                web.find_element(by=By.XPATH,value=f'//*[@id="normal_passenger_id"]/li/label[contains(text(),"{name}")]').click()
            except Exception as e:
                messagebox.showinfo("高铁12306自动化", f"用户-{i}不存在 请仔细阅读手册")
        else:
            for i in name:
                try:
                    web.find_element(by=By.XPATH,value=f'//*[@id="normal_passenger_id"]/li/label[contains(text(),"{name}")]').click()
                except Exception as e:
                    messagebox.showinfo("高铁12306自动化", f"用户-{i}不存在 请仔细阅读手册")
        # 提交订单
        time.sleep(0.4)
        web.find_element(by=By.XPATH,value='//*[@id="submitOrder_id"]').click()
        time.sleep(1)
        # print("抢票成功")
        time.sleep(1)
        web.find_element(by=By.XPATH,value='//*[@id="qr_submit_id"]').click()
        time.sleep(0.1)
        bunk = web.find_element(by=By.XPATH,value='//*[@id="show_ticket_message"]/tr/td[8]').text
        time.sleep(1)
        i+=1
        if not bunk.count('下铺') and i!=4:
            # web.find_element(by=By.XPATH,value='//*[@id="insurance_buy_and_agree"]').click()
            web.find_element(by=By.XPATH,value='//*[@id="cancelButton"]').click()
            time.sleep(1)
            continue
        else:
            break
    messagebox.showinfo("高铁12306自动化", "抢票成功,前往客服端支付")
    web.close()


if __name__ == '__main__':
    root = Tk()
    root.title("自动抢票")
    app = Application(master=root)
    root.mainloop()
    time.sleep(5)