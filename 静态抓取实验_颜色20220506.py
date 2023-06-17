#########################################################
USBCamear = 0 #摄像头编号，自带一般为0，顺延

Delta_Photo_U1 =207 #Delta摄像头截取的图像左上角顶点像素坐标U1
Delta_Photo_V1 =101 #Delta摄像头截取的图像左上角顶点像素坐标V1
Delta_Photo_U2 =397 #Delta摄像头截取的图像右下角顶点像素坐标U2
Delta_Photo_V2 =303 #Delta摄像头截取的图像右下角顶点像素坐标V2

HSV_Blue_LH =97 #蓝色H低值
HSV_Blue_LS =65 #蓝色S低值
HSV_Blue_LV =30 #蓝色V低值
HSV_Blue_HH =137 #蓝色H高值
HSV_Blue_HS =255 #蓝色S高值
HSV_Blue_HV =255 #蓝色V高值
HSV_Red_LH =0  #红色H低值
HSV_Red_LS =39 #红色S低值
HSV_Red_LV =128 #红色V低值
HSV_Red_HH =54 #红色H高值
HSV_Red_HS =255 #红色S高值
HSV_Red_HV =255 #红色V高值

Xa1 =-0.016 #像素坐标_机器人坐标转换矩阵计算的值第一组数值的第一个
Xa2 =-0.712 #像素坐标_机器人坐标转换矩阵计算的值第一组数值的第二个
Xa3 =92.312#像素坐标_机器人坐标转换矩阵计算的值第一组数值的第三个
Ya1 =0.757 #像素坐标_机器人坐标转换矩阵计算的值第二组数值的第一个
Ya2 =0.005 #像素坐标_机器人坐标转换矩阵计算的值第二组数值的第二个
Ya3 =-75.276 #像素坐标_机器人坐标转换矩阵计算的值第二组数值的第三个
##############################################################

import math
import socket
import struct
import time
import tkinter as tk
from tkinter import *

import cv2 as cv
import numpy as np
from PIL import Image, ImageTk

# 创建画布需要的库
class basedesk():
    def __init__(self, master):
        self.top = master
        self.top.config()
        self.top.title('应用实验')
        self.top.geometry('1536x808')
        self.top.resizable(0, 0)
        self.top.configure(bg="whitesmoke")

        face1(self.top)
class face1():##第四个页面（静态抓取）
    def __init__(self, master):
        self.master = master
        self.master.config(bg='gainsboro')
        self.master.title('基于视觉的静态物体抓取')
        self.master.iconphoto(False, tk.PhotoImage(file="D:/study_work/logo/logo.png"))
        self.face3 = tk.Canvas(self.master, height=808, width=1536,
                               bg="gainsboro")
        self.face3.place(x=0, y=0)
        ##参数初始化
        self.var = tk.StringVar()
        self.var1 = tk.StringVar()
        self.var1.set("0.087")
        self.var2 = tk.StringVar()
        self.var2.set(0.057)
        self.var3 = tk.StringVar()
        self.var3.set(0.097)
        ##原点到达标志
        self.var4 = tk.IntVar()
        self.var4.set(0)
        ##等待区到达标志位
        self.var5 = tk.IntVar()
        self.var5.set(0)
        ##拍照位置到达标志位置
        self.var6 = tk.IntVar()
        self.var6.set(0)
        ##抓取结束标志位
        self.var7 = tk.IntVar()
        self.var7.set(0)
        ##大小圆个数
        self.var8 = tk.IntVar()
        self.var8.set(0)
        self.var9 = tk.IntVar()
        self.var9.set(0)
        ##画布
        ##画布1（用来放显示label）
        self.canvas = tk.Canvas(self.face3, height=791, width=508,
                           bg="whitesmoke")
        self.canvas.place(x=2, y=5)
        ##画布2（用来放按钮）
        self.canvas1 = tk.Canvas(self.face3, height=791, width=240,
                            bg="whitesmoke")
        self.canvas1.place(x=515, y=5)
        ##画布3（用来放原始图像和处理后图像）
        self.canvas2 = tk.Canvas(self.face3, height=788, width=769,
                            bg="whitesmoke")
        self.canvas2.place(x=760, y=5)
        self.canvas3 = tk.Canvas(self.face3, height=2, width=769,
                                 bg="gainsboro")
        self.canvas3.place(x=760, y=400)
        photo1 = None;photo2=None;img1=None;img2=None
        self.cap = cv.VideoCapture(USBCamear)#USB摄像头编号
        ##显示标签
        label1 = tk.Label(self.canvas, text="蓝色零件个数：", bg="whitesmoke", font=("微软雅黑", 14), width=11, height=1)
        label1.place(x=2, y=90)
        label2 = tk.Label(self.canvas, text="红色零件个数：", bg="whitesmoke", font=("微软雅黑", 14), width=11, height=1)
        label2.place(x=2, y=160)
        label3 = tk.Label(self.canvas, text="机器人关节1实时角度：", bg="whitesmoke", font=("微软雅黑", 14), width=17, height=1)
        label3.place(x=2, y=230)
        label4 = tk.Label(self.canvas, text="机器人关节2实时角度：", bg="whitesmoke", font=("微软雅黑", 14), width=17, height=1)
        label4.place(x=2, y=300)
        label5 = tk.Label(self.canvas, text="机器人关节3实时角度：", bg="whitesmoke", font=("微软雅黑", 14), width=17, height=1)
        label5.place(x=2, y=370)
        label6 = tk.Label(self.canvas, text="原点到达标志位（0：未到达，1：到达）：", bg="whitesmoke", font=("微软雅黑", 14), width=30, height=1)
        label6.place(x=2, y=430)
        label7 = tk.Label(self.canvas, text="到达等候区标志位（0：未到达，1：到达）：", bg="whitesmoke", font=("微软雅黑", 14), width=32,
                          height=1)
        label7.place(x=2, y=500)

        label8 = tk.Label(self.canvas, text="抓取结束标志位（0：未到达，1：到达）：", bg="whitesmoke", font=("微软雅黑", 16), width=31, height=1)
        label8.place(x=2, y=570)
        label9 = tk.Label(self.canvas, text="到达拍照位置标志位（0：未到达，1：到达）：", bg="whitesmoke", font=("微软雅黑", 16), width=34,
                          height=1)
        label9.place(x=2, y=640)

        label101 = tk.Label(self.canvas, text="Z方向坐标值:", bg="whitesmoke", font=("微软雅黑", 14), width=9, height=1)
        label101.place(x=1, y=710)
        self.user_text71 = tk.Entry(width=12, font=("微软雅黑", 14))  # 创建文本框填写关节3
        self.user_text71.place(x=150, y=715)

        label10 = tk.Label(self.canvas2, text="原始图像", bg="whitesmoke", fg="red", font=("微软雅黑", 24), width=8, height=1)
        label10.place(x=310, y=340)
        label11 = tk.Label(self.canvas2, text="红色零件", bg="whitesmoke", fg="red", font=("微软雅黑", 24), width=8, height=1)
        label11.place(x=120, y=705)
        label100 = tk.Label(self.canvas2, text="蓝色零件", bg="whitesmoke", fg="blue", font=("微软雅黑", 24), width=8, height=1)
        label100.place(x=490, y=705)

        label22 = tk.Label(self.canvas, text="参数显示", bg="whitesmoke", fg="red", font=("微软雅黑", 24), width=8, height=1)
        label22.place(x=180, y=1)
        label23 = tk.Label(self.canvas1, text="按钮显示", bg="whitesmoke", fg="red", font=("微软雅黑", 24), width=8, height=1)
        label23.place(x=45, y=1)
        ###按钮
        homebutton = tk.Button(self.canvas1, text="机器人回原点", bg="gainsboro", command=self.home, font=("微软雅黑", 14), width=10,
                               height=2)
        homebutton.config(relief=RIDGE)
        homebutton.place(x=59, y=100)
        waitbutton = tk.Button(self.canvas1, text="等待位置", bg="gainsboro", command=self.wait, font=("微软雅黑", 14), width=10,
                               height=2)
        waitbutton.config(relief=RIDGE)
        waitbutton.place(x=59, y=230)
        grabbutton = tk.Button(self.canvas1, text="抓取", bg="gainsboro", command=self.grab, font=("微软雅黑", 14), width=10, height=2)
        grabbutton.config(relief=RIDGE)
        grabbutton.place(x=59, y=360)
        imagebutton = tk.Button(self.canvas1, text="图像采集-处理", bg="gainsboro", command=self.show, font=("微软雅黑", 14), width=10,
                                height=2)
        imagebutton.config(relief=RIDGE)
        imagebutton.place(x=59, y=490)
        tpbutton = tk.Button(self.canvas1, text="拍照位置", bg="gainsboro", command=self.tkphoto, font=("微软雅黑", 14), width=10,
                             height=2)
        tpbutton.config(relief=RIDGE)
        tpbutton.place(x=59, y=630)

    def inverse(self,x1,y1,z1):
        R = 51.5
        r = 33
        L1 = 200
        L2 = 392
        x = 0.8776 * x1 + 0.4929 * y1
        y = 0.8682 * y1 - 0.5041 * x1
        z = z1 - 325.4555
        m = L2 ** 2 - L1 ** 2 - x ** 2 - y ** 2 - z ** 2 - (R - r) ** 2
        m1 = ((R - r) * (math.sqrt(3) * x + y))
        m2 = ((R - r) * (math.sqrt(3) * x - y))
        if (x1 > 110) or (x1 < -110) or (y1 > 110) or (y1 < -110) or (z1 > 76) or (z1 < -39):
            print("超出运行轨迹范围，逆解不存在")
        else:
            K1 = ((m + m1) / L1 + 2 * z)
            K2 = ((m - m2) / L1 + 2 * z)
            K3 = ((m - 2 * y * (R - r)) / (2 * L1) + z)
            U1 = (-2 * (2 * (R - r) - (math.sqrt(3)) * x - y))
            U2 = (-2 * (2 * (R - r) + (math.sqrt(3)) * x - y))
            U3 = (-2 * (R - r + y))
            V1 = ((m + m1) / L1 - 2 * z)
            V2 = ((m - m1) / L1 - 2 * z)
            V3 = ((m - 2 * y * (R - r)) / (2 * L1) - z)
            T1 = ((-1 * U1 - (math.sqrt(U1 ** 2 - 4 * K1 * V1))) / (2 * K1))
            T2 = ((-1 * U2 - (math.sqrt(U2 ** 2 - 4 * K2 * V2))) / (2 * K2))
            T3 = ((-1 * U3 - (math.sqrt(U3 ** 2 - 4 * K3 * V3))) / (2 * K3))
            theta1 = (2 * (math.atan(T1)) - 1.5708) * 180 / (math.pi)
            theta1 = round(theta1, 4)
            theta2 = (2 * (math.atan(T2)) - 1.5708) * 180 / (math.pi)
            theta2 = round(theta2, 4)
            theta3 = (2 * (math.atan(T3)) - 1.5708) * 180 / (math.pi)
            theta3 = round(theta3, 4)
            if (theta1 > 26.5) or (theta1 < -42.79) or (theta2 > 26.5) or (theta2 < -37.86) or (theta3 > 26.5) or (
                    theta3 < -42.93):
                print("超出运行轨迹范围，逆解不存在")
            else:
                return theta1, theta2, theta3
    def soc_ket(self,aa,bb,cc,dd,ee,ff):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # AF_INET表示使用ipv4,默认不变，SOCK_DGRAM表示使用UDP通信协议
        # a=self.user_text71.get()
        # local_addr = (a, 7878)  # 默认本机任何ip ，指定端口号7878
        local_addr = ("192.168.1.189", 7878)
        udp_socket.bind(local_addr)  # 绑定端口

        x = float(aa * (Xa1) + bb * (Xa2) + (Xa3))  ##机器人X坐标,根据校准替换数值
        y = float(aa * (Ya1) + bb * (Ya2) + (Ya3))  ##机器人Y坐标，根据校准替换数值
        z = float(cc)  ##机器人Z坐标(0值)

        send_data1 = x  ###直线版本
        send_data2 = y  ###直线版本
        send_data3 = z  ###直线版本
        send_data4 = float(dd)  #####运行模式标志位（1代表回原点，2代表等待位置，3.代表拍照位置，4.代表抓取）
        send_data5 = float(ee)  ##检测物体标志位（1代表红色零件，2代表蓝色零件）
        send_data6 = float(ff)##机械臂Z位置
        byte1 = struct.pack('f', send_data1)  # folat转为4个字节
        byte2 = struct.pack('f', send_data2)
        byte3 = struct.pack('f', send_data3)
        byte4 = struct.pack('f', send_data4)
        byte5 = struct.pack('f', send_data5)
        byte6 = struct.pack('f', send_data6)
        byte = byte1 + byte2 + byte3 + byte4 + byte5+byte6  # 六个拼接成24个字节
        udp_socket.sendto(byte, ("192.168.1.181", 12300))  # 编码成全球统一数据格式，用元组表示接收方ip和port
        while True:
            self.master.update()

            recv_data = udp_socket.recvfrom(1024)
            recv_msg = recv_data[0]
            a1 = recv_msg[:4]  # 关节1实时位置
            a2 = recv_msg[4:8]  # 关节2实时位置
            a3 = recv_msg[8:12]  # 关节3实时位置
            a4 = recv_msg[12:16]  # 原点到达标志位
            a5 = recv_msg[16:20]  # 等待区到达标志位
            a6 = recv_msg[20:24]  # 拍照位置到达标志位
            a7 = recv_msg[-4:]  # 跳出WHILE循环

            m1 = struct.unpack("f", a1)
            m1 = round(float(m1[0]), 3)  # 关节1实时位置
            m1 = str(m1)
            m2 = struct.unpack("f", a2)
            m2 = round(float(m2[0]), 3)  # 关机2实时位置
            m2 = str(m2)
            m3 = struct.unpack("f", a3)
            m3 = round(float(m3[0]), 3)  # 关节3实时位置
            m3 = str(m3)
            m4 = struct.unpack("f", a4)
            m4 = int(m4[0])  # 原点到达标志位
            m5 = struct.unpack("f", a5)
            m5 = int(m5[0])  # 等待区到达标志位
            m6 = struct.unpack("f", a6)
            m6 = int(m6[0])  # 拍照位置到达标志位
            m7 = struct.unpack("f", a7)
            m7 = int(m7[0])  # 跳出WHILE循环标志位

            self.var1.set(m1)
            self.var2.set(m2)
            self.var3.set(m3)
            self.var4.set(m4)
            self.var5.set(m5)
            self.var7.set(m6)

            label14 = tk.Label(self.canvas, text=str(self.var1.get()), width=6, font=("微软雅黑", 14), height=1,
                               bg="white")  ##机器人关节1实时位置
            label14.place(x=216, y=232)
            label15 = tk.Label(self.canvas, text=str(self.var2.get()), width=6, font=("微软雅黑", 14), height=1,
                               bg="white")  ##机器人关节2实时位置
            label15.place(x=216, y=302)
            label16 = tk.Label(self.canvas, text=str(self.var3.get()), width=6, font=("微软雅黑", 14), height=1,
                               bg="white")  ##机器人关节3实时位置
            label16.place(x=216, y=372)
            label17 = tk.Label(self.canvas, text=str(self.var4.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##原点到达标志位
            label17.place(x=460, y=430)
            label18 = tk.Label(self.canvas, text=str(self.var5.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##等待位置到达标志位
            label18.place(x=460, y=500)
            label19 = tk.Label(self.canvas, text=str(self.var6.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##抓取位置到达标志位
            label19.place(x=460, y=570)
            label20 = tk.Label(self.canvas, text=str(self.var7.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##拍照位置到达标志位
            label20.place(x=468, y=640)
            if m7 == 1:

                break
        udp_socket.close()
    def undistort(self,frame):
        fx = 2433.94693
        cx = 215.8150
        fy = 2418.95178
        cy = 197.4180
        k1, k2, p1, p2, k3 = -12.2360, 185.2994, 0, 0, 0

        # 相机坐标系到像素坐标系的转换矩阵
        k = np.array([
            [fx, 0, cx],
            [0, fy, cy],
            [0, 0, 1]
        ])
        # 畸变系数
        d = np.array([
            k1, k2, p1, p2, k3
        ])
        h, w = frame.shape[:2]
        mapx, mapy = cv.initUndistortRectifyMap(k, d, None, k, (w, h), 5)
        return cv.remap(frame, mapx, mapy, cv.INTER_LINEAR)
    def take_photo(self):
        while True:
            ret, frame = self.cap.read()  # 读取摄像头,它能返回两个参数，第一个参数是bool型的ret，其值为True或False，代表有没有读到图片；第二个参数是frame，是当前截取一帧的图片
            if ret == True:

                time.sleep(1)

                cv.imwrite("D:/study_work/python/static_photo/camera80.png",
                           # frame) #截取区域范围打开此语句，否则关闭此语句
                           frame[Delta_Photo_V1:Delta_Photo_V2,Delta_Photo_U1:Delta_Photo_U2]) ##取得左上角和右下角的像素坐标，进行抓取实验操作打开此语句；进行截取区域范围时关闭此语句
                break
            else:
                pass
    def home(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # a = self.user_text71.get()
        # local_addr = (a, 7878)  # 默认本机任何ip ，指定端口号7878
        local_addr = ("192.168.1.189", 7878)
        udp_socket.bind(local_addr)
        send_data1 = 0.0  # 机器人关节1
        send_data2 = 0.0  # 机器人关节2
        send_data3 = 0.0  # 机器人关节3
        send_data4 = 1.0  ###运行模式标志位（1代表回原点，2代表等待位置，3.代表拍照位置，4.代表抓取）
        send_data5 = 4.0  ###检测物体标志位（1代表大圆，2代表小圆）
        send_data6 = 0.0  ###检测物体标志位（1代表大圆，2代表小圆）
        byte1 = struct.pack('f', send_data1)  # folat转为4个字节
        byte2 = struct.pack('f', send_data2)
        byte3 = struct.pack('f', send_data3)
        byte4 = struct.pack('f', send_data4)
        byte5 = struct.pack('f', send_data5)
        byte6 = struct.pack('f', send_data6)

        byte = byte1 + byte2 + byte3 + byte4 + byte5+ byte6
        udp_socket.sendto(byte, ("192.168.1.181", 12300))
        while True:
            self.master.update()

            recv_data = udp_socket.recvfrom(1024)
            recv_msg = recv_data[0]
            a1 = recv_msg[:4]  # 关节1实时位置
            a2 = recv_msg[4:8]  # 关节2实时位置
            a3 = recv_msg[8:12]  # 关节3实时位置
            a4 = recv_msg[12:16]  # 原点到达标志位
            a5 = recv_msg[16:20]  # 等待区到达标志位
            a6 = recv_msg[20:24]  # 拍照位置到达标志位
            a7 = recv_msg[-4:]  # 跳出WHILE循环

            m1 = struct.unpack("f", a1)
            m1 = round(float(m1[0]), 3)  # 关节1实时位置
            m1 = str(m1)
            m2 = struct.unpack("f", a2)
            m2 = round(float(m2[0]), 3)  # 关机2实时位置
            m2 = str(m2)
            m3 = struct.unpack("f", a3)
            m3 = round(float(m3[0]), 3)  # 关节3实时位置
            m3 = str(m3)
            m4 = struct.unpack("f", a4)
            m4 = int(m4[0])  # 原点到达标志位
            m5 = struct.unpack("f", a5)
            m5 = int(m5[0])  # 等待区到达标志位
            m6 = struct.unpack("f", a6)
            m6 = int(m6[0])  # 拍照位置到达标志位
            self.var1.set(m1)
            self.var2.set(m2)
            self.var3.set(m3)
            self.var4.set(m4)
            self.var5.set(m5)
            self.var7.set(m6)


            label14 = tk.Label(self.canvas, text=str(self.var1.get()), width=6, font=("微软雅黑", 14), height=1,
                               bg="white")  ##机器人关节1实时位置
            label14.place(x=216, y=232)
            label15 = tk.Label(self.canvas, text=str(self.var2.get()), width=6, font=("微软雅黑", 14), height=1,
                               bg="white")  ##机器人关节2实时位置
            label15.place(x=216, y=302)
            label16 = tk.Label(self.canvas, text=str(self.var3.get()), width=6, font=("微软雅黑", 14), height=1,
                               bg="white")  ##机器人关节3实时位置
            label16.place(x=216, y=372)
            label17 = tk.Label(self.canvas, text=str(self.var4.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##原点到达标志位
            label17.place(x=460, y=430)
            label18 = tk.Label(self.canvas, text=str(self.var5.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##等待位置到达标志位
            label18.place(x=460, y=500)
            label19 = tk.Label(self.canvas, text=str(self.var6.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##抓取位置到达标志位
            label19.place(x=460, y=570)
            label20 = tk.Label(self.canvas, text=str(self.var7.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##拍照位置到达标志位
            label20.place(x=468, y=640)
            if m4 == 1:

                break
        udp_socket.close()
    def wait(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # a = self.user_text71.get()
        # local_addr = (a, 7878)  # 默认本机任何ip ，指定端口号7878
        local_addr = ("192.168.1.189", 7878)
        udp_socket.bind(local_addr)
        send_data1 = 0.0  # 机器人关节1
        send_data2 = 0.0  # 机器人关节2
        send_data3 = 0.0  # 机器人关节3
        send_data4 = 2.0  ###运行模式标志位（1代表回原点，2代表等待位置，3.代表拍照位置，4.代表抓取）
        send_data5 = 4.0  ###检测物体标志位（1代表大圆，2代表小圆）
        send_data6 = 0.0
        byte1 = struct.pack('f', send_data1)  # folat转为4个字节
        byte2 = struct.pack('f', send_data2)
        byte3 = struct.pack('f', send_data3)
        byte4 = struct.pack('f', send_data4)
        byte5 = struct.pack('f', send_data5)
        byte6 = struct.pack('f', send_data6)

        byte = byte1 + byte2 + byte3 + byte4 + byte5+byte6
        udp_socket.sendto(byte, ("192.168.1.181", 12300))
        while True:
            self.master.update()

            recv_data = udp_socket.recvfrom(1024)
            recv_msg = recv_data[0]
            a1 = recv_msg[:4]  # 关节1实时位置
            a2 = recv_msg[4:8]  # 关节2实时位置
            a3 = recv_msg[8:12]  # 关节3实时位置
            a4 = recv_msg[12:16]  # 原点到达标志位
            a5 = recv_msg[16:20]  # 等待区到达标志位
            a6 = recv_msg[20:24]  # 拍照位置到达标志位
            a7 = recv_msg[-4:]  # 跳出WHILE循环

            m1 = struct.unpack("f", a1)
            m1 = round(float(m1[0]), 3)  # 关节1实时位置
            m1 = str(m1)
            m2 = struct.unpack("f", a2)
            m2 = round(float(m2[0]), 3)  # 关机2实时位置
            m2 = str(m2)
            m3 = struct.unpack("f", a3)
            m3 = round(float(m3[0]), 3)  # 关节3实时位置
            m3 = str(m3)
            m4 = struct.unpack("f", a4)
            m4 = int(m4[0])  # 原点到达标志位
            m5 = struct.unpack("f", a5)
            m5 = int(m5[0])  # 等待区到达标志位
            m6 = struct.unpack("f", a6)
            m6 = int(m6[0])  # 拍照位置到达标志位
            self.var1.set(m1)
            self.var2.set(m2)
            self.var3.set(m3)
            self.var4.set(m4)
            self.var5.set(m5)
            self.var7.set(m6)

            label14 = tk.Label(self.canvas, text=str(self.var1.get()), width=6, font=("微软雅黑", 14), height=1,
                               bg="white")  ##机器人关节1实时位置
            label14.place(x=216, y=232)
            label15 = tk.Label(self.canvas, text=str(self.var2.get()), width=6, font=("微软雅黑", 14), height=1,
                               bg="white")  ##机器人关节2实时位置
            label15.place(x=216, y=302)
            label16 = tk.Label(self.canvas, text=str(self.var3.get()), width=6, font=("微软雅黑", 14), height=1,
                               bg="white")  ##机器人关节3实时位置
            label16.place(x=216, y=372)
            label17 = tk.Label(self.canvas, text=str(self.var4.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##原点到达标志位
            label17.place(x=460, y=430)
            label18 = tk.Label(self.canvas, text=str(self.var5.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##等待位置到达标志位
            label18.place(x=460, y=500)
            label19 = tk.Label(self.canvas, text=str(self.var6.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##抓取位置到达标志位
            label19.place(x=460, y=570)
            label20 = tk.Label(self.canvas, text=str(self.var7.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##拍照位置到达标志位
            label20.place(x=468, y=640)
            if m5 == 1:

                break
        udp_socket.close()
    def grab(self):

        global bounding_boxes1
        global bounding_boxes2
        j1 = 0#红色
        j2=0#蓝色
        k1=0#红色
        k2=0#蓝色
        k = 0  # 当K等于总个数时退出程序
        m = 0  # 抓取结束标志位
        self.var6.set(m)
        label19 = tk.Label(self.canvas, text=str(self.var6.get()), width=3, font=("微软雅黑", 14), height=1,
                           bg="white")  ##抓取位置到达标志位
        label19.place(x=460, y=570)
        total_box=len(bounding_boxes1)+len(bounding_boxes2)

        cc = 0  ##机器人Z高度（直线版本）
        dd = float(4)  # #####运行模式标志位（1代表回原点，2代表等待位置，3.代表拍照位置，4.代表抓取）
        for bbox2 in bounding_boxes2:#红色

            len_m1 = len(bounding_boxes2)
            j1 = j1 + 1
            if j1 == len(bounding_boxes2):
                for i1 in range(len_m1):
                    a = (bounding_boxes2[i1][0] + (bounding_boxes2[i1][2]) / 2)
                    b = (bounding_boxes2[i1][1] + (bounding_boxes2[i1][3]) / 2)
                    aa = int(a)
                    bb = int(b)

                    self.soc_ket(aa, bb, cc, dd, 1.0,self.user_text71.get())
                    k1=k1+1
        for bbox1 in bounding_boxes1:#蓝色

            len_m2 = len(bounding_boxes1)
            j2 = j2 + 1
            if j2 == len(bounding_boxes1):
                for i2 in range(len_m2):
                    a = (bounding_boxes1[i2][0] + (bounding_boxes1[i2][2]) / 2)
                    b = (bounding_boxes1[i2][1] + (bounding_boxes1[i2][3]) / 2)
                    aa = int(a)
                    bb = int(b)

                    self.soc_ket(aa, bb, cc, dd, 2.0,self.user_text71.get())
                    k2=k2+1
        k=k1+k2
        if k==total_box:
            m=1
            self.var6.set(m)
            label19 = tk.Label(self.canvas, text=str(self.var6.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##抓取位置到达标志位
            label19.place(x=460, y=570)

    def show(self):
        self.take_photo()

        global photo1, photo2,photo3
        global img1, img2,img3
        global bounding_boxes1
        global bounding_boxes2
        lower_blue = np.array([HSV_Blue_LH, HSV_Blue_LS, HSV_Blue_LV])  # 蓝色范围低阈值,依次为（H,S,V）值
        upper_blue = np.array([HSV_Blue_HH, HSV_Blue_HS, HSV_Blue_HV])  # 蓝色范围高阈值，依次为（H,S,V）值
        lower_red = np.array([HSV_Red_LH, HSV_Red_LS, HSV_Red_LV])  # 红色范围低阈值，依次为（H,S,V）值
        upper_red = np.array([HSV_Red_HH, HSV_Red_HS, HSV_Red_HV])  # 红色范围高阈值，依次为（H,S,V）值
        j1 = 0  # 记录红色零件个数
        j2 = 0  # 记录蓝色零件个数

        frame= cv.imread("D:/study_work/python/static_photo/camera80.png", 1)
        hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask_blue = cv.inRange(hsv_img, lower_blue, upper_blue)
        mask_blue = cv.erode(mask_blue, None, iterations=2)
        mask_blue = cv.GaussianBlur(mask_blue, (3, 3), 0)  # 中值滤波
        mask_red = cv.inRange(hsv_img, lower_red, upper_red)
        mask_red = cv.erode(mask_red, None, iterations=2)
        mask_red = cv.GaussianBlur(mask_red, (3, 3), 0)  # 中值滤波
        cv.imwrite("D:/study_work/python/static_photo/camera84.png", mask_blue)
        cv.imwrite("D:/study_work/python/static_photo/camera85.png", mask_red)
        contours1, hierarchy1 = cv.findContours(mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        bounding_boxes1 = [cv.boundingRect(cnt1) for cnt1 in contours1]
        contours2, hierarchy2 = cv.findContours(mask_red, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        bounding_boxes2 = [cv.boundingRect(cnt2) for cnt2 in contours2]
        for bbox1 in bounding_boxes1:#蓝色
            j2 = j2 + 1
            [x, y, w, h] = bbox1
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        for bbox2 in bounding_boxes2:#红色
            j1=j1+1
            [x, y, w, h] = bbox2
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)


        cv.imwrite("D:/study_work/python/static_photo/camera86.png", frame)
        img1 = Image.open("D:/study_work/python/static_photo/camera86.png")  # 打开图片
        img1 = img1.resize((330, 330), Image.ANTIALIAS)

        img2 = Image.open("D:/study_work/python/static_photo/camera85.png")
        img2 = img2.resize((290, 290), Image.ANTIALIAS)
        img3 = Image.open("D:/study_work/python/static_photo/camera84.png")
        img3 = img3.resize((290, 290), Image.ANTIALIAS)
        photo1 = ImageTk.PhotoImage(img1)  # 用PIL模块的PhotoImage打开
        photo2 = ImageTk.PhotoImage(img2)  # 用PIL模块的PhotoImage打开
        photo3 = ImageTk.PhotoImage(img3)  # 用PIL模块的PhotoImage打开
        imglabel1 = Label(self.canvas2, image=photo1)
        imglabel1.place(x=220, y=5)
        imglabel2 = Label(self.canvas2, image=photo2)
        imglabel2.place(x=55, y=410)
        imglabel3 = Label(self.canvas2, image=photo3)
        imglabel3.place(x=420, y=410)

        self.var8.set(j2)
        self.var9.set(j1)
        label12 = tk.Label(self.canvas, text=str(self.var8.get()), width=3, font=("微软雅黑", 14), height=1, bg="white")  ##蓝色个数
        label12.place(x=160, y=92)
        label13 = tk.Label(self.canvas, text=str(self.var9.get()), width=3, font=("微软雅黑", 14), height=1, bg="white")  ##红色个数
        label13.place(x=160, y=162)
    def tkphoto(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # a = self.user_text71.get()
        # local_addr = (a, 7878)  # 默认本机任何ip ，指定端口号7878
        local_addr = ("192.168.1.189", 7878)
        udp_socket.bind(local_addr)
        send_data1 = 0.0  # 机器人关节1
        send_data2 = 0.0  # 机器人关节2
        send_data3 = 0.0  # 机器人关节3
        send_data4 = 3.0  ###运行模式标志位（1代表回原点，2代表等待位置，3.代表拍照位置，4.代表抓取）
        send_data5 = 4.0  ###检测物体标志位（1代表大圆，2代表小圆）
        send_data6 = 0.0
        byte1 = struct.pack('f', send_data1)  # folat转为4个字节
        byte2 = struct.pack('f', send_data2)
        byte3 = struct.pack('f', send_data3)
        byte4 = struct.pack('f', send_data4)
        byte5 = struct.pack('f', send_data5)
        byte6 = struct.pack('f', send_data6)

        byte = byte1 + byte2 + byte3 + byte4 + byte5+byte6
        udp_socket.sendto(byte, ("192.168.1.181", 12300))
        while True:
            self.master.update()

            recv_data = udp_socket.recvfrom(1024)
            recv_msg = recv_data[0]
            a1 = recv_msg[:4]  # 关节1实时位置
            a2 = recv_msg[4:8]  # 关节2实时位置
            a3 = recv_msg[8:12]  # 关节3实时位置
            a4 = recv_msg[12:16]  # 原点到达标志位
            a5 = recv_msg[16:20]  # 等待区到达标志位
            a6 = recv_msg[20:24]  # 拍照位置到达标志位
            a7 = recv_msg[-4:]  # 跳出WHILE循环

            m1 = struct.unpack("f", a1)
            m1 = round(float(m1[0]), 3)  # 关节1实时位置
            m1 = str(m1)
            m2 = struct.unpack("f", a2)
            m2 = round(float(m2[0]), 3)  # 关机2实时位置
            m2 = str(m2)
            m3 = struct.unpack("f", a3)
            m3 = round(float(m3[0]), 3)  # 关节3实时位置
            m3 = str(m3)
            m4 = struct.unpack("f", a4)
            m4 = int(m4[0])  # 原点到达标志位
            m5 = struct.unpack("f", a5)
            m5 = int(m5[0])  # 等待区到达标志位
            m6 = struct.unpack("f", a6)
            m6 = int(m6[0])  # 拍照位置到达标志位
            self.var1.set(m1)
            self.var2.set(m2)
            self.var3.set(m3)
            self.var4.set(m4)
            self.var5.set(m5)
            self.var7.set(m6)

            label14 = tk.Label(self.canvas, text=str(self.var1.get()), width=6, font=("微软雅黑", 14), height=1,
                               bg="white")  ##机器人关节1实时位置
            label14.place(x=216, y=232)
            label15 = tk.Label(self.canvas, text=str(self.var2.get()), width=6, font=("微软雅黑", 14), height=1,
                               bg="white")  ##机器人关节2实时位置
            label15.place(x=216, y=302)
            label16 = tk.Label(self.canvas, text=str(self.var3.get()), width=6, font=("微软雅黑", 14), height=1,
                               bg="white")  ##机器人关节3实时位置
            label16.place(x=216, y=372)
            label17 = tk.Label(self.canvas, text=str(self.var4.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##原点到达标志位
            label17.place(x=460, y=430)
            label18 = tk.Label(self.canvas, text=str(self.var5.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##等待位置到达标志位
            label18.place(x=460, y=500)
            label19 = tk.Label(self.canvas, text=str(self.var6.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##抓取位置到达标志位
            label19.place(x=460, y=570)
            label20 = tk.Label(self.canvas, text=str(self.var7.get()), width=3, font=("微软雅黑", 14), height=1,
                               bg="white")  ##拍照位置到达标志位
            label20.place(x=468, y=640)
            if m6 == 1:

                break
        udp_socket.close()
    def back(self):
        pass

if __name__ == '__main__':
    top = tk.Tk()
    basedesk(top)
    top.mainloop()