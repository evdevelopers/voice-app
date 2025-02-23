import os
import sys
from audio import AudioReceiver, ServerConnection
import socket
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QTimer,QDateTime, QCoreApplication, QObject, QThread, pyqtSignal
from bluetooth import *
import subprocess
import speaker
import subprocess
from time import sleep, time
from bluetooth_battery import BatteryStateQuerier, BatteryQueryError, BluetoothError
from threading import Thread
import psutil


class AlertDialog(QtWidgets.QDialog):
    def __init__(self , title, qst, yes, no):
        super().__init__()

        self.setWindowTitle(title)

        # self.setFixedSize(300, 200)
        self.setFixedHeight(200)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel(qst)
        space = QtWidgets.QLabel("")
        self.layout.addWidget(message)
        self.layout.addWidget(space)

        self.hlayout = QtWidgets.QHBoxLayout()

        self.yes_btn = QtWidgets.QPushButton(text=yes)
        self.yes_btn.setFixedHeight(50)
        self.no_btn = QtWidgets.QPushButton(text=no)
        self.no_btn.setFixedHeight(50)
        self.hlayout.addWidget(self.yes_btn)
        self.hlayout.addWidget(self.no_btn)
        self.layout.addLayout(self.hlayout)
        self.setLayout(self.layout)

        self.yes_btn.clicked.connect(self.yes_action)
        self.no_btn.clicked.connect(self.no_action)


    def yes_action(self):
        # print("yes")
        self.accept()

    def no_action(self):
        # print("no")
        self.reject()

# class CustomDialog(QtWidgets.QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         self.interface = "eth0"
#         # self.interface = "wlan0"

#         # self.setWindowTitle("Room Info")

#         self.setFixedWidth(500)
#         self.setFixedHeight(350)

#         QBtn = QtWidgets.QDialogButtonBox.Cancel

#         self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
#         # self.buttonBox.accepted.connect(self.accept)
#         self.buttonBox.rejected.connect(self.reject)

#         self.layout = QtWidgets.QVBoxLayout()
#         # self.frame_2 = QtWidgets.QFrame()
#         # self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         # self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
#         # self.frame_2.setObjectName("frame_2")
#         # self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
#         # self.verticalLayout_2.setObjectName("verticalLayout_2")
#         self.label = QtWidgets.QLabel()
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
#         self.label.setSizePolicy(sizePolicy)
#         font = QtGui.QFont()
#         font.setPointSize(16)
#         font.setBold(True)
#         font.setWeight(75)
#         self.label.setFont(font)
#         self.label.setAlignment(QtCore.Qt.AlignCenter)
#         self.label.setObjectName("label")
#         # self.label.mousePressEvent = self.closeWindow

#         # self.verticalLayout_2.addWidget(self.label)
#         self.line = QtWidgets.QFrame()
#         self.line.setFrameShape(QtWidgets.QFrame.HLine)
#         self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
#         self.line.setObjectName("line")

#         self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
#         self.horizontalLayout_5.setObjectName("horizontalLayout_5")
#         self.label_6 = QtWidgets.QLabel()
#         self.label_6.setAlignment(QtCore.Qt.AlignCenter)
#         self.label_6.setObjectName("label_6")
        
#         self.line_4 = QtWidgets.QFrame()
#         self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
#         self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
#         self.line_4.setObjectName("line_4")
        
#         self.label_ip = QtWidgets.QLabel()
#         self.label_ip.setAlignment(QtCore.Qt.AlignCenter)
#         self.label_ip.setObjectName("label_ip")
        
#         self.horizontalLayout_5.addWidget(self.label_ip)
#         self.horizontalLayout_5.addWidget(self.line_4)
#         self.horizontalLayout_5.addWidget(self.label_6)
        
#         self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
#         self.horizontalLayout_9.setObjectName("horizontalLayout_9")
#         self.label_9 = QtWidgets.QLabel()
#         self.label_9.setAlignment(QtCore.Qt.AlignCenter)
#         self.label_9.setObjectName("label_9")
#         self.label_9.setText("الحالة")
        
#         self.line_9 = QtWidgets.QFrame()
#         self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
#         self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
#         self.line_9.setObjectName("line_9")
        
#         self.label_ip_connection = QtWidgets.QLabel()
#         self.label_ip_connection.setAlignment(QtCore.Qt.AlignCenter)
#         self.label_ip_connection.setObjectName("label_ip_connection")

#         self.horizontalLayout_9.addWidget(self.label_ip_connection)
#         self.horizontalLayout_9.addWidget(self.line_9)
#         self.horizontalLayout_9.addWidget(self.label_9)

#         self.line_mid = QtWidgets.QFrame()
#         self.line_mid.setFrameShape(QtWidgets.QFrame.HLine)
#         self.line_mid.setFrameShadow(QtWidgets.QFrame.Sunken)
#         self.line_mid.setObjectName("line_end")

#         self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
#         self.label_16 = QtWidgets.QLabel()
#         self.label_16.setAlignment(QtCore.Qt.AlignCenter)
#         self.label_16.setText("static ip")
#         self.horizontalLayout_15.addWidget(self.label_16)
#         self.line_14 = QtWidgets.QFrame()
#         self.line_14.setFrameShape(QtWidgets.QFrame.VLine)
#         self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
#         self.horizontalLayout_15.addWidget(self.line_14)
#         # self.label_ip2 = QtWidgets.QLabel()
#         # self.label_ip2.setAlignment(QtCore.Qt.AlignCenter)
#         self.edit_ip = QtWidgets.QLineEdit()
#         self.horizontalLayout_15.addWidget(self.edit_ip)
        
#         self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
#         self.staticip_button = QtWidgets.QPushButton()
#         self.staticip_button.clicked.connect(self.actionIP)
#         self.staticip_button.setText("set new static ip")
#         self.horizontalLayout_19.addWidget(self.staticip_button)
#         # self.line_19 = QtWidgets.QFrame()
#         # self.line_19.setFrameShape(QtWidgets.QFrame.VLine)
#         # self.line_19.setFrameShadow(QtWidgets.QFrame.Sunken)
#         # self.horizontalLayout_19.addWidget(self.line_19)

#         self.line_end = QtWidgets.QFrame()
#         self.line_end.setFrameShape(QtWidgets.QFrame.HLine)
#         self.line_end.setFrameShadow(QtWidgets.QFrame.Sunken)
#         self.line_end.setObjectName("line_end")

#         self.label.setText("بيانات الاتصال")
#         self.layout.addWidget(self.label)
#         self.layout.addWidget(self.line)
#         self.layout.addLayout(self.horizontalLayout_5)
#         self.layout.addLayout(self.horizontalLayout_9)
#         # self.layout.addWidget(self.line_mid)
#         # self.layout.addLayout(self.horizontalLayout_15)
#         # self.layout.addLayout(self.horizontalLayout_19)
#         self.layout.addWidget(self.line_end)
        
#         # self.layout.addWidget(self.buttonBox)

#         self.hlayout = QtWidgets.QHBoxLayout()

#         self.yes_btn = QtWidgets.QPushButton(text="إغلاق")
#         self.yes_btn.clicked.connect(self.yes_action)
#         self.hlayout.addWidget(self.yes_btn)
#         self.layout.addLayout(self.hlayout)

#         self.setLayout(self.layout)

#         self.running = self.getRunning()
#         self.ip = self.getIP(self.interface)
#         self.label_6.setText("IP العنوان")
#         if(self.ip!=None): self.label_ip.setText(self.ip)

#         if (self.running):
#             self.label_ip_connection.setText("متصل")
#             self.label_ip_connection.setStyleSheet("color: green;")
#         else:
#             self.label_ip_connection.setText("غير متصل")
#             self.label_ip_connection.setStyleSheet("color: red;")
        
#         self.timer_check_ip = QTimer(self)
#         self.timer_check_ip.timeout.connect(self.checkIP)
#         self.timer_check_ip.start(3000)

#     def yes_action(self):
#         self.reject()

#     def getRunning(self):
#         running = False
#         try:
#             my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#             my_socket.connect(("8.8.8.8", 80))
#             # ip = my_socket.getsockname()[0]
#             # print('Your IP Address is',ip)
#             running = True
#         except:
#             running = False
#         return running
    
#     def getIP(self, interface):
#         ip = None
#         proc = subprocess.Popen('ifconfig ' + interface, shell=True, stdout=subprocess.PIPE)
#         stdout = proc.communicate()[0].decode()
#         proc.wait()
#         # print(stdout)
#         ip = stdout.split("\n")[1].strip().split(" ")[1].strip()
#         # print("ip : ", ip)
#         if (len(ip.split("."))!=4):
#             ip = None

#         return ip
        
#     def setIP(self, old, new):
#         fname= "/etc/dhcpcd.conf"
#         file = open(fname, 'r')
#         content = file.read()
#         i = 0
#         n = 0
#         for line in content.split('\n'):
#             if (self.interface in line):
#                 if (line[0]!="#"):
#                     n = i
#             i += 1
#         if (n>0):
#             m = n + 1
#             old_ip = content.split('\n')[m].split("=")[1].split("/")[0]
#             content = content.replace(old, new)
#         else:
#             new_config = "\n\ninterface "+ self.interface + "\n" +  "static ip_address="+ new +"/24\n" + "static routers=192.168.31.1\n" + "static domain_name_servers=192.168.31.1\n"
#             content += new_config
#         file = open(fname, 'w')
#         file.write(content)
#         os.system("sudo ifconfig " + self.interface + " down")
#         os.system("sudo ifconfig " + self.interface + " up")
#         sleep(4)
#         # print("restart networking service")
#         os.system("sudo service networking restart")
#         sleep(8)
#         # print("DONE")


#     def setStaticIP(self, static_ip):
#         ip = self.getIP(self.interface)
#         # print("Old System IP : " , ip)
#         self.setIP(ip, static_ip)
#         ip = self.getIP(self.interface)
#         # print("New System IP : " , ip)

#         return True
#         #if (ip==static_ip): return True
#         #else: return False

#     def actionIP(self):
#         newIP = self.edit_ip.text()
#         if (len(newIP.split("."))==4):
#             # print(newIP)
#             self.alert(newIP)

#     def alert(self, ip):
#         reply = QMessageBox.question(self, 'Set Static IP', 'Are you sure you want to set static ip to : ' + ip + ' ?\nSystem reboot after setting static ip',
#         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#         if reply == QMessageBox.Yes:
#             self.waiting()
#             done = self.setStaticIP(ip)
#             if (done):
#                 # print("DONE")
#                 # print("Rebooting")
#                 os.system("echo voicetoall | sudo reboot")

#     def waiting(self):
#         reply = QMessageBox.question(self, 'Processing', 'Please wait...',
#         QMessageBox.No, QMessageBox.No)
    
#     def checkIP(self):
#         self.running = self.getRunning()
#         self.ip = self.getIP(self.interface)
#         if (self.ip!=None): self.label_ip.setText(self.ip)

#         if (self.running):
#             self.label_ip_connection.setText("متصل")
#             self.label_ip_connection.setStyleSheet("color: green;")
#         else:
#             self.label_ip_connection.setText("غير متصل")
#             self.label_ip_connection.setStyleSheet("color: red;")


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        self.speaker = speaker.Speaker()
        self.assets = self.resource_path("assets")
        self.room = ""
        self.interface = "eth0"
        # self.interface = "wlan0"
        self.system_title = "نظام التواصل الصوتي"
        self.devs = []
        self.speaking_status = False
        self.once = False
        self.scanning = False
        self.ip = self.getIP(self.interface)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_title = QtWidgets.QLabel()
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setText(self.system_title)
        self.label_title.setStyleSheet("background-color: grey; color: white;")
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setFixedHeight(50)
        self.label_title.mousePressEvent = self.closeWindow

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.label_title)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame()
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        # font.setWeight(60)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        # self.label.mousePressEvent = self.closeWindow

        self.verticalLayout_2.addWidget(self.label)
        
        self.line = QtWidgets.QFrame(self.frame_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.line_4 = QtWidgets.QFrame(self.frame_2)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_5.addWidget(self.line_4)
        self.label_ip = QtWidgets.QLabel(self.frame_2)
        self.label_ip.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ip.setObjectName("label_ip")
        self.horizontalLayout_5.addWidget(self.label_ip)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_6.addWidget(self.label_8)
        self.line_5 = QtWidgets.QFrame(self.frame_2)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout_6.addWidget(self.line_5)
        self.label_ip_connection = QtWidgets.QLabel(self.frame_2)
        self.label_ip_connection.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ip_connection.setObjectName("label_ip_connection")
        self.horizontalLayout_6.addWidget(self.label_ip_connection)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 2)
        self.verticalLayout_2.setStretch(3, 2)

        self.frame_1 = QtWidgets.QFrame(self.centralwidget)
        self.frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setObjectName("frame_1")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.frame_1)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.label1 = QtWidgets.QLabel(self.frame_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label1.sizePolicy().hasHeightForWidth())
        self.label1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(70)
        self.label1.setFont(font)
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setObjectName("label1")
        # self.label1.mousePressEvent = self.closeWindow
        self.verticalLayout_21.addWidget(self.label1)
        self.line1 = QtWidgets.QFrame(self.frame_1)
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line1.setObjectName("line1")
        self.verticalLayout_21.addWidget(self.line1)

        self.horizontalLayout_select = QtWidgets.QHBoxLayout()
        self.horizontalLayout_select2 = QtWidgets.QHBoxLayout()
        self.label_select = QtWidgets.QLabel()
        self.label_select.setText("اختر السماعة")

        self.cb = QtWidgets.QComboBox()
        self.cb.setFixedHeight(80)
        # self.cb.currentIndexChanged.connect(self.selectPairedSpeaker)

        self.connect_paired_button = QtWidgets.QPushButton()
        self.connect_paired_button.setText("اتصال")
        self.connect_paired_button.setFixedHeight(100)
        self.connect_paired_button.clicked.connect(self.selectPairedSpeaker)

        self.horizontalLayout_select2.addWidget(self.connect_paired_button)
        self.horizontalLayout_select.addWidget(self.cb, 2)
        self.horizontalLayout_select.addWidget(self.label_select, 1)
        
        self.verticalLayout_21.addLayout(self.horizontalLayout_select)
        self.verticalLayout_21.addLayout(self.horizontalLayout_select2)

        self.line__ = QtWidgets.QFrame()
        self.line__.setFrameShape(QtWidgets.QFrame.HLine)
        self.line__.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout_21.addWidget(self.line__)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.label_2 = QtWidgets.QLabel(self.frame_1)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.line_2 = QtWidgets.QFrame()
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_speaker_name = QtWidgets.QLabel()
        self.label_speaker_name.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout_4.addWidget(self.label_speaker_name)
        self.horizontalLayout_4.addWidget(self.line_2)
        self.horizontalLayout_4.addWidget(self.label_2)

        self.verticalLayout_21.addLayout(self.horizontalLayout_4)
        
        self.horizontalLayout_battery = QtWidgets.QHBoxLayout()
        self.label_battery_text = QtWidgets.QLabel()
        self.label_battery_text.setAlignment(QtCore.Qt.AlignCenter)
        self.label_battery_text.setText("البطارية")
        self.line_battery = QtWidgets.QFrame()
        self.line_battery.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_battery.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_battery_level = QtWidgets.QLabel()
        self.label_battery_level.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout_battery.addWidget(self.label_battery_level)
        self.horizontalLayout_battery.addWidget(self.line_battery)
        self.horizontalLayout_battery.addWidget(self.label_battery_text)

        self.verticalLayout_21.addLayout(self.horizontalLayout_battery)

        # self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        # self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        # self.label_4 = QtWidgets.QLabel(self.frame_1)
        # self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_4.setObjectName("label_4")
        # self.horizontalLayout_3.addWidget(self.label_4)
        # self.line_3 = QtWidgets.QFrame(self.frame_1)
        # self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        # self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.line_3.setObjectName("line_3")
        # self.horizontalLayout_3.addWidget(self.line_3)
        # self.label_speaker_connection = QtWidgets.QLabel(self.frame_1)
        # self.label_speaker_connection.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_speaker_connection.setObjectName("label_speaker_connection")


        # self.MovieLabel = QLabel(self)
        # Set gif content to be same size as window (600px / 400px)
        # self.MovieLabel.setGeometry(QtCore.QRect(0, 0, 600, 400))
        # gifFile = self.assets +  "/voice.gif"
        # self.movie = QtGui.QMovie(gifFile)
        # self.label_speaker_connection.setMovie(self.movie)
        # self.movie.start()

        # self.horizontalLayout_3.addWidget(self.label_speaker_connection)
        # self.horizontalLayout_3.addWidget(self.line_3)
        # self.horizontalLayout_3.addWidget(self.label_4)

        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.label_14 = QtWidgets.QLabel(self.frame_1)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setText("اتصال")
        # self.horizontalLayout_13.addWidget(self.label_14)
        self.line_13 = QtWidgets.QFrame(self.frame_1)
        self.line_13.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.horizontalLayout_13.addWidget(self.line_13)

        self.label_speaker_action = QtWidgets.QWidget()
        self.label_speaker_action.setObjectName("label_speaker_action")

        self.button_speaker_action = QtWidgets.QPushButton()
        self.button_speaker_action.setObjectName("button_speaker_action")
        self.button_speaker_action.setText("-")
        self.button_speaker_action.clicked.connect(self.disconnect_speaker)
        self.button_speaker_action.setEnabled(False)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.button_speaker_action)
        self.label_speaker_action.setLayout(self.button_layout)

  
        self.horizontalLayout_13.addWidget(self.label_speaker_action)
        self.horizontalLayout_13.addWidget(self.line_13)
        self.horizontalLayout_13.addWidget(self.label_14)

        # self.verticalLayout_21.addLayout(self.horizontalLayout_3)
        self.verticalLayout_21.addLayout(self.horizontalLayout_13)
        self.verticalLayout_21.setStretch(0, 1)
        self.verticalLayout_21.setStretch(1, 1)
        self.verticalLayout_21.setStretch(2, 3)
        self.verticalLayout_21.setStretch(3, 3)
        self.verticalLayout_21.setStretch(4, 1)
        self.verticalLayout_21.setStretch(5, 1)
        self.verticalLayout_21.setStretch(6, 1)
        self.verticalLayout_21.setStretch(7, 1)

        # self.horizontalLayout.addWidget(self.frame_1)
        self.verticalLayout.addLayout(self.horizontalLayout)


        self.frame = QtWidgets.QFrame()
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        
        # self.btn_info = QtWidgets.QPushButton()
        # self.btn_info.setText("معلومات الاتصال")
        # self.btn_info.clicked.connect(self.button_clicked)
        # self.connection_status = self.getRunning()
        # if (self.connection_status): 
        #     self.btn_info.setStyleSheet("background-color: green;")
        # else:
        #     self.btn_info.setStyleSheet("background-color: red;")
        
        ######################################## IP_CONNECT

        self.layout_ip = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(70)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        # self.label.mousePressEvent = self.closeWindow

        # self.verticalLayout_2.addWidget(self.label)
        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.line.setObjectName("line")

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        # self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel()
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_6.setObjectName("label_6")
        
        self.line_4 = QtWidgets.QFrame()
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.line_4.setObjectName("line_4")
        
        self.label_ip = QtWidgets.QLabel()
        self.label_ip.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_ip.setObjectName("label_ip")
        
        self.horizontalLayout_5.addWidget(self.label_ip)
        self.horizontalLayout_5.addWidget(self.line_4)
        self.horizontalLayout_5.addWidget(self.label_6)
        
        self.horizontalLayout_5_ = QtWidgets.QHBoxLayout()

        self.label_6_ = QtWidgets.QLabel()
        self.label_6_.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6_.setText("المعالج")
        self.line_4_ = QtWidgets.QFrame()
        self.line_4_.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4_.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_cpu = QtWidgets.QLabel()
        self.label_cpu.setAlignment(QtCore.Qt.AlignCenter)

        cpu_temp = self.get_cpu_temperature()
        cpu_percent = psutil.cpu_percent(1)
        # self.label_cpu.setText(str(cpu_temp) + " C" + " | " + str(cpu_percent) + "%")

        self.horizontalLayout_5_.addWidget(self.label_cpu)
        self.horizontalLayout_5_.addWidget(self.line_4_)
        self.horizontalLayout_5_.addWidget(self.label_6_)

        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        # self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_9 = QtWidgets.QLabel()
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_9.setObjectName("label_9")
        self.label_9.setText("الحالة")
        
        self.line_9 = QtWidgets.QFrame()
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.line_9.setObjectName("line_9")
        
        self.label_ip_connection = QtWidgets.QLabel()
        self.label_ip_connection.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_ip_connection.setObjectName("label_ip_connection")

        self.horizontalLayout_9.addWidget(self.label_ip_connection)
        self.horizontalLayout_9.addWidget(self.line_9)
        self.horizontalLayout_9.addWidget(self.label_9)

        self.label.setText("بيانات الاتصال")
        self.layout_ip.addWidget(self.label)
        self.layout_ip.addWidget(self.line)
        self.layout_ip.addLayout(self.horizontalLayout_5)
        self.layout_ip.addLayout(self.horizontalLayout_9)
        # self.layout_ip.addLayout(self.horizontalLayout_5_)
        # self.layout.addWidget(self.line_mid)
        # self.layout.addLayout(self.horizontalLayout_15)
        # self.layout.addLayout(self.horizontalLayout_19)
 
        # self.layout.addWidget(self.buttonBox)

        # self.hlayout = QtWidgets.QHBoxLayout()

        # self.yes_btn = QtWidgets.QPushButton(text="إغلاق")
        # self.yes_btn.clicked.connect(self.yes_action)
        # self.hlayout.addWidget(self.yes_btn)
        # self.layout.addLayout(self.hlayout)

        # self.setLayout(self.layout)

        self.running = self.getRunning()
        self.ip = self.getIP(self.interface)
        self.label_6.setText("IP العنوان")
        if(self.ip!=None): self.label_ip.setText(self.ip)

        if (self.running):
            self.label_ip_connection.setText("متصل")
            self.label_ip_connection.setStyleSheet("color: green;")
        else:
            self.label_ip_connection.setText("غير متصل")
            self.label_ip_connection.setStyleSheet("color: red;")

        #####################################################
        
        # self.label_10 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        # self.label_10.setFont(font)
        # self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_10.setObjectName("label_10")
        # self.verticalLayout_3.addWidget(self.btn_info)
        self.verticalLayout_3.addLayout(self.layout_ip)
        # self.verticalLayout_3.addWidget(self.label_10)
        self.line_6 = QtWidgets.QFrame(self.frame)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_3.addWidget(self.line_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_11 = QtWidgets.QLabel()
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")

        self.line_16 = QtWidgets.QFrame()
        self.line_16.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        
        self.label_streaming_status = QtWidgets.QLabel(self.frame)
        self.label_streaming_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_streaming_status.setObjectName("label_streaming_status")

        # gifFile = self.assets +  "/voice.gif"
        # self.movie = QtGui.QMovie(gifFile)
        # self.label_streaming_status.setMovie(self.movie)
        # self.movie.start()
        imgFile = self.assets +  "/mute2.png"
        self.label_streaming_status.setPixmap(QtGui.QPixmap(imgFile))
        
        self.horizontalLayout_7.addWidget(self.label_streaming_status)
        # self.horizontalLayout_7.addWidget(self.line_16)
        # self.horizontalLayout_7.addWidget(self.label_11)
        
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        
        # add slider
        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        # self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider.setTickInterval(5)
        self.slider.setSingleStep(1)
        try:
            self.slider.setValue(float(self.get_volume()))
        except:
            self.slider.setValue(0.0)
        self.slider.valueChanged.connect(self.valuechange)
        self.slider.setMinimumSize(0, 40)
       
        self.label_volume_title = QtWidgets.QLabel()
        self.label_volume_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_volume_title.setText("الصوت")

        self.label_volume_value = QtWidgets.QLabel()
        self.label_volume_value.setAlignment(QtCore.Qt.AlignCenter)
        self.label_volume_value.setText(" " + str(self.get_volume()) + "%")

        self.button_decrease = QtWidgets.QPushButton()
        # self.button_decrease.setText("-")
        self.button_decrease.clicked.connect(lambda: self.add_volume(-10))
        self.button_decrease.setFixedWidth(50)
        self.button_decrease.setFixedHeight(50)
        self.button_decrease.setIcon(QtGui.QIcon(QtGui.QPixmap(self.assets +  "/volume_minus.png")))
        self.button_decrease.setIconSize(QtCore.QSize(40,40))
        # font = self.button_decrease.font()
        # font.setBold(True)
        # font.setPointSize(16)
        # self.button_decrease.setFont(font)

        self.button_increase = QtWidgets.QPushButton()
        # self.button_increase.setText("+")
        self.button_increase.clicked.connect(lambda: self.add_volume(10))
        self.button_increase.setFixedWidth(50)
        self.button_increase.setFixedHeight(50)
        self.button_increase.setIcon(QtGui.QIcon(QtGui.QPixmap(self.assets +  "/volume_plus.png")))
        self.button_increase.setIconSize(QtCore.QSize(40,40))
        # font = self.button_increase.font()
        # font.setBold(True)
        # font.setPointSize(16)
        # self.button_increase.setFont(font)


        # self.horizontalLayout_8.addWidget(self.label_volume_title)
        self.horizontalLayout_8.addWidget(self.button_decrease)
        self.horizontalLayout_8.addWidget(self.slider)
        self.horizontalLayout_8.addWidget(self.button_increase)
        # self.horizontalLayout_8.addWidget(self.label_volume_value)

        # self.horizontalLayout_8.setStretch(0, 0)
        # self.horizontalLayout_8.setStretch(1, 1)
        # self.horizontalLayout_8.setStretch(2, 0)

        self.label_volume_value.setFixedHeight(30)
        
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.verticalLayout_3.addWidget(self.label_volume_value)
        self.horizontalLayout.addWidget(self.frame)

        self.verticalLayout_3.setStretch(5,0)
        # self.horizontalLayout.addWidget(self.frame_1)
      
        self.frame_4 = QtWidgets.QFrame()
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")

        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        # self.label_room = QtWidgets.QLabel()
        # self.label_room.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_room.setText("---")
        self.scrollArea = QtWidgets.QScrollArea(self.frame_4)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 351, 187))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.devicesLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.devicesLayout.setObjectName("devicesLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        self.label_room = QtWidgets.QLabel()
        self.label_room.setAlignment(QtCore.Qt.AlignCenter)
        self.label_room.setText("---")
        self.label_room.setStyleSheet("background-color: grey; color: white;")
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(70)
        self.label_room.setFont(font)
        self.label_room.setFixedHeight(50)

        self.verticalLayout_4.addWidget(self.label_room)
        self.verticalLayout_4.addWidget(self.scrollArea)

        # self.button_layout = QtWidgets.QHBoxLayout()
        self.h_layout = QtWidgets.QVBoxLayout(self.frame_4)
        self.button_scan = QtWidgets.QPushButton(self.frame_4)
        self.button_scan.setObjectName("button_scan")
        self.button_scan.clicked.connect(self.scan)
        self.button_scan.setFixedHeight(60)
        self.button_scan_reset = QtWidgets.QPushButton(self.frame_4)
        self.button_scan_reset.setObjectName("button_scan_reset")
        self.button_scan_reset.setText("حذف النتائج")
        self.button_scan_reset.setFixedHeight(60)
        self.button_scan_reset.clicked.connect(self.resetScan)
        # self.button_scan_reset.setContentsMargins(10,20,10, 0)

        self.h_layout.addWidget(self.button_scan)
        self.h_layout.addWidget(self.button_scan_reset)
        # self.h_layout.setStretch(0, 0)

        self.h_widget = QtWidgets.QWidget(self.frame_4)
        self.h_widget.setLayout(self.h_layout)

        self.verticalLayout_4.addWidget(self.h_widget)
        self.speaking(False)

        self.horizontalLayout.addWidget(self.frame_4)
        self.horizontalLayout.addWidget(self.frame_1)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        # self.info = CustomDialog(self)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        device, paired = self.speaker.check_devices()
        # print("connected device : ", device)
        if (device):
            self.label_speaker_name.setText(device["name"])
            # self.label_speaker_connection.setText("متصل")

        self.setup_server()
        self.start_server()

        # self.timer_check = QTimer(self)
        # self.timer_check.timeout.connect(self.checkInfo)
        # self.timer_check.start(3000)

        # self.thread = QThread()
        # self.thread.started.connect(self.checkingLoop)
        # self.thread.start()
        # self.thread.finished.connect(self.Quit_)

        self.th = Thread(target=self.checkingLoop, daemon=True)
        self.th.start()


        self.timer_clientcheck = QTimer(self)
        self.timer_clientcheck.timeout.connect(self.ListenScanning)
        self.timer_clientcheck.start(2000)

        self.speak_timer = None
        # self.speak_timer = QTimer(self)
        # self.speak_timer.timeout.connect(self.StartSpeaking)
    
    def processcheck(self):
        process_name = "control-panel"
        for p in psutil.process_iter():
            if (process_name in p.name()):
                cpu = p.cpu_percent(1)
                # print(p.name() + " : " + str(p.pid) + " : " + str(cpu))
                # if(cpu==0):
                #     print("killing process " , cpu)
                #     os.system("sudo kill -9 " + str(p.pid))
                # if(cpu >= 98):
                #     print("reboot : ", cpu)
                #     os.system("sudo reboot")

    def Quit_(self):
        self.thread.deleteLater
        exit()
        quit()
        sys.exit()
        print(y)

    def get_cpu_temperature(self):
        # Initialize the result.
        result = 0.0
        # The first line in this file holds the CPU temperature as an integer times 1000.
        # Read the first line and remove the newline character at the end of the string.
        if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
            with open('/sys/class/thermal/thermal_zone0/temp') as f:
                line = f.readline().strip()
            # Test if the string is an integer as expected.
            if line.isdigit():
                # Convert the string with the CPU temperature to a float in degrees Celsius.
                result = float(line) / 1000
        # Give the result back to the caller.
        result = int(result)
        return result

    def checkingLoop(self):
        print("start checkingLoop")
        self.last = time()
        # self.timer_check = QTimer(self)
        # self.timer_check.timeout.connect(self.checkInfo)
        # self.timer_check.start(2000)
        while True:
            try:
                self.checkInfo()
            except:
                pass
            sleep(2)

    def getRunning(self):
        running = False
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.connect(("8.8.8.8", 80))
            running = True
        except:
            running = False
        return running
    

    def selectPairedSpeaker(self):
        try:
            i = self.cb.currentIndex()
            # print("index: " , i)
            self.connect_dev(None, self.paired[i])
        except:
            pass

    def getPowerLevel(self, mac):
        result = -1
        try:
            query = BatteryStateQuerier(mac)
            result = int(query)  # returns integer between 0 and 100
            # print(result)
        except:
            pass
        
        return result

    def getIP(self, interface):
        ip = None
        proc = subprocess.Popen('ifconfig ' + interface, shell=True, stdout=subprocess.PIPE)
        stdout = proc.communicate()[0].decode()
        proc.wait()
        # print(stdout)
        ip = stdout.split("\n")[1].strip().split(" ")[1].strip()
        # print("ip : ", ip)
        if (len(ip.split("."))!=4):
            ip = None

        return ip
    
    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)


    def speaking(self, status):
        if (status):
            # gifFile = self.assets +  "/voice.gif"
            # self.movie = QtGui.QMovie(gifFile)
            # self.label_streaming_status.setMovie(self.movie)
            # self.movie.start()
            imgFile = self.assets +  "/speak.png"
            self.label_streaming_status.setPixmap(QtGui.QPixmap(imgFile))
        else:
            imgFile = self.assets +  "/mute2.png"
            self.label_streaming_status.setPixmap(QtGui.QPixmap(imgFile))
        
        
    def add_volume(self, vol):
        v = int(self.get_volume())
        v += vol
        if (v>100): v = 100
        elif (v<0): v = 0
        self.set_volume(v)
        self.slider.setValue(v)

    def button_clicked(self, s):
        if self.info.exec():
            print("Success!")
        else:
            print("Cancel!")

    def valuechange(self, value):
        self.set_volume(value)
        self.label_volume_value.setText(" " + str(self.get_volume()) + "%")

    def addActionButton(self):
        # self.button_layout = QtWidgets.QHBoxLayout()
        self.clearActionButton()
        # self.button_speaker_action = QtWidgets.QPushButton()
        # self.button_speaker_action.setObjectName("button_speaker_action")
        self.button_speaker_action.setText("إلغاء الاتصال")
        self.button_speaker_action.clicked.connect(self.disconnect_speaker)
        self.button_speaker_action.setEnabled(True)
        # self.button_layout.addWidget(self.button_speaker_action)
        # self.label_speaker_action.setLayout(self.button_layout)

    def clearActionButton(self):
        # self.clearLayout(self.button_layout)
        self.button_speaker_action.setText("-")
        # self.button_speaker_action.clicked.connect(self.disconnect_speaker)
        self.button_speaker_action.setEnabled(False)

    def resetScan(self):
        self.clearLayout(self.devicesLayout)

    def scan(self):
        self.resetScan()
        self.loading()
        self.button_scan.setEnabled(False)
        self.button_scan_reset.setEnabled(False)
        # self.scan_timer = QTimer(self)
        # self.scan_timer.timeout.connect(self.Scanning)
        # self.scan_timer.start(10)
        self.scan_thread = Thread(target=self.Scanning, daemon=True)
        self.scan_thread.start()


    def disconnect_speaker(self):
        # print("disconnect")
        self.speaker.disconnect()

    def ListenScanning(self):
        if (len(self.devs)>0):
            # print(self.devs)
            self.resetScan()
            for dev in self.devs:
                self.device_node(dev)
            self.devs = []


    def Scanning(self):
        print("Scanning...")
        self.speaker.scan_devices_cmd()
        # print("Scanning devs...")
        self.devs = self.speaker.scan_devices()
        print("devs: " , self.devs)
        self.resetScan()
        self.scanning = False
        try:
            if self.device: self.button_scan.setEnabled(False)
            else: self.button_scan.setEnabled(True)
        except:
            self.button_scan.setEnabled(True)
        self.button_scan_reset.setEnabled(True)
        # print(devs)
        # self.resetScan()
        # for dev in devs:
        #     self.device_node(dev)
        # self.scan_timer.stop()
        # self.spinner.stop()
        
    def device_node(self, dev):
        devLayout = QtWidgets.QHBoxLayout()
        devlabel_1 = QtWidgets.QLabel(self.scrollArea)
        devlabel_1.setAlignment(QtCore.Qt.AlignCenter)
        devlabel_1.setText(dev["name"])
        devLayout.addWidget(devlabel_1)
        devline_1 = QtWidgets.QFrame(self.frame_4)
        devline_1.setFrameShape(QtWidgets.QFrame.VLine)
        devline_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        # devline_1.setObjectName("devline_1")
        devLayout.addWidget(devline_1)
        dev_status = QtWidgets.QLabel(self.scrollArea)
        dev_status.setAlignment(QtCore.Qt.AlignCenter)
        # dev_status.setObjectName("dev_status")
        dev_status.setText(dev["mac"])
        devLayout.addWidget(dev_status)
        # frame = QtWidgets.QFrame()
        frame = QtWidgets.QGroupBox("")
        frame.setFixedHeight(100)
        frame.setLayout(devLayout)
        frame.mousePressEvent = lambda a: self.connect_dev(a, dev)

        # frame.setStyleSheet("QGroupBox#dframe{background-color:grey}")
        self.devicesLayout.addWidget(frame)
    
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def connect_dev(self, event, dev):
        # print("clicked : " , dev)
        # reply = QMessageBox.question(self, 'اتصال', 'هل أنت متأكد من الاتصال ب '+ dev["name"]  +' ؟',
        # QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # if reply == QMessageBox.Yes:
        #     # event.accept()
        #     connected = self.speaker.connectTo(dev["mac"])
        #     if (connected):
        #         print("connected")
        #         self.label_speaker_name.setText(dev["name"])
        #         self.label_speaker_connection.setText("متصل")
        #         self.resetScan()
        #         self.once = False

        dlg = AlertDialog('اتصال', 'هل أنت متأكد من الاتصال ب '+ dev["name"]  +' ؟', "نعم", "لا")
        if dlg.exec():
            # print("Yes!")
            connected = self.speaker.connectTo(dev["mac"])
            if (connected):
                # print("connected")
                self.label_speaker_name.setText(dev["name"])
                # self.label_speaker_connection.setText("متصل")
                self.resetScan()
                self.once = False


    def checkPairedSpeakers(self):
        device, self.paired = self.speaker.check_devices()
        if (device==None):
            # self.once = False
            self.cb.clear()
            for pair in self.paired:
                self.cb.addItem(pair["name"])

            self.once = True


    def checkInfo(self):
        # t = time() - self.last
        # self.processcheck()
        # cpu_temp = self.get_cpu_temperature()
        # cpu_percent = psutil.cpu_percent(1)
        # if (cpu_temp>=98):
        #     print("Reboot")
        #     os.system("systemctl reboot -i")

        self.device, self.paired = self.speaker.check_devices()
        # print("connected device : ", self.device)
        if (self.device):
            if (self.connection): 
                self.connection.set_speaker(1)
                self.label_room.setText(self.room)
            self.label_speaker_name.setText(self.device["name"])
            # self.label_speaker_connection.setText("متصل")
            self.addActionButton()
            self.cb.setEnabled(False)
            self.connect_paired_button.setEnabled(False)
            self.button_scan.setEnabled(False)
            self.battery = self.getPowerLevel(self.device["mac"])
            if (self.battery>=0):
                self.battery_text = str(self.battery) + " %"
                # print("Battery Level: ", self.battery_text)
                self.label_battery_level.setText(self.battery_text)
            else:
                self.label_battery_level.setText("-")
            self.scanning = False
            self.devs = []
            self.resetScan()
            
        else:
            if (self.connection): self.connection.set_speaker(0)
            self.label_speaker_name.setText("-")
            self.label_battery_level.setText("-")
            # self.label_speaker_connection.setText("-")
            self.clearActionButton()
            self.cb.setEnabled(True)
            if (not self.scanning): self.button_scan.setEnabled(True)
            self.connect_paired_button.setEnabled(True)
            if(not self.once): self.checkPairedSpeakers()
            # self.once = True
            # self.cb.clear()
            # for pair in self.paired:
            #     self.cb.addItem(pair["name"])

            # self.once = False
        if (self.connection):
            self.room = self.connection.get_room()
            # print("connection room : ", self.room )
            self.label_room.setText(self.room)

        # ip, self.running = self.getIPRunning()
        # # print(ip)
        # if (self.running):
        #     self.label_ip_connection.setText("متصل")
        # else:
        #     self.label_ip_connection.setText("غير متصل")
        
        self.running = self.getRunning()

        # self.ip = self.getIP(self.interface)

        self.ip = self.getIP("eth0")
        if (self.ip==None): 
            self.ip = self.getIP("wlan0")

        # print("ip : ", self.ip)
        self.label_6.setText("IP العنوان")
        if(self.ip!=None): self.label_ip.setText(self.ip)

        if (self.running):
            self.label_ip_connection.setText("متصل")
            self.label_ip_connection.setStyleSheet("color: green;")
        else:
            self.label_ip_connection.setText("غير متصل")
            self.label_ip_connection.setStyleSheet("color: red;")

        self.check_if_client_connected()
        # self.ListenScanning()
        self.last = time()
        # sleep(1)

        
    def check_if_client_connected(self):
        check, toned = self.receiver.check_client()
        self.connection_status = self.getRunning()

        if (check):
            if (toned):
                self.speaking(True)
                self.speaking_status = True
        else:
            self.speaking(False)
            self.speaking_status = False

    def StartSpeaking(self):
        self.speaking(True)
        self.speak_timer.stop()
        self.speaking_status = True

    def StopSpeaking(self):
        self.speaking(False)
        self.speaking_status = False
        self.nospeak_timer.stop()


    def showTime(self):
        time=QDateTime.currentDateTime()
        timeDisplay=time.toString('yyyy-MM-dd hh:mm:ss dddd')
        # print(timeDisplay)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "لوحة التحم"))
        self.label.setText(_translate("MainWindow", "معلومات الاتصال"))
        self.label_6.setText(_translate("MainWindow", "IP العنوان"))
        self.label_ip.setText(_translate("MainWindow", self.ip))
        self.label_8.setText(_translate("MainWindow", "الحالة"))
        self.label_ip_connection.setText(_translate("MainWindow", "-"))
        self.label1.setText(_translate("MainWindow", "معلومات السماعة"))
        self.label_2.setText(_translate("MainWindow", "اسم السماعة"))
        self.label_speaker_name.setText(_translate("MainWindow", "-"))
        # self.label_4.setText(_translate("MainWindow", "الحالة"))
        # self.label_speaker_connection.setText(_translate("MainWindow", "-"))
        # self.label_10.setText(_translate("MainWindow", "معلومات عملية التحدث"))
        self.label_11.setText(_translate("MainWindow", "الحالة"))
        # self.label_streaming_status.setText(_translate("MainWindow", "-"))
        self.button_scan.setText(_translate("MainWindow", "بحث سماعات البلوتوث"))

    def loading(self):
        # print("loading")
        self.scanning = True
        label = QtWidgets.QLabel()
        label.setText("الرجاء الانتظار…")
        label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.devicesLayout.addWidget(label)
     
  
    def get_volume(self):
        try:
            proc = subprocess.Popen('/usr/bin/amixer sget Master', shell=True, stdout=subprocess.PIPE)
            amixer_stdout = proc.communicate()[0].decode().split('\n')[5]
            proc.wait()
            find_start = amixer_stdout.find('[') + 1
            find_end = amixer_stdout.find('%]', find_start)
            return amixer_stdout[find_start:find_end]
        except:
            return "0"


    def set_volume(self, volume):
        val = volume
        val = float(int(val))
        proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE)
        proc.wait()
        

    def getIPRunning(self):
        running = False
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.connect(("8.8.8.8", 80))
            ip = my_socket.getsockname()[0]
            # print('Your IP Address is',ip)
            running = True
        except:
            ip = ""
            running = False
        return ip, running
    
    def setup_server(self):
        # self.HOST = '0.0.0.0'
        self.HOST = ''
        self.PORT = 9999
        self.receiver = AudioReceiver(self.HOST, self.PORT, 100)
        self.connection = ServerConnection(self.HOST, 7777)
        self.connection.start_server()

    def start_server(self):
        if (self.receiver): 
            self.receiver.start_server()
            # print(self.receiver.isRunning())
        else:
            self.setup_server()
            self.receiver.start_server()
            # print(self.receiver.isRunning())

    def closeWindow(self, event):
        dlg = AlertDialog("إغلاق البرنامج", "هل تريد إغلاق البرنامج؟", "نعم", "لا")
        if dlg.exec():
            # print("Success!")
            event.accept()
            print(self.quit)
        else:
            print("Cancel!")

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def closeEvent(self,event):
        dlg = AlertDialog("إغلاق البرنامج", "هل تريد إغلاق البرنامج؟", "نعم", "لا")
        if dlg.exec():
            event.accept()
            print(self.quit)
        else:
            print("Cancel!")


app = QApplication([])

window = Window()
window.showFullScreen()
sys.exit(app.exec())