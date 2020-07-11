#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'moveGUI.ui'
# Created by: PyQt5 UI code generator 5.14.2
# WARNING! All changes made in this file will be lost!
import rospy
from geometry_msgs.msg import Twist
from PyQt5 import QtCore, QtGui, QtWidgets

rospy.init_node('drive')
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(2)
move = Twist()
move.linear.x = 0.0 #Move the robot with a linear velocity in the x axis
move.angular.z = 0.0 #Move the with an angular velocity in the z axis
def publishTo(): 
    print move
    pub.publish(move)
    rate.sleep()
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(190, 60, 391, 241))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.backward = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.backward.setMinimumSize(QtCore.QSize(30, 30))
        self.backward.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backward.setAutoFillBackground(False)
        self.backward.setCheckable(False)
        self.backward.setObjectName("backward")
        self.backward.pressed.connect(self.Bpressed)
        self.backward.released.connect(self.FBreleased)

        self.gridLayout.addWidget(self.backward, 1, 1, 1, 1)
        self.forward = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.forward.setMinimumSize(QtCore.QSize(30, 30))
        self.forward.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.forward.setAutoFillBackground(False)
        self.forward.setCheckable(False)
        self.forward.setObjectName("forward")
        self.forward.pressed.connect(self.Fpressed)
        self.forward.released.connect(self.FBreleased)

        self.gridLayout.addWidget(self.forward, 0, 1, 1, 1)
        self.left = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.left.setMinimumSize(QtCore.QSize(30, 30))
        self.left.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.left.setAutoFillBackground(False)
        self.left.setCheckable(False)
        self.left.setObjectName("left")
        self.left.pressed.connect(self.Lpressed)
        self.left.released.connect(self.RLreleased)

        self.gridLayout.addWidget(self.left, 1, 0, 1, 1)
        self.right = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.right.setMinimumSize(QtCore.QSize(30, 30))
        self.right.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.right.setAutoFillBackground(False)
        self.right.setCheckable(False)
        self.right.setObjectName("right")
        self.right.pressed.connect(self.Rpressed)
        self.right.released.connect(self.RLreleased)

        self.gridLayout.addWidget(self.right, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.forward, self.backward)

    def Fpressed(self):
        move.linear.x = 1.0
        publishTo()
    def FBreleased(self):
        move.linear.x = 0.0
        publishTo()

    def Bpressed(self):
        move.linear.x = -1.0
        publishTo()

    def Rpressed(self):
        move.angular.z = 50.0
        publishTo()
    def RLreleased(self):
        move.angular.z = 0.0
        publishTo()

    def Lpressed(self):
        move.angular.z = -50.0
        publishTo()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.backward.setText(_translate("MainWindow", "Backward"))
        self.forward.setText(_translate("MainWindow", "Forward"))
        self.left.setText(_translate("MainWindow", "Left"))
        self.right.setText(_translate("MainWindow", "Right"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())