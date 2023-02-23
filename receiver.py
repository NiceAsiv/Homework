import sys
import time
import json
import socket
from binascii import crc32
from queue import Queue
from threading import Thread

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Slot
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication

Rn = 0  # 下一个待确定帧的序列号
NAKSent = False  # NAK帧是否已发送
ACKNeeded = False  # 是否需要发送ACK帧
MAX_RECV_BUFFER = 1024  # 接收缓冲区大小


#
# app=QApplication(sys.argv)
# ui=QUiLoader().load("receiver.ui")
# ui.setWindowTitle("接收方")
# ui.show()
# sys.exit(app.exec_())


class receiver:
    def __init__(self):
        self.Rn = 0  # 下一个待确定帧的序列号
        self.m = 4  # 帧的头部序列号的位数
        self.Rw = 2 ** (self.m - 1)  # 接收窗口大小
        self.slots = [False for _ in range(MAX_RECV_BUFFER)]  # slots用于存储接收到的帧#TODO:这里的slots是不是应该是一个队列？
        self.ipaddress = ("127.0.0.1", 6555)
        self.stored_frame = dict()  # 已存储帧
        self.re_socket = self.connect()
        self.ui = QUiLoader().load("receiver.ui")
        self.ui.setWindowTitle("接收方")
        self.ui.button_time.clicked.connect(self.TimeOut)

    def connect(self):
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 建立socket
        receiver_socket.bind(self.ipaddress)  # 绑定ip地址和端口
        receiver_socket.listen(5)  # 监听
        print('正在等待发送方连接...')
        receiver_socket, addr = receiver_socket.accept()  # 接受连接
        print(f'{self.ipaddress}接收到来自{addr}的连接')
        return receiver_socket

    @Slot()
    def TimeOut(self):
        time.sleep(10)

    def CRCcheck(self, frame):
        crc = frame['crc']
        del frame['crc']
        json_frame = json.dumps(frame, indent=4)
        if crc32(json_frame.encode()) == crc:
            return True
        else:
            return False

    def MakeFrame(self, Data):
        frame = dict()
        frame['seq'] = self.Rn
        frame['data'] = Data
        json_frame = json.dumps(frame, indent=4)
        frame['crc'] = crc32(json_frame.encode())
        return frame

    def sendACK(self):
        frame = self.MakeFrame('ACK')
        self.re_socket.sendall(json.dumps(frame).encode())
        print('[!]已发送ACK帧', frame)

    def sendNAK(self):
        frame = self.MakeFrame('NAK')
        self.re_socket.sendall(json.dumps(frame).encode())
        print('[!]已发送NAK帧')

    def getData(self, seqNo):
        data = self.stored_frame[seqNo]['data']
        print('[!]已从帧中提取数据:', data)

    def RecvFrame(self):
        global Rn, NAKSent, ACKNeeded
        while True:
            data = self.re_socket.recv(MAX_RECV_BUFFER).decode()
            if not data:
                # print('Connection closed')
                break
            frame = json.loads(data)
            SeqNo = frame['seq']
            print('[!]已接收到帧:', frame)
            # 插入到表格
            self.ui.table2.insertRow(self.ui.table2.rowCount())
            self.ui.table2.setItem(SeqNo, 0, QtWidgets.QTableWidgetItem(str(SeqNo)))
            self.ui.table2.setItem(SeqNo, 1, QtWidgets.QTableWidgetItem(str(frame['data'])))
            # 若帧已损坏且NAK帧未发送，则发送NAK帧
            if not self.CRCcheck(frame) and not NAKSent:
                print('[!]帧已损坏')
                self.sendNAK()
                self.ui.table2.setItem(SeqNo, 2, QtWidgets.QTableWidgetItem('NAK'))
                NAKSent = True
                # time.sleep(0.2)
                continue
            # 若帧不等于Rn，且未被标记
            if SeqNo != self.Rn and not NAKSent:
                self.sendNAK()
                self.ui.table2.setItem(SeqNo, 2, QtWidgets.QTableWidgetItem('NAK'))
                NAKSent = True
                print('[!]帧序列号不正确')
                if (self.Rn <= SeqNo < self.Rn + self.Rw) and not self.slots[SeqNo]:
                    self.slots[SeqNo] = True
                    self.slots[SeqNo] = True
                    self.stored_frame[SeqNo] = frame
                    while self.slots[self.Rn]:
                        self.Rn = (self.Rn + 1) % self.Rw
                    ACKNeeded = True
                # time.sleep(0.2)
            # 若帧等于或大于Rn，且未被标记
            if SeqNo == self.Rn:
                self.slots[SeqNo] = frame['data']
                while self.slots[self.Rn]:
                    self.Rn = (self.Rn + 1) % self.Rw
                ACKNeeded = True
                # time.sleep(0.2)
            if ACKNeeded:
                self.sendACK()
                self.ui.table2.setItem(SeqNo, 2, QtWidgets.QTableWidgetItem('ACK'))
                self.ui.table3.insertRow(self.ui.table3.rowCount())
                self.ui.table3.setItem(SeqNo, 0, QtWidgets.QTableWidgetItem(str(frame['data'])))
                ACKNeeded = False
                NAKSent = False

    def runner(self):
        self.RecvFrame()
        # self.socket.close()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    receiver = receiver()
    receiver.ui.show()
    thread_of_runner = Thread(target=receiver.runner)
    thread_of_runner.start()
    sys.exit(app.exec_())
