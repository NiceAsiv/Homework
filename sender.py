import sys
import socket
import random
from threading import Lock, Thread
import time
import json
import numpy as np
from queue import Queue
from binascii import crc32
from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem, QTableWidget, QSlider
from PySide2.QtCore import Slot
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader


send_lock = Lock()  # 锁
IO_lock = Lock()  # 输入数出锁


# 建立连接


class senderWithGUI:
    def __init__(self):
        self.ui = QUiLoader().load('sender.ui')
        self.ui.button_send.clicked.connect(self.getData)
        self.ui.cbox1.currentIndexChanged.connect(self.getFrame)
        self.ui.drop_Slider.setRange(0, 100)
        self.ui.drop_Slider.setTickPosition(QSlider.TicksBelow)
        self.ui.drop_Slider.setTickInterval(10)
        self.ui.drop_Slider.setValue(0)
        self.ui.drop_Slider.valueChanged.connect(self.dropRate)
        self.ui.input_data.setPlaceholderText('输入数据>>>')
        # self.ui.timeOut.clicked.connect(self.timeOut)
        self.m = 4  # 帧的头部序列号的位数
        self.Sw = 2 ** (self.m - 1)  # 发送窗口大小
        self.Smax = 2 ** self.m  # 最大序列号
        self.Sf = 0  # 待发送帧的序列号
        self.Sn = 0  # 下一个待发送帧的序列号
        self.max_time_out = 5  # 最大超时时间
        self.IO_buffer = Queue()  # 缓存帧
        self.stored_frame = dict()  # 已存储帧
        self.ip = "127.0.0.1"
        self.port = 6555
        self.sender_socket = self.connect()
        self.droprate = 0

    def connect(self):
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 建立socket
        print('正在连接接收方...')
        # sender_socket.bind(self.ipaddress)#绑定ip地址和端口
        # socket,addr=sender_socket.accept()#接受连接
        sender_socket.connect((self.ip, self.port))
        print('连接成功')
        return sender_socket

    @Slot()
    # 控制bit丢包率  0-100
    def dropRate(self):
        self.droprate = self.ui.drop_Slider.value() / 100

    @Slot()
    def getFrame(self):
        seqNo = int(self.ui.cbox1.currentText()[-1])
        self.ui.frame_view.clear()
        try:
            json_frame = json.dumps(self.stored_frame[seqNo], indent=4)
            self.ui.frame_view.append(json_frame)
        except:
            self.ui.frame_view.append('无此帧')

    @Slot()  # 槽函数
    def getData(self):
        data = self.ui.input_data.toPlainText()
        self.ui.input_data.clear()
        if data == '':
            print('输入不能为空')
            return
        if data == 'exit':
            self.sender_socket.close()
            sys.exit()
            # frame={'seq':Sn,'data':data}
        self.IO_buffer.put(data)
        # Sn+=1
        # print('IO_buffer:',IO_buffer)

    # def FrameTimer(self,seq):
    #     stored_frame_lock.acquire()
    #     self.stored_frame[seq]['create_time'] = time.time()
    #     stored_frame_lock.release()

    # 成帧·
    def MakeFrame(self, data):
        frame = {'seq': self.Sn, 'create_time': time.time(), 'data': data, 'isDone': False}
        json_frame = json.dumps(frame, indent=4)
        crc = crc32(json_frame.encode())
        frame['crc'] = crc
        print('[!]已生成frame:', frame)
        return frame

    def storeFrame(self, frame):
        self.stored_frame[frame['seq']] = frame
        print('[!]已存储frame:', frame)

    def SendFrame(self):
        # json.dumps()将Python对象编码成JSON字符串
        json_frame = json.dumps(self.stored_frame[self.Sn], indent=4)
        send_lock.acquire()
        self.sender_socket.sendall(json_frame.encode())  # 这里不能用 send,因为send只能发送1024字节
        send_lock.release()
        print('[!]已发送frame:', json_frame)
        # return json_frame

    def resendFrame(self, seq):
        # 更新本地帧
        frame = self.stored_frame[seq]
        frame['create_time'] = time.time()
        del frame['crc']
        json_frame = json.dumps(frame, indent=4).encode()
        frame['crc'] = crc32(json_frame)
        # 更新存储帧
        self.stored_frame[seq] = frame
        to_send = json.dumps(frame)
        send_lock.acquire()
        self.sender_socket.sendall(to_send.encode())
        send_lock.release()
        print('[!]已重发frame:', to_send)
        # return json_frame

    def CRCcheck(self, frame):
        recv_crc = frame['crc']
        del frame['crc']
        json_frame = json.dumps(frame, indent=4).encode()
        crc = crc32(json_frame)
        if crc != recv_crc:
            print('[!]crc校验错误')
            return False
        else:
            return True

    def RecvFrame(self):
        while True:
            json_frame = self.sender_socket.recv(1024).decode()
            frame = json.loads(json_frame)
            IO_lock.acquire()
            print('[!]已接收帧:', frame)
            IO_lock.release()
            # 重新计算crc
            if not self.CRCcheck(frame):
                IO_lock.acquire()
                print('[!]crc校验错误')
                IO_lock.release()
                continue

            if frame['data'] == 'NAK':
                nak_Seq = frame['seq']
                IO_lock.acquire()
                print('[NAK]', nak_Seq)
                IO_lock.release()
                if nak_Seq >= self.Sf and nak_Seq < self.Sn:
                    if nak_Seq < self.Sw:
                        self.ui.table1.setItem(nak_Seq, 3, QTableWidgetItem('NAK重发'))
                    else:
                        self.ui.table1.setItem(self.Sw - (self.Sn - nak_Seq), 3, QTableWidgetItem('NAK重发'))
                    time.sleep(0.8)
                    self.resendFrame(nak_Seq)

            if frame['data'] == 'ACK':
                ack_Seq = frame['seq']
                IO_lock.acquire()
                print('[ACK]', ack_Seq)
                IO_lock.release()
                if ack_Seq >= self.Sf and ack_Seq <= self.Sn:
                    while self.Sf < ack_Seq:
                        # del self.stored_frame[self.Sf]
                        self.stored_frame[self.Sf]['isDone'] = True
                        print('[!]已删除帧:', self.stored_frame[self.Sf])
                        if self.Sf < self.Sw:
                            self.ui.table1.setItem(self.Sf, 3, QTableWidgetItem('ACK'))
                        else:
                            self.ui.table1.setItem(self.Sw - (self.Sn - self.Sf), 3, QTableWidgetItem('ACK'))
                        # print('已删除帧', self.Sf)
                        self.Sf = (self.Sf + 1) % self.Sw

    # 发送帧计时器

    def timer(self):
        # start_time=self.stored_frame[seq]['create_time']
        while True:
            time.sleep(1)
            for seq in range(self.Sf, self.Sn):
                if not self.stored_frame[seq]['isDone']:
                    print(self.stored_frame[seq]['isDone'])
                    if (time.time() - self.stored_frame[seq]['create_time']) >= self.max_time_out:
                        self.resendFrame(seq)
                    # self.stored_frame[seq]['create_time'] = time.time()


    # 随机丢包
    def packLoss(self):
        np.random.seed(0)
        out = [self.droprate, 1 - self.droprate]
        poss = np.array(out)
        choice = np.random.choice(['drop', 'no'], p=poss)
        return choice

    def runner(self):
        # 启动发送机
        # Thread_of_getData = Thread(target=self.getData)  # 用户输入数据
        try:
            Thread_of_RecvFrame = Thread(target=self.RecvFrame, daemon=True)  # 接收帧
            Thread_of_timer = Thread(target=self.timer, daemon=True)  # 计时器
            # Thread_of_getData.start()
            Thread_of_RecvFrame.start()
            Thread_of_timer.start()
            while True:
                if (self.Sn - self.Sf) >= self.Sw:
                    print('[!]发送窗口已满')
                    time.sleep(1)
                    continue
                if not self.IO_buffer.empty():
                    IO_lock.acquire()
                    data = self.IO_buffer.get()
                    print('data:', data)
                    # print('Sn:', self.Sn)
                    IO_lock.release()
                    if data == 'exit':
                        break
                else:
                    time.sleep(1)
                    continue
                frame = self.MakeFrame(data)
                self.storeFrame(frame)
                randchoice = self.packLoss()
                if randchoice == 'drop':
                    self.stored_frame[self.Sn]['crc'] = self.stored_frame[self.Sn]['crc'] + 1
                self.SendFrame()
                self.ui.cbox1.addItem("帧" + str(self.Sn))
                if self.Sn < self.Sw:
                    self.ui.table1.insertRow(self.Sn)
                    self.ui.table1.setItem(self.Sn, 0, QTableWidgetItem(str(self.Sn)))
                    self.ui.table1.setItem(self.Sn, 1, QTableWidgetItem(str(data)))
                    self.ui.table1.setItem(self.Sn, 2, QTableWidgetItem("传输完成"))
                    self.ui.table1.setItem(self.Sn, 4, QTableWidgetItem(str(self.Sn+1)))
                else:
                    self.ui.table1.insertRow(self.Sw)
                    self.ui.table1.setItem(self.Sw - (self.Sn - self.Sf), 0, QTableWidgetItem(str(self.Sn)))
                    self.ui.table1.setItem(self.Sw - (self.Sn - self.Sf), 1, QTableWidgetItem(str(data)))
                    self.ui.table1.setItem(self.Sw - (self.Sn - self.Sf), 2, QTableWidgetItem("传输完成"))
                    self.ui.table1.setItem(self.Sw - (self.Sn - self.Sf), 3, QTableWidgetItem(str(self.Sw)))
                self.Sn = (self.Sn + 1) % self.Sw
                # Thread_of_timer=Thread(target=self.timer,args=(self.Sn,))

        finally:
            self.sender_socket.close()
            print('[!]发送机已关闭')

    def tester(self):
        self.getData()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    sender = senderWithGUI()
    sender.ui.show()
    thread_of_runner = Thread(target=sender.runner, daemon=True)
    thread_of_runner.start()
    sys.exit(app.exec_())
    # sender.tester()
#发送方采用了多线程，异步的实现了成帧、发送帧、接收帧、计时器、用户输入数据等功能，其中计时器和接收帧是守护线程，当主线程结束时，它们也会结束。发送方的GUI界面如下图所示。
