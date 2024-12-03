from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd
import matplotlib.pyplot as plt
import pyqtgraph as pg
from PyQt5.QtGui import QIcon
from fpdf import FPDF
import os
import pyqtgraph.exporters
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from pyqtgraph.examples.optics import ParamObj


class Spectrograph(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.style.use('dark_background')

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Frequency')

        super(Spectrograph, self).__init__(self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def update_graph(self, file, col, v_max):
        self.axes.clear()

        self.axes.specgram(file, Fs=10e6, cmap=col, vmin=None, vmax=v_max)
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Frequency')

        self.draw()


class Ui_MainWindow(object):
    # flag for pause function
    numberOfFiles = 0
    max_xvalue = 0
    min_yvalue = 0
    max_yvalue = 0
    interval1 = 80
    interval2 = 80
    interval3 = 80
    lastPoint1 = 0
    lastPoint2 = 0
    lastPoint3 = 0
    zoomDegree = 1
    isChanged = False
    isPaused = False
    # the length of data on a file
    dataLength = 0
    filenames = dict()
    image_list = []
    info_list = []
    Current_File = dict()
    spectroImg_list = [None, None, None]
    # pens colors for the graph
    wave1_WHITE = [255, 255, 255]
    wave1_MAROON = [220, 20, 60]
    wave1_YELLOW = [255, 215, 0]
    wave2_WHITE = [255, 255, 255]
    wave2_MAROON = [220, 20, 60]
    wave2_YELLOW = [255, 215, 0]
    wave3_WHITE = [255, 255, 255]
    wave3_MAROON = [220, 20, 60]
    wave3_YELLOW = [255, 215, 0]
    invisible1 = None
    invisible2 = None
    invisible3 = None
    csv1 = pd.DataFrame()
    csv2 = pd.DataFrame()
    csv3 = pd.DataFrame()
    # a list for pens to used in plot function
    wave1_colors = [wave1_WHITE, wave1_MAROON, wave1_YELLOW, invisible1]
    wave2_colors = [wave2_WHITE, wave2_MAROON, wave2_YELLOW, invisible2]
    wave3_colors = [wave3_WHITE, wave3_MAROON, wave3_YELLOW, invisible3]
    curr_csv = []
    # stores number of the selected widget
    current_widget = int
    color1 = int
    color2 = int
    color3 = int

    # intial graph range
    graph_rangeMin = [0, 0, 0]
    graph_rangeMax = [1, 1, 1]
    cmap = 'Greys'
    curr = None
    maxs = None
    idx1 = 0
    idx2 = 0
    idx3 = 0
    speed1 = 5
    speed2 = 5
    speed3 = 5
    Move = 0.1



    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 1000)
        self.timer1 = QtCore.QTimer()
        self.timer1.setInterval(self.interval1)
        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(self.interval2)
        self.timer3 = QtCore.QTimer()
        self.timer3.setInterval(self.interval3)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(305, 20, 311, 71))
        self.label.setObjectName("label")

        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(25, 160, 311, 71))
        self.label_1.setObjectName("label_1")


        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(25, 170, 311, 71))
        self.label_2.setObjectName("label_2")
        self.label_2.resize(80, 80)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(25, 180, 311, 71))
        self.label_3.setObjectName("label_3")
        self.label_2.resize(80, 80)

        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(160, 185, 110, 70))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.vboxlayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.vboxlayout_3.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout_3.setSpacing(1)
        self.vboxlayout_3.setObjectName("vboxlayout_3")


        self.vboxlayout_3.addWidget(self.label_1)
        self.vboxlayout_3.addWidget(self.label_2)
        self.vboxlayout_3.addWidget(self.label_3)

        self.verticalLayoutWidget_1 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_1.setGeometry(QtCore.QRect(850, 120, 600, 600))
        self.verticalLayoutWidget_1.setObjectName("verticalLayoutWidget_1")
        self.vboxlayout_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_1)
        self.vboxlayout_1.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout_1.setSpacing(7)
        self.vboxlayout_1.setObjectName("vboxlayout_1")
        self.vboxlayout_1.addWidget(self.label)

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(850, 120, 600, 600))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.vboxlayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.vboxlayout_2.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout_2.setSpacing(7)
        self.vboxlayout_2.setObjectName("vboxlayout_2")

        self.graph = Spectrograph(self.centralwidget, width=16, height=15, dpi=100)
        self.vboxlayout_1.addWidget(self.graph)

        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.slider.setTickPosition(self.slider.TicksBothSides)
        self.slider.setTickInterval(5)
        self.slider.setSingleStep(1)
        self.slider.setMinimum(0)
        self.slider.setMaximum(225)
        self.vboxlayout_1.addWidget(self.slider)

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.splitter.setGeometry(QtCore.QRect(250, 50, 1200, 700))

        self.scroll = QtWidgets.QScrollBar(Qt.Horizontal)
        self.horizontalB_bar_limit = 1000  #
        self.scroll.setRange(0, self.horizontalB_bar_limit)

        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(140, 120, 661, 200))
        self.graphicsView.setObjectName("graphicsView")
        self.vboxlayout_2.addWidget(self.graphicsView)
        self.vboxlayout_2.addWidget(self.scroll)


        self.splitter.addWidget(self.verticalLayoutWidget_1)
        self.splitter.addWidget(self.verticalLayoutWidget_2)


        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 160, 110, 500))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setSpacing(7)
        self.vboxlayout.setObjectName("vboxlayout")

        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.vboxlayout.addWidget(self.comboBox)

        self.comboBox2 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox2.setObjectName("comboBox2")
        self.comboBox2.addItem("")
        self.comboBox2.addItem("")
        self.comboBox2.addItem("")
        self.vboxlayout.addWidget(self.comboBox2)

        self.comboBox5 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox5.setObjectName("comboBox5")
        self.comboBox5.addItem("")
        self.comboBox5.addItem("")
        self.comboBox5.addItem("")
        self.vboxlayout.addWidget(self.comboBox5)

        self.comboBox6 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox6.setObjectName("comboBox6")
        self.comboBox6.addItem("")
        self.comboBox6.addItem("")
        self.comboBox6.addItem("")
        self.vboxlayout.addWidget(self.comboBox6)

        self.comboBox3 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox3.setObjectName("comboBox3")
        self.comboBox3.addItem("")
        self.comboBox3.addItem("")
        self.comboBox3.addItem("")
        self.vboxlayout_1.addWidget(self.comboBox3)

        self.comboBox4 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox4.setObjectName("comboBox4")
        self.comboBox4.addItem("")
        self.comboBox4.addItem("")
        self.comboBox4.addItem("")
        self.comboBox4.addItem("")
        self.comboBox4.addItem("")
        self.vboxlayout_1.addWidget(self.comboBox4)

        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("F:/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.vboxlayout.addWidget(self.pushButton)
        self.pushButton.setToolTip(" Add File")

        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("F:/pll.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setObjectName("pushButton_3")
        self.vboxlayout.addWidget(self.pushButton_3)
        self.pushButton_3.setToolTip("cine")

        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("F:/p.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setObjectName("pushButton_2")
        self.vboxlayout.addWidget(self.pushButton_2)
        self.pushButton_2.setToolTip("pause")

        self.pushButton_5 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("F:/r.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon)
        self.pushButton_5.setObjectName("pushButton_5")
        self.vboxlayout.addWidget(self.pushButton_5)
        self.pushButton_5.setToolTip("restart")

        self.pushButton_7 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("F:/c.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon)
        self.pushButton_7.setObjectName("pushButton_7")
        self.vboxlayout.addWidget(self.pushButton_7)
        self.pushButton_7.setToolTip("clear")

        self.pushButton_6 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("F:/e.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon)
        self.pushButton_6.setObjectName("pushButton_6")
        self.vboxlayout.addWidget(self.pushButton_6)
        self.pushButton_6.setToolTip("Exit")

        self.pushButton_8 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.vboxlayout.addWidget(self.pushButton_8)
        self.pushButton_8.setToolTip("Zoom In")

        self.pushButton_9 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.vboxlayout.addWidget(self.pushButton_9)
        self.pushButton_9.setToolTip("Zoom Out")

        self.pushButton_11 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("F:/ra.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_11.setIcon(icon)
        self.pushButton_11.setObjectName("pushButton_11")
        self.vboxlayout.addWidget(self.pushButton_11)
        self.pushButton_11.setToolTip("Move Right")

        self.pushButton_12 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("F:/lef.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_12.setIcon(icon)
        self.pushButton_12.setObjectName("pushButton_12")
        self.vboxlayout.addWidget(self.pushButton_12)
        self.pushButton_12.setToolTip("Move Left")

        self.pushButton_13 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("F:/ex.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_13.setIcon(icon)
        self.pushButton_13.setObjectName("pushButton_13")
        self.vboxlayout.addWidget(self.pushButton_13)
        self.pushButton_13.setToolTip("Export")

        self.pushButton_14 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_14.setObjectName("pushButton_14")
        self.vboxlayout.addWidget(self.pushButton_14)

        self.pushButton_15 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("F:/sw.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_15.setIcon(icon)
        self.pushButton_15.setObjectName("pushButton_15")
        self.vboxlayout.addWidget(self.pushButton_15)
        self.pushButton_15.setToolTip("Switch")

        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(140, 185, 40, 70))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.vboxlayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.vboxlayout_4.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout_4.setSpacing(1)
        self.vboxlayout_4.setObjectName("vboxlayout_4")

        self.pushButton_16 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_16.setObjectName("pushButton_16")
        self.pushButton_16.resize(22, 22)
        self.vboxlayout_4.addWidget(self.pushButton_16)

        self.pushButton_18 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_18.setObjectName("pushButton_18")
        self.pushButton_18.resize(22, 22)
        self.vboxlayout_4.addWidget(self.pushButton_18)

        self.pushButton_19 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_19.setObjectName("pushButton_19")
        self.pushButton_19.resize(22, 22)
        self.vboxlayout_4.addWidget(self.pushButton_19)



        self.pushButton_17 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("F:/pdf.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_17.setIcon(icon)
        self.pushButton_17.setObjectName("pushButton_17")
        self.vboxlayout.addWidget(self.pushButton_17)
        self.pushButton_17.setToolTip("PDF")



        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 845, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # connecting button to function
        self.pushButton.clicked.connect(self.load_file)
        self.pushButton_7.clicked.connect(self.clear)
        self.pushButton_3.clicked.connect(self.start1)
        self.pushButton_2.clicked.connect(self.pause)
        self.pushButton_6.clicked.connect(self.close)
        self.pushButton_5.clicked.connect(self.restart)
        self.pushButton_8.clicked.connect(self.zoom_in)
        self.pushButton_9.clicked.connect(self.zoom_out)
        self.pushButton_11.clicked.connect(self.move_right)
        self.pushButton_12.clicked.connect(self.move_left)
        self.pushButton_13.clicked.connect(self.export)
        self.pushButton_14.clicked.connect(self.changeSpeed)
        self.pushButton_15.clicked.connect(self.check_color_spec)
        self.pushButton_15.clicked.connect(self.check_spec)
        self.pushButton_16.clicked.connect(self.show_hide_1)
        self.pushButton_18.clicked.connect(self.show_hide_2)
        self.pushButton_19.clicked.connect(self.show_hide_3)
        self.pushButton_17.clicked.connect(self.create_pdf)
        self.comboBox.activated.connect(self.ischangedMethod)
        self.scroll.valueChanged.connect(self.update)
        self.slider.valueChanged.connect(self.slidy)

        self.wave1 = self.graphicsView

        # will help to identify which widget or wave we are trying to reference basically save which graph we use
        self.widgets = [self.wave1]

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SignalViewer"))
        MainWindow.setStyleSheet("background:peachpuff")

        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; "
                                      "font-weight:600; color:#00007f;\">SIGNAL VIEWER</span></p></body></html>"))
        self.label_1.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; "
                                      "font-weight:600; color:#00007f;\">Wave1</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; "
                                      "font-weight:600; color:#00007f;\">Wave2</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; "
                                      "font-weight:600; color:#00007f;\">Wave3</span></p></body></html>"))
        self.comboBox.setItemText(0, _translate("MainWindow", "wave1"))
        self.comboBox.setItemText(1, _translate("MainWindow", "wave2"))
        self.comboBox.setItemText(2, _translate("MainWindow", "wave3"))
        self.pushButton.setText("")
        self.pushButton_3.setText("")
        self.pushButton_2.setText("")
        self.pushButton_7.setText("")
        self.pushButton_6.setText("")
        self.pushButton_5.setText("")
        self.pushButton_8.setText(_translate("MainWindow", "zoom_in(100%)"))
        self.pushButton_9.setText(_translate("MainWindow", "zoom_out(100%)"))
        self.pushButton_11.setText("")
        self.pushButton_12.setText("")
        self.pushButton_13.setText("")
        self.pushButton_14.setText(_translate("MainWindow", "1x"))
        self.pushButton_15.setText("")
        self.pushButton_16.setText("Hide")
        self.pushButton_18.setText("Hide")
        self.pushButton_19.setText("Hide")
        self.pushButton_17.setText("")

        self.pushButton.setStyleSheet("background:#FFA352")
        self.pushButton_2.setStyleSheet("background:#FFA352")
        self.pushButton_3.setStyleSheet("background:#FFA352")
        self.pushButton_14.setStyleSheet("background:#FFA352")
        self.pushButton_5.setStyleSheet("background:#FFA352")
        self.pushButton_9.setStyleSheet("background:#FFA352")
        self.pushButton_8.setStyleSheet("background:#FFA352")
        self.pushButton_6.setStyleSheet("background:#FFA352")
        self.pushButton_7.setStyleSheet("background:#FFA352")
        self.pushButton_13.setStyleSheet("background:#FFA352")
        self.pushButton_11.setStyleSheet("background:#FFA352")
        self.pushButton_12.setStyleSheet("background:#FFA352")
        self.pushButton_15.setStyleSheet("background:#FFA352")

        self.comboBox2.setItemText(0, _translate("MainWindow", "WHITE"))
        self.comboBox2.setItemText(1, _translate("MainWindow", "MAROON"))
        self.comboBox2.setItemText(2, _translate("MainWindow", "YELLOW"))
        self.comboBox5.setItemText(0, _translate("MainWindow", "WHITE"))
        self.comboBox5.setItemText(1, _translate("MainWindow", "MAROON"))
        self.comboBox5.setItemText(2, _translate("MainWindow", "YELLOW"))
        self.comboBox6.setItemText(0, _translate("MainWindow", "WHITE"))
        self.comboBox6.setItemText(1, _translate("MainWindow", "MAROON"))
        self.comboBox6.setItemText(2, _translate("MainWindow", "YELLOW"))
        self.comboBox3.setItemText(0, _translate("MainWindow", "spec_wave_1"))
        self.comboBox3.setItemText(1, _translate("MainWindow", "spec_wave_2"))
        self.comboBox3.setItemText(2, _translate("MainWindow", "spec_wave_3"))
        self.comboBox4.setItemText(0, _translate("MainWindow", "viridis"))
        self.comboBox4.setItemText(1, _translate("MainWindow", "plasma"))
        self.comboBox4.setItemText(2, _translate("MainWindow", "inferno"))
        self.comboBox4.setItemText(3, _translate("MainWindow", "Blues"))
        self.comboBox4.setItemText(4, _translate("MainWindow", "cividis"))

    def changeSpeed2(self):
        self.speed1 = 5
        self.speed2 = 5
        self.speed3 = 5
        self.pushButton_14.setText("1x")
        self.isChanged = False

    def changeSpeed(self):

        text1 = self.pushButton_14.text()

        if text1 == "1x" and self.comboBox.currentText() == "wave1":
            self.speed1 = 2 * self.speed1
            self.pushButton_14.setText("2x")

        elif text1 == "2x" and self.comboBox.currentText() == "wave1":
            self.speed1 = 5
            self.speed1 = 4 * self.speed1
            self.pushButton_14.setText("4x")

        elif text1 == "4x" and self.comboBox.currentText() == "wave1":
            self.speed1 = 5
            self.speed1 = 8 * self.speed1
            self.pushButton_14.setText("8x")
        elif text1 == "8x" and self.comboBox.currentText() == "wave1":
            self.speed1 = 5
            self.pushButton_14.setText("1x")

        if text1 == "1x" and self.comboBox.currentText() == "wave2":
            self.speed2 = 2 * self.speed2
            self.pushButton_14.setText("2x")

        elif text1 == "2x" and self.comboBox.currentText() == "wave2":
            self.speed2 = 5
            self.speed2 = 4 * self.speed2
            self.pushButton_14.setText("4x")

        elif text1 == "4x" and self.comboBox.currentText() == "wave2":
            self.speed2 = 5
            self.speed2 = 8 * self.speed2
            self.pushButton_14.setText("8x")
        elif text1 == "8x" and self.comboBox.currentText() == "wave2":
            self.speed2 = 5
            self.pushButton_14.setText("1x")

        if text1 == "1x" and self.comboBox.currentText() == "wave3":
            self.speed3 = 2 * self.speed3
            self.pushButton_14.setText("2x")
        elif text1 == "2x" and self.comboBox.currentText() == "wave3":
            self.speed3 = 5
            self.speed3 = 4 * self.speed3
            self.pushButton_14.setText("4x")

        elif text1 == "4x" and self.comboBox.currentText() == "wave3":
            self.speed3 = 5
            self.speed3 = 8 * self.speed3
            self.pushButton_14.setText("8x")

        elif text1 == "8x" and self.comboBox.currentText() == "wave3":
            self.speed3 = 5
            self.pushButton_14.setText("1x")

    def show_hide_1(self):
        text2 = self.pushButton_16.text()

        if text2 == "Hide":
            self.color1 = 3
            self.data_line1.setData(self.xs, self.ys, pen=self.wave1_colors[self.color1])
            self.graphicsView.plotItem.legend.removeItem(self.data_line1.name())
            self.pushButton_16.setText("Show")

        elif text2 == "Show":
            self.check_color1()
            self.data_line1.setData(self.xs, self.ys, pen=self.wave1_colors[self.color1])
            self.data_line1 = self.graphicsView.plot(
                self.x1, self.y1, name=self.name1, pen=None)
            self.pushButton_16.setText("Hide")

    def show_hide_2(self):
        text2 = self.pushButton_18.text()
        if text2 == "Hide":
            self.color2 = 3
            self.data_line2.setData(self.xs2, self.ys2, pen=self.wave2_colors[self.color2])
            self.graphicsView.plotItem.legend.removeItem(self.data_line2.name())
            self.pushButton_18.setText("Show")
        elif text2 == "Show":
            self.check_color2()
            self.data_line2 = self.graphicsView.plot(
                self.x2, self.y2, name=self.name2, pen=None)
            self.data_line2.setData(self.xs2, self.ys2, pen=self.wave2_colors[self.color2])
            self.pushButton_18.setText("Hide")

    def show_hide_3(self):
        text2 = self.pushButton_19.text()
        if text2 == "Hide":
            self.color3 = 3
            self.data_line3.setData(self.xs3, self.ys3, pen=self.wave3_colors[self.color3])
            self.graphicsView.plotItem.legend.removeItem(self.data_line3.name())
            self.pushButton_19.setText("Show")
        elif text2 == "Show":
            self.check_color3()
            self.data_line3 = self.graphicsView.plot(
                self.x3, self.y3, name=self.name3, pen=None)
            self.data_line3.setData(self.xs3, self.ys3, pen=self.wave3_colors[self.color3])
            self.pushButton_19.setText("Hide")

    def load_file(self):
        self.numberOfFiles += 1
        if self.numberOfFiles <= 3:
            self.load_file2()
        else:
            print("max number of files uploaded is 3")

    def load_file2(self):
        # a function that loads the files data

        if self.numberOfFiles == 1:
            self.check_color1()
            self.filename1, self.format1 = QtWidgets.QFileDialog.getOpenFileName(None, "Load Signal File 1", "",
                                                                                 "*.csv;;")
            self.x1 = pd.read_csv(self.filename1).iloc[:, 0]
            self.y1 = pd.read_csv(self.filename1).iloc[:, 1]
            self.info1 = self.y1.describe().to_string()
            self.info_list.append(self.info1)
            self.maxy1 = self.y1.max()
            self.miny1 = self.y1.min()
            self.xmax1 = self.x1.max()
            self.plot_signal_info1(self.y1, self.filename1)
            self.graphicsView.setLimits(xMin=0, xMax=self.xmax1, yMin=self.miny1, yMax=self.maxy1)

        elif self.numberOfFiles == 2:
            self.check_color2()
            self.filename2, self.format2 = QtWidgets.QFileDialog.getOpenFileName(None, "Load Signal File 2", "",
                                                                                 "*.csv;;")
            self.x2 = pd.read_csv(self.filename2).iloc[:, 0]
            self.y2 = pd.read_csv(self.filename2).iloc[:, 1]
            self.info2 = self.y2.describe().to_string()
            self.info_list.append(self.info2)

            self.maxy2 = self.y2.max()
            self.miny2 = self.y2.min()
            self.xmax2 = self.x2.max()

            self.max_xvalue = max(self.xmax1, self.xmax2)
            self.min_yvalue = min(self.miny1, self.miny2)
            self.max_yvalue = max(self.maxy1, self.maxy2)
            self.plot_signal_info2(self.y2, self.filename2)
            self.graphicsView.setLimits(xMin=0, xMax=self.max_xvalue, yMin=self.min_yvalue, yMax=self.max_yvalue)

        elif self.numberOfFiles == 3:

            self.check_color3()
            self.filename3, self.format3 = QtWidgets.QFileDialog.getOpenFileName(None, "Load Signal File 3", "",
                                                                                 "*.csv;;")
            self.x3 = pd.read_csv(self.filename3).iloc[:, 0]
            self.y3 = pd.read_csv(self.filename3).iloc[:, 1]

            self.info3 = self.y3.describe().to_string()

            self.info_list.append(self.info3)

            self.maxy3 = self.y3.max()
            self.miny3 = self.y3.min()
            self.xmaxy3 = self.x3.max()

            self.max_xvalue = max(self.max_xvalue, self.xmaxy3)
            self.min_yvalue = min(self.min_yvalue, self.miny3)
            self.max_yvalue = max(self.max_yvalue, self.maxy3)
            self.graphicsView.setLimits(xMin=0, xMax=self.max_xvalue, yMin=self.min_yvalue, yMax=self.max_yvalue)

            self.plot_signal_info3(self.y3, self.filename3)

        self.graph.update_graph(self.y1, self.cmap, self.maxs)

    def start1(self):
        self.isPaused = False
        if self.numberOfFiles > 0:
            self.current_widget = 0
            self.timer1.timeout.connect(self.update_plot_data1)
            self.timer1.start(50)
        if self.numberOfFiles >= 2:
            self.current_widget = 1
            self.timer2.timeout.connect(self.update_plot_data2)
            self.timer2.start(50)
        if self.numberOfFiles == 3:
            self.current_widget = 2
            self.timer3.timeout.connect(self.update_plot_data3)
            self.timer3.start(50)

    def update_plot_data1(self):
        text16 = self.pushButton_16.text()

        if text16 == "Hide":

            self.check_color1()

        if self.isChanged:
            self.changeSpeed2()

        if not self.isPaused:

            self.idx1 += self.speed1
            self.xs = self.x1[:self.idx1]
            self.ys = self.y1[:self.idx1]
            # shrink range of x-axis
            self.lastPoint1 = self.xs[self.idx1-1]
            if self.lastPoint1 >= max(self.lastPoint2, self.lastPoint3):
                self.graphicsView.plotItem.setXRange(
                    max(self.xs, default=0) - self.zoomDegree, max(self.xs, default=0))

            elif self.lastPoint2 >= max(self.lastPoint1, self.lastPoint3):
                self.graphicsView.plotItem.setXRange(
                    max(self.xs2, default=0) - self.zoomDegree, max(self.xs2, default=0))

            elif self.lastPoint3 >= max(self.lastPoint1, self.lastPoint2):
                self.graphicsView.plotItem.setXRange(
                    max(self.xs3, default=0) - self.zoomDegree, max(self.xs3, default=0))

            # Plot the new data
            self.data_line1.setData(self.xs, self.ys, pen=self.wave1_colors[self.color1])
        else:
            self.timer1.stop()

    def update_plot_data2(self):
        text18 = self.pushButton_18.text()

        if text18 == "Hide":
            self.check_color2()

        if self.isChanged:
            self.changeSpeed2()

        if not self.isPaused:

            self.idx2 += self.speed2
            self.xs2 = self.x2[:self.idx2]
            self.ys2 = self.y2[:self.idx2]
            # shrink range of x-axis
            self.lastPoint2 = self.xs2[self.idx2-1]

            if self.lastPoint1 >= max(self.lastPoint2, self.lastPoint3):
                self.graphicsView.plotItem.setXRange(
                    max(self.xs, default=0) - self.zoomDegree, max(self.xs, default=0))

            elif self.lastPoint2 >= max(self.lastPoint1, self.lastPoint3):
                self.graphicsView.plotItem.setXRange(
                    max(self.xs2, default=0) - self.zoomDegree, max(self.xs2, default=0))

            elif self.lastPoint3 >= max(self.lastPoint1, self.lastPoint2):
                self.graphicsView.plotItem.setXRange(
                    max(self.xs3, default=0) - self.zoomDegree, max(self.xs3, default=0))
            # Plot the new data
            self.data_line2.setData(self.xs2, self.ys2, pen=self.wave2_colors[self.color2])

        else:
            self.timer2.stop()

    def update_plot_data3(self):
        text19 = self.pushButton_19.text()
        if text19 == "Hide":

            self.check_color3()

        if self.isChanged:
            self.changeSpeed2()

        if not self.isPaused:

            self.idx3 += self.speed3
            self.xs3 = self.x3[:self.idx3]
            self.ys3 = self.y3[:self.idx3]
            # shrink range of x-axis
            self.lastPoint3 = self.xs3[self.idx3-1]

            if self.lastPoint1 >= max(self.lastPoint2, self.lastPoint3):
                self.graphicsView.plotItem.setXRange(
                    max(self.xs, default=0) - self.zoomDegree, max(self.xs, default=0))

            elif self.lastPoint2 >= max(self.lastPoint1, self.lastPoint3):
                self.graphicsView.plotItem.setXRange(
                    max(self.xs2, default=0) - self.zoomDegree, max(self.xs2, default=0))

            elif self.lastPoint3 >= max(self.lastPoint1, self.lastPoint2):
                self.graphicsView.plotItem.setXRange(
                    max(self.xs3, default=0) - self.zoomDegree, max(self.xs3, default=0))

            self.data_line3.setData(self.xs3, self.ys3, pen=self.wave3_colors[self.color3])

        else:
            self.timer3.stop()

    def pause(self):
        self.isPaused = True

    def getCurrentSpeed(self):

        text1 = self.pushButton_14.text()
        if self.comboBox.currentText() == "wave1":

            self.speed1 = 5
            if text1 == "1x":
                return self.speed1
            elif text1 == "2x":
                return 2 * self.speed1
            elif text1 == "4x":
                return 4 * self.speed1
            elif text1 == "8x":
                return 8 * self.speed1

        elif self.comboBox.currentText() == "wave2":

            self.speed2 = 5
            if text1 == "1x":
                return self.speed2
            elif text1 == "2x":
                return 2 * self.speed2
            elif text1 == "4x":
                return 4 * self.speed2
            elif text1 == "8x":
                return 8 * self.speed2

        elif self.comboBox.currentText() == "wave3":

            self.speed3 = 5
            if text1 == "1x":
                return self.speed3
            elif text1 == "2x":
                return 2 * self.speed3
            elif text1 == "4x":
                return 4 * self.speed3
            elif text1 == "8x":
                return 8 * self.speed3

    def zoom_in(self):

        text1 = self.pushButton_8.text()
        text2 = text1[8:]
        self.zoom = text2[:-1]

        if self.zoom == "100%":
            self.pushButton_8.setText("zoom_in(200%)")
            self.zoomDegree = self.zoomDegree / 2

        elif self.zoom == "200%":
            self.pushButton_8.setText("zoom_in(400%)")
            self.zoomDegree = self.zoomDegree / 2

        elif self.zoom == "400%":
            self.pushButton_8.setText("zoom_in(100%)")
            self.zoomDegree = 4 * self.zoomDegree

        if self.lastPoint1 >= max(self.lastPoint2, self.lastPoint3):
            self.graphicsView.plotItem.setXRange(
                max(self.xs, default=0) - self.zoomDegree, max(self.xs, default=0))

        elif self.lastPoint2 >= max(self.lastPoint1, self.lastPoint3):
            self.graphicsView.plotItem.setXRange(
                max(self.xs2, default=0) - self.zoomDegree, max(self.xs2, default=0))

        elif self.lastPoint3 >= max(self.lastPoint1, self.lastPoint2):
            self.graphicsView.plotItem.setXRange(
                max(self.xs3, default=0) - self.zoomDegree, max(self.xs3, default=0))

    def zoom_out(self):

        text1 = self.pushButton_9.text()
        text2 = text1[9:]
        self.zoom = text2[:-1]

        if self.zoom == "100%":
            self.pushButton_9.setText("zoom_out(50%)")
            self.zoomDegree = 2 * self.zoomDegree

        elif self.zoom == "50%":
            self.pushButton_9.setText("zoom_out(25%)")
            self.zoomDegree = 2 * self.zoomDegree

        elif self.zoom == "25%":
            self.pushButton_9.setText("zoom_out(100%)")
            self.zoomDegree = self.zoomDegree / 4

        if self.lastPoint1 >= max(self.lastPoint2, self.lastPoint3):
            self.graphicsView.plotItem.setXRange(
                max(self.xs, default=0) - self.zoomDegree, max(self.xs, default=0))

        elif self.lastPoint2 >= max(self.lastPoint1, self.lastPoint3):
            self.graphicsView.plotItem.setXRange(
                max(self.xs2, default=0) - self.zoomDegree, max(self.xs2, default=0))

        elif self.lastPoint3 >= max(self.lastPoint1, self.lastPoint2):
            self.graphicsView.plotItem.setXRange(
                max(self.xs3, default=0) - self.zoomDegree, max(self.xs3, default=0))

    def move_right(self):

        self.graphicsView.setXRange(self.graph_rangeMin[0] + self.Move,
                                    self.graph_rangeMax[0] + self.Move)

        self.graph_rangeMin[0] = self.graph_rangeMin[0] + self.Move
        self.graph_rangeMax[0] = self.graph_rangeMax[0] + self.Move

    def move_left(self):

        self.graphicsView.setXRange(self.graph_rangeMin[0] - self.Move,
                                    self.graph_rangeMax[0] - self.Move)

        self.graph_rangeMin[0] = self.graph_rangeMin[0] - self.Move
        self.graph_rangeMax[0] = self.graph_rangeMax[0] - self.Move

    def restart(self):
        # the reseting happens regardless of which function am in
        self.timer1.stop()
        self.timer2.stop()
        self.timer3.stop()
        self.idx1 = 0
        self.idx2 = 0
        self.idx3 = 0
        self.timer1.start()
        self.timer2.start()
        self.timer3.start()

    def ischangedMethod(self):
        self.isChanged = True

    def clear(self):
        # a functions that clears a graph and delete its file if the graph was occupied
        self.graphicsView.clear()  # list clear fucntion to show that the graph is clear

    def check_color1(self):
        # a function checks the selected widget

        if self.comboBox2.currentText() == "WHITE":
            self.color1 = 0

        elif self.comboBox2.currentText() == "MAROON":
            self.color1 = 1

        elif self.comboBox2.currentText() == "YELLOW":
            self.color1 = 2

    def check_color2(self):
        # a function checks the selected widget

        if self.comboBox5.currentText() == "WHITE":
            self.color2 = 0

        elif self.comboBox5.currentText() == "MAROON":
            self.color2 = 1

        elif self.comboBox5.currentText() == "YELLOW":
            self.color2 = 2

    def check_color3(self):
        # a function checks the selected widget

        if self.comboBox6.currentText() == "WHITE":
            self.color3 = 0

        elif self.comboBox6.currentText() == "MAROON":
            self.color3 = 1

        elif self.comboBox6.currentText() == "YELLOW":
            self.color3 = 2

    def check_color_spec(self):
        # a function checks the selected widget

        if self.comboBox4.currentText() == "viridis":
            self.cmap = "viridis"
        elif self.comboBox4.currentText() == "plasma":
            self.cmap = "plasma"
        elif self.comboBox4.currentText() == "inferno":
            self.cmap = "inferno"
        elif self.comboBox4.currentText() == "Blues":
            self.cmap = "Blues"
        elif self.comboBox4.currentText() == "cividis":
            self.cmap = "cividis"

    def check_spec(self):
        # a function checks the selected widget

        if self.comboBox3.currentText() == "spec_wave_1":

            self.graph.update_graph(self.y1, self.cmap, self.maxs)
        elif self.comboBox3.currentText() == "spec_wave_2":
            self.graph.update_graph(self.y2, self.cmap, self.maxs)

        elif self.comboBox3.currentText() == "spec_wave_3":
            self.graph.update_graph(self.y3, self.cmap, self.maxs)

    def slidy(self):
        self.maxs = self.slider.value()
        if self.slider.value() == 0:
            self.maxs = None

    def update(self, val):
        new_index = int(val / self.horizontalB_bar_limit * len(self.x1))
        x_left, x_right = self.x1[new_index] - .05, self.x1[new_index] + 0.05
        self.graphicsView.setXRange(x_left, x_right)

    def plot_signal_info1(self, file, fileName):
        # the function that plot the graphs on the selected widget
        self.name1 = fileName.split("/")[-1]
        self.graphicsView.plotItem.setTitle("Channel " + str(1))
        self.graphicsView.plotItem.addLegend(size=(2, 3))
        self.graphicsView.plotItem.showGrid(True, True, alpha=1)
        self.graphicsView.plotItem.setLabel("bottom", text="Time in ms")
        self.graphicsView.plotItem.setLabel("left", text="Voltage (V)")
        fig, ax = plt.subplots()
        self.data_line1 = self.graphicsView.plot(
            self.x1, self.y1, name=self.name1, pen=None)
        plt.specgram(file, Fs=10e3)
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.savefig('spectro' + str(1) + '.png')
        self.spectroImg_list[0] = 'spectro' + str(1) + '.png'
        plt.show()
        self.start1()

    def plot_signal_info2(self, file, fileName):
        # the function that plot the graphs on the selected widget
        self.name2 = fileName.split("/")[-1]
        self.graphicsView.plotItem.setTitle("Channel " + str(1))
        self.graphicsView.plotItem.addLegend(size=(2, 3))
        self.graphicsView.plotItem.setLabel("bottom", text="Time in ms")
        self.graphicsView.plotItem.setLabel("left", text="Voltage (V)")
        self.data_line2 = self.graphicsView.plot(
            self.x2, self.y2, name=self.name2, pen=None)
        plt.specgram(file, Fs=10e3)
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.savefig('spectro' + str(2) + '.png')
        self.spectroImg_list[1] = 'spectro' + str(2) + '.png'
        plt.show()
        self.start1()

    def plot_signal_info3(self, file, fileName):
        # the function that plot the graphs on the selected widget
        self.name3 = fileName.split("/")[-1]
        self.graphicsView.plotItem.setTitle("Channel " + str(1))
        self.graphicsView.plotItem.addLegend(size=(2, 3))
        self.graphicsView.plotItem.setLabel("bottom", text="Time in ms")
        self.graphicsView.plotItem.setLabel("left", text="Voltage (V)")
        self.data_line3 = self.graphicsView.plot(
            self.x3, self.y3, name=self.name3, pen=None)
        plt.specgram(file, Fs=10e3)
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.savefig('spectro' + str(3) + '.png')
        self.spectroImg_list[2] = 'spectro' + str(3) + '.png'
        plt.show()
        self.start1()

    def export(self):
        # a function that creates a pictures of the drawn graphs
        exporter1 = pg.exporters.ImageExporter(self.graphicsView.plotItem)
        exporter1.export('signal' + str(self.current_widget) + '.png')

        # stores the pictures files in image list
        self.image_list = ['signal0.png', 'signal1.png', 'signal2.png']



    def create_pdf(self):
        # the function that creates the pdf report

        pdf = FPDF()

        for x in range(3):
            # set pdf title
            pdf.add_page()
            pdf.set_font('Arial', 'B', 15)
            pdf.cell(0, 0, 'Signal no: ' + str(x + 1), 0, 1, 'C')

            # put the graphs on the pdf
            pdf.image(self.image_list[x], 30, 20, 150, 50)
            pdf.image(self.spectroImg_list[x], 30, 80, 150, 100)

        pdf.add_page()
        pdf.set_font('Arial', 'B', 15)
        for x in range(3):
            pdf.cell(60, 0, 'Signal no: ' + str(x + 1), 0, 1, 'C')
            pdf.ln(10)
            pdf.multi_cell(70, 9, self.info_list[x], 1, 0, 'C')
            pdf.ln(10)

        pdf.output("report.pdf", "F")

        # removes the graphs pictures as we dont need
        os.remove("signal0.png")
        os.remove("signal1.png")
        os.remove("signal2.png")
        os.remove("spectro1.png")
        os.remove("spectro2.png")
        os.remove("spectro3.png")

    def close(self):
        sys.exit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())